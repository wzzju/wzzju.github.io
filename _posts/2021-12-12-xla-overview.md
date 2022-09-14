---
layout: post
title: XLA功能原理分析
date: 2021-12-12
comments: true
toc: true
mathjax: false
categories: [ "TensorFlow", "XLA" ]
---

> **特别声明：未经授权，禁止转载。** <br>
> 本文所使用的TensorFlow代码库commit id为f270180a6caa8693f2b2888ac7e6b8e69c4feaa8（r2.1分支）。

# XLA功能概览

* **tensorflow/compiler/aot**
	- AOT方式使用XLA，通过`tfcompile`命令实现[^1]。
* **tensorflow/compiler/jit**
	-  JIT方式使用XLA，通过设置`tf.ConfigProto().graph_options.optimizer_options.global_jit_level = tf.OptimizerOptions.ON_1`或者使用`xla.compile`接口实现。
	- 三个算子：`XlaCompileOp`、`XlaRunOp`和`XlaMergeOp`，其中`XlaCompileOp`通过tf2xla完成**编译**功能，`XlaRunOp`通过xla/client完成**运行**功能。
	- 11个优化pass：`BuildXlaOpsPass`、`CloneConstantsForBetterClusteringPass`、`ClusterScopingPass`、`EncapsulateSubgraphsPass`、`EncapsulateXlaComputationsPass`、`IncreaseDynamismForAutoJitPass`、`IntroduceFloatingPointJitterPass`、`MarkForCompilationPass`、`PartiallyDeclusterPass`、`ReportClusteringInfoPass`、`FunctionalizeControlFlowForXlaPass`。
* **tensorflow/compiler/tf2xla**
	- 提供`XlaCompiler::CompileFunction`(xla\_compiler.cc)接口，用于将适合被JIT编译的计算图区域（cluster）转化为`XlaComputation`。其核心是通过调用`XlaCompiler::CompileGraph`接口使用`ExecuteGraph`函数完成XlaOpKernel的符号执行[^2]。
	- 符号执行时会调用每个`XlaOpKernel`子类的Compute函数，进而调用其Compile成员函数。Compile函数的功能描述如下：
		+  从`XlaOpKernelContext`中取出`XlaExpression`或`XlaOp`，调用`xla/client/xla_builder.h`提供的方法执行计算(编译), 最后将完成计算的最终`XlaOp`存入`XlaKernelContext`中作为输出。
* **tensorflow/compiler/xla/client** 
	- 提供`xla::XlaBuilder`功能以及预定义的XLA元算子(xla\_builder.cc)，供`XlaCompiler::CompileFunction`使用，即将由Op表达的Graph转化为HloModuleProto表达并将其保存在`XlaComputation`中。
	- 提供`LocalClient::Compile`(local\_client.cc)接口，并将其作为JIT编译的入口，供`XlaCompilationCache::BuildExecutable`接口(xla_compilation_cache.cc)使用。`LocalClient::Compile`接口将已经得到的`XlaComputation`交给`LocalService::CompileExecutable`（locla\_service.cc）进行编译以得到二进制（`LocalService::CompileExecutable`会进一步调用`BuildExecutable`接口）。
	- 提供`LocalExecutable::Run`接口(local\_client.cc)，作为运行入口供`XlaRunOp`(xla_ops.cc)使用，通过Key找到相应的二进制交给service层处理(`GpuExecutable`/`CpuExecutable`)。 
* **tensorflow/compiler/xla/service**
	-  提供`Service::BuildExecutable`（service.cc）功能，供 `LocalClient::Compile`使用以实现真正的编译。具体编译过程描述如下：
		+ `BuildExecutable`将`XlaComputation`封装的HloModuleProto转化为HloModule表达，并对其进行优化。
		+ 接着将HloModule转为`llvm::Module`，并调用`CpuCompiler::RunBackend`(cpu\_compiler.cc)或`GpuCompiler::RunBackend`(gpu\_compiler.cc)将其编译为相应平台的Executable二进制。
	- 提供`Executable::ExecuteOnStream`(executable.cc)，其为`LocalExecutable::Run`接口提供了真正的二进制执行实现。
* **tensorflow/compiler/mlir**
	- 提供tf、tflite以及xla使用的mlir方言和相关工具
* **tensorflow/compiler/xrt**
	- XRT是一个同时支持多个计算引擎的运行时加速库，目前已经集成了TensorFlow XLA和Nvidia TensorRT两个后端引擎。其中XLA全面支持训练和预测，TensorRT支持预测以及部分算子支持训练。对于同一个计算图，XRT允许多个计算引擎联合使用，以获得更好的加速效果。

# XLA完整执行流程分析
## 示例代码
```python
# scope_xla.py
import numpy as np
from tensorflow.python.client import timeline
from tensorflow.python.compiler.xla import jit
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

def nn_block(input_tensor_0):
    op_0_0 = tf.square(input_tensor_0)
    op_1_1 = tf.matmul(op_0_0, op_0_0)
    op_1_0 = tf.subtract(op_1_1, op_1_1)
    op_2_0 = tf.add(op_1_0, op_1_1)
    return op_2_0

def nn(input_tensor_0):
    for i in range(0, 1):
        tmp = input_tensor_0
        input_tensor_0 = nn_block(tmp)
    return input_tensor_0

def test_scope():
  x = tf.placeholder(tf.float32, [None, 2])
  with jit.experimental_jit_scope(compile_ops=True):
    output = nn(x)

  run_metadata = tf.RunMetadata()
  with tf.Session() as sess:
    tf.global_variables_initializer().run(session=sess)

    data = np.array([[1, 2],
                     [3, 4]])
    # data = np.random.rand(2, 2).astype('float32')
    res = sess.run(output,
             feed_dict={x: data},
             options=tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE),
             run_metadata=run_metadata)
    print(res)

    trace = timeline.Timeline(step_stats=run_metadata.step_stats)
    with open('./timeline.ctf.json', 'w') as trace_file:
      trace_file.write(trace.generate_chrome_trace_format())

if __name__ == '__main__':
  test_scope()
```

* 执行脚本如下：

```shell
#!/usr/bin/env bash
set -ex

CUDA_VISIBLE_DEVICES=0                                                                                                                        \
TF_CPP_MIN_LOG_LEVEL=0                                                                                                                        \
TF_CPP_VMODULE=cuda_driver=2                                                                                                                  \
TF_DUMP_GRAPH_PREFIX="./graph_dump_path"                                                                                                      \
TF_XLA_FLAGS="--tf_xla_clustering_debug"                                                                                                      \
XLA_FLAGS="--xla_dump_to=./xla_scope_output --xla_dump_hlo_pass_re=.* --xla_dump_hlo_as_text --xla_dump_hlo_as_html --xla_dump_hlo_snapshots" \
python -u scope_xla.py
```

## 执行流程梳理
* **Xla cluster子图构建流程**
![xla-overview](/images/posts/xla/xla-overview.png)
* **XlaCompile执行流程**
![xla-compile](/images/posts/xla/xla-compile.png)

* **XlaRun执行流程**
![xla-run](/images/posts/xla/xla-run.png)

# XLA中使用NVTX

* 修改[tensorflow/core/profiler/internal/gpu/nvtx_utils.h](https://github.com/tensorflow/tensorflow/blob/2a44ee90/tensorflow/core/profiler/backends/gpu/nvtx_utils.h#L53)文件，在` NVTXRangeTracker`类定义下方添加如下内容：

```cpp
class RecordEvent {
 public:
  RecordEvent(const std::string& name);
  ~RecordEvent();
};

void ProfilerRangePush(const std::string& name);

void ProfilerRangePop();
```

* 修改[tensorflow/core/profiler/internal/gpu/nvtx_utils.cc](https://github.com/tensorflow/tensorflow/blob/2a44ee90/tensorflow/core/profiler/backends/gpu/nvtx_utils.cc#L27)文件，添加如下内容：

```cpp
RecordEvent::RecordEvent(const std::string& name) {
  nvtxRangePushA(name.c_str());
}

RecordEvent::~RecordEvent() {
  nvtxRangePop();
}

void ProfilerRangePush(const std::string& name) {
  nvtxRangePushA(name.c_str());
}

void ProfilerRangePop() {
  nvtxRangePop();
}
```

* 在需要使用nvtx打tag的源码中引入头文件`tensorflow/core/profiler/internal/gpu/nvtx_utils.h`，如下所示：
  
```cpp
#include "tensorflow/core/profiler/internal/gpu/nvtx_utils.h"

// method 1
{
  // ...
  tensorflow::profiler::RecordEvent pass_enevt("RunHloPasses");
  // ...
}

// method 2
tensorflow::profiler::ProfilerRangePush("RunBackend");
// ...
tensorflow::profiler::ProfilerRangePop();
```

* 在源码中引入nvtx打tag功能后，需要更改对应源码编译所需的BUILD文件，在其中加入`//tensorflow/core/profiler/lib:profiler_backends`编译依赖。举例说明如下：
  - 在[tensorflow/compiler/xla/python/jax_jit.cc](https://github.com/tensorflow/tensorflow/blob/2a44ee90/tensorflow/compiler/xla/python/jax_jit.cc)中使用nvtx打tag后，需要在[tensorflow/compiler/xla/python/BUILD](https://github.com/tensorflow/tensorflow/blob/2a44ee90/tensorflow/compiler/xla/python/BUILD#L381)文件内容`cc_library(name = "jax_jit", srcs = ["jax_jit.cc"], ..., deps = [...])`的deps域中添加一行`"//tensorflow/core/profiler/lib:profiler_backends",`编译依赖。

# XLA Client元算子

以下列举的XLA Client元算子类型来源于[tensorflow/compiler/xla/client/xla_builder.h](https://github.com/tensorflow/tensorflow/blob/r2.1/tensorflow/compiler/xla/client/xla_builder.h)。

```shell
'Abs',
'Add',
'AfterAll',
'AllReduce',
'AllToAll',
'And',
'Atan2',
'BatchNormGrad',
'BatchNormInference',
'BatchNormTraining',
'BitcastConvertType',
'Broadcast',
'BroadcastInDim',
'Call',
'Ceil',
'Cholesky',
'Clamp',
'Clz',
'Collapse',
'CollectivePermute',
'Compare',
'Complex',
'ConcatInDim',
'Conditional',
'Conj',
'ConstantFromArray',
'ConstantFromArrayWithLayout',
'ConstantLiteral',
'ConstantR0',
'ConstantR1',
'ConstantR2',
'ConstantR2FromArray2D',
'ConstantR2FromArray2DWithLayout',
'ConstantR3FromArray3D',
'ConstantR3FromArray3DWithLayout',
'ConstantR4FromArray4D',
'ConstantR4FromArray4DWithLayout',
'Conv',
'ConvGeneral',
'ConvGeneralDilated',
'ConvWithGeneralDimensions',
'ConvWithGeneralPadding',
'ConvertElementType',
'Cos',
'CreateToken',
'CrossReplicaSum',
'CustomCall',
'CustomCallWithLayout',
'Div',
'Dot',
'DotGeneral',
'DynamicSlice',
'DynamicUpdateSlice',
'Eq',
'Exp',
'Expm1',
'Fft',
'Floor',
'Gather',
'Ge',
'GetDimensionSize',
'GetTupleElement',
'Gt',
'Imag',
'Infeed',
'InfeedWithToken',
'Iota',
'IsFinite',
'Le',
'Log',
'Log1p',
'Lt',
'Map',
'Max',
'Min',
'Mul',
'Ne',
'Neg',
'Not',
'Or',
'OutfeedWithToken',
'Pad',
'Parameter',
'PopulationCount',
'Pow',
'Real',
'Recv',
'RecvFromHost',
'RecvWithToken',
'Reduce',
'ReduceAll',
'ReducePrecision',
'ReduceWindow',
'ReduceWindowWithGeneralPadding',
'Rem',
'ReplicaId',
'Reshape',
'ReshapeWithInferredDimension',
'Rev',
'RngNormal',
'RngUniform',
'Round',
'Rsqrt',
'Scatter',
'Select',
'SelectAndScatter',
'SelectAndScatterWithGeneralPadding',
'SendToHost',
'SendWithToken',
'SetDimensionSize',
'ShiftLeft',
'ShiftRightArithmetic',
'ShiftRightLogical',
'Sign',
'Sin',
'Slice',
'SliceInDim',
'Sort',
'Sqrt',
'Sub',
'Tanh',
'Transpose',
'TriangularSolve',
'Tuple',
'While',
'Xor'
```

[^1]: [tensorflow xla tfcompile命令和interactive_graphviz工具](https://zhuanlan.zhihu.com/p/71245637)

[^2]: [tensorflow xla 符号执行](https://zhuanlan.zhihu.com/p/71488578)

# 参考资料

* [Tensorflow JIT/XLA UML](https://sketch2sky.com/2019/09/22/tensorflow-jit-xla-uml/)
* [TensorFlow XLA工作原理](https://zhuanlan.zhihu.com/p/98565435)