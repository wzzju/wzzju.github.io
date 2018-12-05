---
layout: post
title: How to add a new operation in Paddle Mobile?
date: 2018-11-28
comments: true
categories: [ "AI Framework", "Paddle Mobile" ]
---

##  1. 需要修改的文件

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

