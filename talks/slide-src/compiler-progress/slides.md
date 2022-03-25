---
# try also 'default' to start simple
theme: seriph
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: /images/background/bg.jpeg
# apply any windi css classes to the current slide
class: 'text-center'
# https://sli.dev/custom/highlighters.html
highlighter: shiki
# show line numbers in code blocks
lineNumbers: true
drawings:
  persist: false
download: true
---

# 编译器支持科学计算

## 关键技术点、支持进度与工作展望

Author

2022/03/21

---
layout: image-right
image: /images/post/science-infra.png
---

# 关键技术点

<small>

* 可无穷求导的基础算子集合确定：经`AutoGrad`处理后的Program中仅含基础算子
* 基础算子所需的元算子语义开发：在`CinnBuilder`中实现完成基础算子计算逻辑所需的元算子语义
* 基础算子OpMapper功能开发：在CINN中实现每个基础算子所需的映射逻辑
* 子图划分：对仅包含基础算子的Paddle全图进行划分，以得到CINN支持的子图
* 符号执行：通过调用每个基础算子对应的OpMapper将子图转化为CINN可识别的算子指令
* 复杂算子拆解：可选地将复杂算子指令拆解为元算子指令
* Pass优化：基于CINN Graph执行用于提升性能的Pass优化，包括<kbd>TransposeFolding</kbd>、<kbd>GemmRewriter</kbd>、<kbd>GpuTreeReductionRewriter</kbd>、<kbd>OpFusion</kbd>等
* Low-level优化：基于Compute & Schedule原语的优化
* 执行：计算图执行到`CinnLaunchOp`时，会在其内创建新`PE`用于执行每一个`CinnInstructionRunOp`

</small>

<style>
small {
  font-size: 75%;
  font-weight: 400;
  letter-spacing: 0;
}
</style>

<!--
layout: two-cols

::right::

<img src="/images/post/science-infra.png" style="height: 100%;margin-left: 30px"> -->

---

# 支持进度

## Q1关键进展
* 编译器支持Laplace模型训练功能打通
  - ☑ 与科学计算模型开发同学对齐Laplace模型所需的18个基础算子
  - ☑ 完成Laplace模型所需元算子梳理及相应CINN指令功能开发
  - ☑ 完成Laplace模型符号化转换过程中所需的OpMapper功能开发
  - ☑ 编译器支持Laplace模型训练整体功能联调，当前<font color="#48b4e0">全流程已可正常跑通</font>，但<font color="red">精度未对齐</font>
  - ☐ 编译器支持Laplace模型训练loss与未进行手工转换前的Laplace静态图模型训练loss对齐
  - ☐ 编译器支持Laplace模型训练性能优化

<style>
ul ul li {
  position: relative;
  list-style: none;
}
</style>

---

# 支持进度

## Q1关键进展

* 编译器通用Pass优化能力增强
  - ☑ **TransposeFolding**(<font color="#48b4e0">功能开发完成</font>)：将Transpose语义折叠到Dot操作，为后续使用`GEMM`重写`dot + add`做准备
  - ⬓ **GemmRewriter**(<font color="#48b4e0">功能开发接近尾声</font>)：将transpose、dot和add操作合并，并使用`cuBLAS GEMM`替换
  - ⬓ **GpuTreeReductionRewriter**(<font color="#48b4e0">功能基本开发完成，PR待合入</font>)：使用2个Reduce重写Reduce操作，以增加Reduction并行度并同时避免原子操
  - ☐ **DotMerger**(<font color="red">功能待开发</font>)：将满足一定条件的两个Dot合并为一个Dot操作
  - ☐ **AlgebraicSimplifier**(<font color="red">功能待开发</font>)：对Abs、Add、Dot、Reduce等操作进行代数化简，仅对Laplace模型中使用到的计算操作进行重点实现

<style>
ul ul li {
  position: relative;
  list-style: none;
}
</style>

---

# 支持进度

## Q1关键进展
* 编译器融合Pass功能增强与完善
  - ☑ 完成竞品算子融合功能调研，分析现有CINN融合Pass功能差距
  - ☑ 完成算子融合功能的设计方案编写，并进行设计评审
  - ⬓ 基本完成OpFunsion Pass功能开发
  - ⬓ 基本完成OpLowering代码生成功能开发
  - ☐ `FusionMerger`和`HorizontalFusion`融合功能预计4月底完成

<style>
ul ul li {
  position: relative;
  list-style: none;
}
</style>

---

# 工作展望

## Q2重点计划

* 编译器支持Laplace模型训练性能优化
  - ❐ 基于开发完成的GemmRewriter、GpuTreeReductionRewriter、OpFunsion等Pass功能，验证在Laplace模型训练性能
  - ❐ 进一步增强编译器通用Pass优化能力，完成DotMerger、AlgebraicSimplifier等Pass功能的开发
  - ❐ 进一步增强编译器算子融合能力，完成`FusionMerger`和`HorizontalFusion`等融合功能的开发
  - ❐ 探索与深挖编译器支持Laplace模型训练过程中可优化的性能瓶颈点
* 完善编译器支持科学计算所需的元算子语义
  - ❐ 新增`gather`和`scatter_add`元算子指令
* 编译器支持3d圆柱绕流模型训练
  - ❐ 待3d圆柱绕流模型就绪后进行编译器支持训练对接


<style>
ul ul li {
  position: relative;
  list-style: none;
}
</style>

---

<div class="grid grid-cols-3 gap-10 pt-4 -mb-6">

<div>
<img src='https://g.gravizo.com/svg?
digraph G {
   node_30[label="A"]
   node_33[label="C"]
   node_39[label="F"]
   node_41[label="elementwise_add_3"]
   node_38[label="matmul_2"]
   node_32[label="transpose_0"]
   node_35[label="transpose_1"]
   node_31[label="var_40"]
   node_34[label="var_42"]
   node_36[label="var_43"]
   node_37[label="var_44"]
   node_40[label="var_46"]
   node_30->node_32
   node_31->node_38
   node_32->node_31
   node_33->node_35
   node_34->node_38
   node_35->node_34
   node_36->node_41
   node_38->node_37
   node_38->node_36
   node_39->node_41
   node_41->node_40
} // end G
' style='height: 500px;margin-left: 200px'/>
</div>

<div>

<arrow x1="520" y1="300" x2="620" y2="300" color="#0085a1" width="3" arrowSize="1" />

</div>

<div>
<img src='https://g.gravizo.com/svg?
digraph G {
   node_42[label="A"]
   node_43[label="C"]
   node_44[label="F"]
   node_46[label="cublas_gemm_0"]
   node_45[label="var_46"]
   node_42->node_46
   node_43->node_46
   node_44->node_46
   node_46->node_45
} // end G
' style='height: 100%;'/>
</div>

</div>
