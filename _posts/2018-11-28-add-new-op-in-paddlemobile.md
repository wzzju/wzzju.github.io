---
layout: post
title: paddle-mobile之添加新Op
date: 2018-11-28
comments: true
categories: [ "AI Framework", "Paddle Mobile" ]
---

#### 需要修改的文件

在paddle-mobile中添加一个新Op并非一件复杂的事情，仅需依次修改如下文件内容：

```bash
tools/op.cmake --> 
src/operators/op_param.h --> 
src/common/types.h --> 
src/common/types.cpp --> 
src/operators/kernel/sum_kernel.h(新增)  -->  
src/operators/kernel/arm/sum_kernel.cpp(新增) --> 
src/operators/kernel/central-arm-func/sum_arm_func.h(新增)  -->  
src/operators/sum_op.h(新增) --> 
src/operators/sum_op.cpp(新增) -->
test/operators/test_sum_op.cpp(新增) -->
test/CMakeLists.txt
```

1. 详细文件修改内容请参考[SumOp的实现](https://github.com/PaddlePaddle/paddle-mobile/pull/1122/files)。
2. `test_sum_op.cpp`文件中Op单测的写法并不正规，请参考[test_mul_op.cpp](https://github.com/PaddlePaddle/paddle-mobile/blob/develop/test/operators/test_mul_op.cpp)文件编写Op UT。
