---
layout: post
title: Paddle框架Op注册机制
date: 2020-07-13
comments: true
categories: [ "Framework" ]
---

## 宏展开调试技巧[^1]

宏代码会在编译前全部展开，因此可以使用编译器（gcc）输出预处理结果。

* `gcc -E`让编译器在预处理结束后停止，不进行后续的编译及链接操作。
* `gcc -P`屏蔽编译器输出预处理结果的行标记 (如`#line lineno "filename"`)，减少干扰。
* 由于输出结果没有格式化，可先传给`clang-format --style=Google`格式化后再输出。
* 屏蔽无关的头文件，临时删掉不影响宏展开的`#include`行，避免多余的引用展开，导致实际关注的宏代码 “被淹没”。

## Paddle `fsp_op` Op注册宏展开示例

* 使用`cd /work/Paddle`命令进入Paddle源码根目录。
* 删除`paddle/fluid/operators/fsp_op.cc`文件中的所有`#include`行，并添加`#include "paddle/fluid/framework/op_registry.h"`语句。
* 删除`paddle/fluid/framework/op_registry.h`文件中的所有`#include`行。
* 执行如下命令进行宏展开（为了将CUDA Op Kernel注册宏也展开，可将`paddle/fluid/operators/fsp_op.cu`中的cuda kernel注册语句也拷贝到`fsp_op.cc`文件中）。

```shell
gcc -E -P paddle/fluid/operators/fsp_op.cc -I. | clang-format --style=Google >./macro.cpp

```

#### Paddle `fsp_op`算子注册方式的宏展开代码

```cpp
namespace ops = paddle::operators;
namespace plat = paddle::platform;
struct __test_global_namespace___reg_op__fsp__ {};
static_assert(std::is_same<::__test_global_namespace___reg_op__fsp__,
                           __test_global_namespace___reg_op__fsp__>::value,
              "REGISTER_OPERATOR must be called in global namespace");
static ::paddle::framework::OperatorRegistrar<
    ops::FSPOp, ops::FSPOpMaker, ops::FSPGradOpMaker<paddle::framework::OpDesc>,
    ops::FSPGradOpMaker<paddle::imperative::OpBase>>
    __op_registrar_fsp__("fsp");
int TouchOpRegistrar_fsp() {
  __op_registrar_fsp__.Touch();
  return 0;
};
struct __test_global_namespace___reg_op_kernel_fsp_CPU_DEFAULT_TYPE____ {};
static_assert(
    std::is_same<
        ::__test_global_namespace___reg_op_kernel_fsp_CPU_DEFAULT_TYPE____,
        __test_global_namespace___reg_op_kernel_fsp_CPU_DEFAULT_TYPE____>::
        value,
    "REGISTER_OP_KERNEL must be called in "
    "global namespace");
static ::paddle::framework::OpKernelRegistrar<
    ::paddle::platform::CPUPlace,
    ops::FSPOpKernel<paddle::platform::CPUDeviceContext, float>,
    ops::FSPOpKernel<paddle::platform::CPUDeviceContext, double>>
    __op_kernel_registrar_fsp_CPU_DEFAULT_TYPE__(
        "fsp", "CPU",
        ::paddle::framework::OpKernelType::kDefaultCustomizedTypeValue);
int TouchOpKernelRegistrar_fsp_CPU_DEFAULT_TYPE() {
  __op_kernel_registrar_fsp_CPU_DEFAULT_TYPE__.Touch();
  return 0;
};
struct __test_global_namespace___reg_op_kernel_fsp_CUDA_DEFAULT_TYPE____ {};
static_assert(
    std::is_same<
        ::__test_global_namespace___reg_op_kernel_fsp_CUDA_DEFAULT_TYPE____,
        __test_global_namespace___reg_op_kernel_fsp_CUDA_DEFAULT_TYPE____>::
        value,
    "REGISTER_OP_KERNEL must be called in "
    "global namespace");
static ::paddle::framework::OpKernelRegistrar<
    ::paddle::platform::CUDAPlace,
    ops::FSPOpKernel<plat::CUDADeviceContext, float>,
    ops::FSPOpKernel<plat::CUDADeviceContext, double>>
    __op_kernel_registrar_fsp_CUDA_DEFAULT_TYPE__(
        "fsp", "CUDA",
        ::paddle::framework::OpKernelType::kDefaultCustomizedTypeValue);
int TouchOpKernelRegistrar_fsp_CUDA_DEFAULT_TYPE() {
  __op_kernel_registrar_fsp_CUDA_DEFAULT_TYPE__.Touch();
  return 0;
};
struct __test_global_namespace___reg_op__fsp_grad__ {};
static_assert(std::is_same<::__test_global_namespace___reg_op__fsp_grad__,
                           __test_global_namespace___reg_op__fsp_grad__>::value,
              "REGISTER_OPERATOR must be called in global namespace");
static ::paddle::framework::OperatorRegistrar<ops::FSPOpGrad>
    __op_registrar_fsp_grad__("fsp_grad");
int TouchOpRegistrar_fsp_grad() {
  __op_registrar_fsp_grad__.Touch();
  return 0;
};
struct __test_global_namespace___reg_op_kernel_fsp_grad_CPU_DEFAULT_TYPE____ {};
static_assert(
    std::is_same<
        ::__test_global_namespace___reg_op_kernel_fsp_grad_CPU_DEFAULT_TYPE____,
        __test_global_namespace___reg_op_kernel_fsp_grad_CPU_DEFAULT_TYPE____>::
        value,
    "REGISTER_OP_KERNEL must be called in "
    "global namespace");
static ::paddle::framework::OpKernelRegistrar<
    ::paddle::platform::CPUPlace,
    ops::FSPGradOpKernel<paddle::platform::CPUDeviceContext, float>,
    ops::FSPGradOpKernel<paddle::platform::CPUDeviceContext, double>>
    __op_kernel_registrar_fsp_grad_CPU_DEFAULT_TYPE__(
        "fsp_grad", "CPU",
        ::paddle::framework::OpKernelType::kDefaultCustomizedTypeValue);
int TouchOpKernelRegistrar_fsp_grad_CPU_DEFAULT_TYPE() {
  __op_kernel_registrar_fsp_grad_CPU_DEFAULT_TYPE__.Touch();
  return 0;
};
struct __test_global_namespace___reg_op_kernel_fsp_grad_CUDA_DEFAULT_TYPE____ {
};
static_assert(
    std::is_same<
        ::__test_global_namespace___reg_op_kernel_fsp_grad_CUDA_DEFAULT_TYPE____,
        __test_global_namespace___reg_op_kernel_fsp_grad_CUDA_DEFAULT_TYPE____>::
        value,
    "REGISTER_OP_KERNEL must be called in "
    "global namespace");
static ::paddle::framework::OpKernelRegistrar<
    ::paddle::platform::CUDAPlace,
    ops::FSPGradOpKernel<plat::CUDADeviceContext, float>,
    ops::FSPGradOpKernel<plat::CUDADeviceContext, double>>
    __op_kernel_registrar_fsp_grad_CUDA_DEFAULT_TYPE__(
        "fsp_grad", "CUDA",
        ::paddle::framework::OpKernelType::kDefaultCustomizedTypeValue);
int TouchOpKernelRegistrar_fsp_grad_CUDA_DEFAULT_TYPE() {
  __op_kernel_registrar_fsp_grad_CUDA_DEFAULT_TYPE__.Touch();
  return 0;
};
```



[^1]: [C/C++ 宏编程的艺术](https://bot-man-jl.github.io/articles/?post=2020/Macro-Programming-Art#%E5%A6%82%E4%BD%95%E8%B0%83%E8%AF%95)。