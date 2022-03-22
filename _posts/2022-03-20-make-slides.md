---
layout: keynote
title: "使用slidev创建幻灯片"
subtitle: "基于markdown编写幻灯片"
date: 2022-03-20
iframe: "/talks/slide-template/"
comments: true
toc: true
mathjax: false
categories: [ "Slides", "Slidev" ]
---

## 1. slidev安装与项目初始化

> slidev requires `Node.js >= 14.0`

* 创建幻灯片工程目录`slides-project`，并在该目录下安装`slidev`，然后进行项目初始化

```shell
# 为了方便统一文件管理，建议将slides-project目录创建在wzzju.github.io项目根目录下，
# 并将slides-project加入到.gitignore中以及_config.yml文件内容的exclude属性值中

mkdir -p slides-project && cd slides-project

# 安装并初始化slidev项目
npm init slidev@latest
# 1）输入项目名称，如slide-template
# 2）按Enter键选择yes，继续
# 3）agent选择npm，直接按Enter键即可
```
* 执行完上述命令后，`slidev`会在本地`3030`端口上启动服务，使用浏览器访问`http://localhost:3030/`即可进行预览
* 接下来我们只需要编辑`slide-template`目录下的`slides.md`文件即可制作幻灯片

### 1.1 图片资源显示

若要显示自定义的幻灯片背景图、内容图等文件资源，需在slidev项目根目录下创建`public`文件夹。示例如下：
```shell
# 进入slidev项目根目录
cd slides-project/slide-template
# 创建public文件夹
mkdir -p public
# 之后，将需要显示的自定义图片等文件放到public目录下即可
```

若幻灯片中使用到`public/images/background/bg.jpeg`文件，则只需要书写`/images/background/bg.jpeg`路径即可。

> 在使用`npx slidev build --base /talks/slide-template/`命令进行编译部署时，`public`目录下的全部文件会被自动拷贝到`dist`目录中。

## 2. 启动已经存在的slidev项目

* 使用`npx slidev`命令可以启动已经存在的slidev项目，示例如下：
```shell
# 进入上面已创建的slidev项目目录
cd slides-project/slide-template
# 重新启动slidev项目
npx slidev
```

## 3. slidev项目部署
* 使用如下命令可将slidev项目编译成`Single Page Application (SPA)`，其中将base路径设置为`/talks/slidev项目名`，示例如下
```shell
npx slidev build --base /talks/slide-template/
# 编译生成的结果位于slide-template项目路径下的dist目录中，
# 该编译产物可部署在GitHub Pages上
```
* 将整个dist目录拷贝到`wzzju.github.io/talks/`目录下，并将其重命名为`slidev项目名`(务必保证和上一步使用的base路径中`/talks/`后面的路径名称相同)，示例如下：
```shell
cp -r dist ~/Study/Blog/wzzju.github.io/talks/slide-template
```
* 建议将slidev项目根目录下的`slides.md`和`public`文件夹备份到`wzzju.github.io/talks/slide-src/`目录下，示例如下：
```shell
cd wzzju.github.io/talks/slide-src
mkdir -p ${slidev项目名}
cp ${slidev项目路径}/slides.md wzzju.github.io/talks/slide-src/${slidev项目名}/
cp -r ${slidev项目路径}/public wzzju.github.io/talks/slide-src/${slidev项目名}/
```

> **因为slidev项目的build产物比较多且大，不利于jekyll页面的生成，建议一直复用`slide-template`项目，而每次只将`slides.md`和`public`文件夹备份到`talks/slide-src`目录下。后续，按需根据`markdown源码文件`和`public资源目录`构建相应幻灯片并用其替换`talks/slide-template`目录下的文件。**

### 3.1 提供PDF格式下载
在将slidev项目编译成`SPA`时，可以选择提供PDF格式文件下载，这只需要在首页格式配置中添加如下语句：
```shell
---
download: true
---
```

然后，使用如下命令安装渲染PDF所需的软件包：
```shell
npm i -D playwright-chromium
npx playwright install
```

最后，执行`npx slidev build --base /talks/slide-template/`命令。这会在生成`SPA`网页的同时，也会将幻灯片渲染为pdf格式文件，并在`SPA`页面中提供下载按钮。

### 3.2 单独导出PDF文件

* 安装`playwright-chromium`：
```shell
npm i -D playwright-chromium
```
* 导出pdf格式幻灯片：
```shell
npx slidev export
```
* 默认导出pdf文件时，会禁用动画效果，如果需要将美步点击都生成一页文档，可以使用如下命令：
```shell
# slidev >= v0.21
npx slidev export --with-clicks
```

## 4. 快捷键功能

* `f`：切换全屏
* `right / space`：下一动画或幻灯片
* `left / shift space`：上一动画或幻灯片
* `up`：上一张幻灯片
* `down`：下一张幻灯片
* `o`：切换幻灯片总览
* `d`：切换暗黑模式
* `g`：显示`前往...`

## 参考资料

* [使用Markdown制作PPT](https://mp.weixin.qq.com/s/W7QeS0csw0my0eig1qPI9w)
* [Slidev Installation](https://sli.dev/guide/install.html)
* [Slidev Static Hosting](https://sli.dev/guide/hosting.html)
* [Slidev Directory Structure](https://sli.dev/custom/directory-structure.html#public)
* [Slidev Exporting PDF](https://sli.dev/guide/exporting.html#pdf)
