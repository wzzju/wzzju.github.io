/* Copyright 2021 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

// An example for reading a HloModule from a HloProto file and execute the
// module on PJRT GPU client.
//
// To build a HloModule,
//
// $ python3 jax/tools/jax_to_ir.py \
// --fn examples.jax_cpp.prog.fn \
// --input_shapes '[("x", "f32[2,2]"), ("y", "f32[2,2]")]' \
// --constants '{"z": 2.0}' \
// --hlo_text_dest /tmp/fn_hlo.txt \
// --hlo_proto_dest /tmp/fn_hlo.pb
//
// To load and run the HloModule,
//
// $ bazel build examples/jax_cpp:main --experimental_repo_remote_exec --check_visibility=false
// $ bazel-bin/examples/jax_cpp/main
// 2021-01-12 15:35:28.316880: I examples/jax_cpp/main.cc:65] result = (
// f32[2,2] {
//   { 1.5, 1.5 },
//   { 3.5, 3.5 }
// }
// )

#include <memory>
#include <string>
#include <vector>

#include "tensorflow/compiler/xla/literal.h"
#include "tensorflow/compiler/xla/literal_util.h"
#include "tensorflow/compiler/xla/pjrt/gpu_device.h"
#include "tensorflow/compiler/xla/pjrt/pjrt_client.h"
#include "tensorflow/compiler/xla/status.h"
#include "tensorflow/compiler/xla/statusor.h"
#include "tensorflow/compiler/xla/tools/hlo_module_loader.h"
#include "tensorflow/core/platform/init_main.h"
#include "tensorflow/core/platform/logging.h"

int main(int argc, char** argv) {
  tensorflow::port::InitMain("", &argc, &argv);

  // Load HloModule from file.
  std::string hlo_filename = "/tmp/fn_hlo.txt";
  std::function<void(xla::HloModuleConfig*)> config_modifier_hook =
      [](xla::HloModuleConfig* config) { config->set_seed(42); };
  std::unique_ptr<xla::HloModule> test_module =
      LoadModuleFromFile(hlo_filename, xla::hlo_module_loader_details::Config(),
                         "txt", config_modifier_hook)
          .ValueOrDie();
  const xla::HloModuleProto test_module_proto = test_module->ToProto();

  // Run it using JAX C++ Runtime (PJRT).

  // Get a GPU client.
  bool asynchronous = true;
  xla::GpuAllocatorConfig allocator_config;
  std::shared_ptr<xla::DistributedRuntimeClient> distributed_client{nullptr};
  int node_id = 0;
  std::unique_ptr<xla::PjRtClient> client =
      xla::GetGpuClient(asynchronous, allocator_config, distributed_client, node_id).ValueOrDie();

  // Compile XlaComputation to PjRtExecutable.
  xla::XlaComputation xla_computation(test_module_proto);
  xla::CompileOptions compile_options;
  std::unique_ptr<xla::PjRtExecutable> executable =
      client->Compile(xla_computation, compile_options).ValueOrDie();

  // Prepare inputs.
  xla::Literal literal_x =
      xla::LiteralUtil::CreateR3<float>({{{1.0f, 1.0f, 1.0f}, {2.0f, 2.0f, 2.0f}, {3.0f, 3.0f, 3.0f}, {4.0f, 4.0f, 4.0f}},
                                        {{5.0f, 5.0f, 5.0f}, {6.0f, 6.0f, 6.0f}, {7.0f, 7.0f, 7.0f}, {8.0f, 8.0f, 8.0f}}});
  xla::Literal literal_y =
      xla::LiteralUtil::CreateR2<float>({{1.0f, 2.0f}, {3.0f, 4.0f}, {5.0f, 6.0f}});

  // xla::Literal literal_z =
  //     xla::LiteralUtil::CreateR1<float>({1.0f});
  xla::Literal literal_z =
      xla::LiteralUtil::CreateR1<float>({1.0f, 1.0f});
  // xla::Literal literal_z =
  //     xla::LiteralUtil::CreateR2<float>({{1.0f, 1.0f}, {1.0f, 1.0f}, {1.0f, 1.0f}, {1.0f, 1.0f}});
  
  std::unique_ptr<xla::PjRtBuffer> param_x =
      client->BufferFromHostLiteral(literal_x, client->addressable_devices()[0])
          .ValueOrDie();
  std::unique_ptr<xla::PjRtBuffer> param_y =
      client->BufferFromHostLiteral(literal_y, client->addressable_devices()[0])
          .ValueOrDie();
  std::unique_ptr<xla::PjRtBuffer> param_z =
      client->BufferFromHostLiteral(literal_z, client->addressable_devices()[0])
          .ValueOrDie();

  // Execute on GPU.
  xla::ExecuteOptions execute_options;
  // One vector<buffer> for each device.
  std::vector<std::vector<std::unique_ptr<xla::PjRtBuffer>>> results =
      executable->Execute({{param_x.get(), param_y.get(), param_z.get()}}, execute_options)
          .ValueOrDie();

  // Get result.
  std::shared_ptr<xla::Literal> result_literal =
      results[0][0]->ToLiteral().ValueOrDie();
  LOG(INFO) << "result = " << *result_literal;
  return 0;
}
