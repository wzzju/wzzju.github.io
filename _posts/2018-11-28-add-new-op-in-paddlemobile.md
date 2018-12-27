---
layout: post
title: 如何在paddle-mobile中添加一个新的Op？
date: 2018-11-28
comments: true
categories: [ "AI Framework", "Paddle Mobile" ]
---

## 需要修改的文件

依次修改如下文件内容：

```bash
tools/op.cmake --> 
src/operators/op_param.h --> 
src/common/types.h --> 
src/common/types.cpp --> 
src/operators/kernel/conv_add_relu_int8_kernel.h(新增)  -->  
src/operators/kernel/arm/conv_add_relu_int8_kernel.cpp(新增) --> 
src/operators/kernel/central-arm-func/conv_add_relu_int8_arm_func.h(新增)  -->  
src/operators/fusion_conv_add_relu_int8_op.h(新增) --> 
src/operators/fusion_conv_add_relu_int8_op.cpp(新增) -->
test/operators/test_fusion_conv_add_relu_int8_op.cpp(新增) -->
test/CMakeLists.txt
```

详细文件修改内容请参考[FusionFcInt8Op的实现](https://github.com/PaddlePaddle/paddle-mobile/pull/1336/files).
