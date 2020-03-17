---
layout: post
title: Docker源码编译GPU版本TensorFlow
date: 2020-03-17
comments: true
categories: [ "TensorFlow" ]
---

## 1. 环境准备

* docker镜像: `paddlepaddle/paddle:latest-gpu-cuda10.0-cudnn7-dev`
* 容器创建命令：
  ```bash
  nvidia-docker run --ulimit core=-1 --privileged=true --security-opt seccomp=unconfined --name tf-wz --net=host -d -v $PWD/.ccache:/root/.ccache -v $PWD/.cache:/root/.cache -v $PWD:/work -v /ssd3/datasets:/work/dataset -it paddlepaddle/paddle:latest-gpu-cuda10.0-cudnn7-dev /bin/bash
  ```

  > 不使用`nvidia-docker`命令创建容器的方法（此文不使用，仅记录）：

  ```bash
  export CUDA_SO="$(\ls /usr/lib64/libcuda* | xargs -I{} echo '-v {}:{}') $(\ls /usr/lib64/libnvidia* | xargs -I{} echo '-v {}:{}')"
  export DEVICES=$(\ls /dev/nvidia* | xargs -I{} echo '--device {}:{}')

  sudo /usr/bin/docker run ${CUDA_SO} ${DEVICES} --ulimit core=-1 --privileged=true --security-opt seccomp=unconfined --name tf-wz --net=host -d -v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi -v $PWD/.ccache:/root/.ccache -v $PWD/.cache:/root/.cache -v $PWD:/work -it paddlepaddle/paddle:latest-gpu-cuda10.0-cudnn7-dev /bin/bash
  # 进入容器再设置一下环境变量：export LD_LIBRARY_PATH=/usr/lib64:/usr/local/lib:$LD_LIBRARY_PATH
  ```


* 进入docker命令：`nvidia-docker exec -it tf-wz /bin/bash`


> 注意以下操作均在容器内完成。

## 2. 获取TensorFlow源码

```bash
git clone  https://github.com/tensorflow/tensorflow.git
# 切换到r1.14分支

git fetch origin r1.14:study_r1.14
git checkout study_r1.14
```

## 3. 安装bazel-0.24.1(对应于tf r1.14)

```bash
# https://github.com/bazelbuild/bazel/releases
wget https://github.com/bazelbuild/bazel/releases/download/0.24.1/bazel-0.24.1-installer-linux-x86_64.sh
chmod +x bazel-0.24.1-installer-linux-x86_64.sh
./bazel-0.24.1-installer-linux-x86_64.sh --user
```

## 4. 编译TensorFlow

* 安装python3-dbg（python的debuginfo包）

  ```bash
  apt install python3-dbg
  ```

* 创建虚环境

  ```bash
  mkvirtualenv --python=python3.7 tf-study
  # workon tf-study
  ```

  > virtualenv的安装及使用方法参考[此处](https://codingpy.com/article/virtualenv-must-have-tool-for-python-development/)。

* 安装TensorFlow编译依赖包（python包）

  ```bash
  pip install -U pip six numpy wheel setuptools mock 'future>=0.17.1'
  pip install -U keras_applications --no-deps
  pip install -U keras_preprocessing --no-deps
  ```

* 进行编译选项配置

  ```bash
  export PATH=/root/bin:$PATH
  ./configure
  # 根据提示进行配置，主要是遇到“是否编译cuda时”选择“y”，其他默认选择即可。
  ```

* 执行编译

  参考[此文](http://jcf94.com/2018/01/13/2018-01-13-tfunpacking/)，为了编译带调试信息的TensorFlow，需要执行如下编译命令：

  ```bash
  bazel build -c opt --config=cuda --copt="-g" --cxxopt="-g" //tensorflow/tools/pip_package:build_pip_package
  ```

## 5. 构建`whl`软件包

```bash
./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
```

## 6. 安装`whl`软件包

```bash
pip install -U /tmp/tensorflow_pkg/tensorflow-*.whl
```

## 7. gdb调试python代码方法

在要调的 python 代码前面加上如下一段代码，用于获取待调试的python脚本进程号，点击查看[示例](/assets/tensorflow/test_debug.py)。

```python
import os
PID = os.getpid()
print('Program pid:', PID)
print('Pause here to enter DBG')
os.system("read _")
```

接着执行`gdb -p PID`即可进行调试。为了可以使用`py-list`之类的python调试指令，进入gdb模式后，需要执行如下代码：

```python
(gdb) python
>import sys
# "/Python-3.7.0/Tools/gdb/libpython.py"
>sys.path.append('/Python-3.7.0/Tools/gdb')
>import libpython
>end
(gdb) ...
```

为了方便起见，可以选择将[libpython.py](/assets/tensorflow/libpython.py)文件拷贝到tensorflow源码根目录下，然后执行如下命令完成python调试指令的加载（请在tensorflow源码根目录下执行gdb调试命令）:

```python
(gdb) python
>import sys
>sys.path.append('.')
>import libpython
>end
(gdb) ...
```


`os.system("read _")`相当于人为地打了一处断点，设置完python调试命令后，在gdb模式中输入`c`指令（可在输入`c`指令前设置一些C/C++文件中的断点，如`break TF_NewBuffer`），然后再在python脚本运行窗口中按Enter键即可让python程序继续运行。

#### gdb调试时注意事项：

* 运行python脚本不能在tensorflow源码根目录下，否则会出错。但是需要在tensorflow源码根目录下存放一个对应的软连接文件(`ln -s python脚本文件 tensorflow/python脚本文件`)，以便使用`py-list`时可以查看脚本源码内容。
* 执行`gdb -p PID`命令最佳方案：**在tensorflow源码根目录下运行gdb**。否则，需要在gdb模式下使用`set substitute-path`指令修改源码搜索路径，详见[此处](https://scc.ustc.edu.cn/zlsc/sugon/intel/debugger/cl/commandref/gdb_mode/cmd_set_substitu.htm)。
* TensorFlow的gdb调试方法详见[此文档](/assets/tensorflow/TensorFlow-SourceCode-Reading.pdf)[^1]。

## 8. docker容器中的一些配置文件

#### 8.1 apt软件包中国源(`/etc/apt/sources.list`的内容)

```bash
deb-src http://archive.ubuntu.com/ubuntu xenial main restricted #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
deb http://archive.canonical.com/ubuntu xenial partner
deb-src http://archive.canonical.com/ubuntu xenial partner
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse
```

#### 8.2 pip中国源(`~/.pip/pip.conf`内容)

```bash
[global]
trusted-host = mirrors.aliyun.com
index-url = https://mirrors.aliyun.com/pypi/simple
```

## 9. Q&A

* Q: 运行`build_pip_package`命令时出现`OverflowError: Size does not fit in an unsigned int`错误。
  A: 需要使用python3.7+进行打包。操作命令如下：

  ```bash
  which python3.7 # /usr/local/bin/python3.7
  # 编辑tools/python_bin_path.sh，将其内容修改为：
  # export PYTHON_BIN_PATH="/usr/local/bin/python3.7"
  ```
  然后再执行打包命令：
  ```python
  ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
  # 这样得到的结果为：tensorflow-1.14.1-cp37-cp37m-linux_x86_64.whl
  ```
  然而这样打包得到的`whl`包只能在python3.7环境中进行安装，所以编译时使用python3.7是最好的选择。

## 参考资料

* [Python开发必备神器之一：virtualenv](https://codingpy.com/article/virtualenv-must-have-tool-for-python-development/)
* [TensorFlow 拆包（一）：Session.Run ()](http://jcf94.com/2018/01/13/2018-01-13-tfunpacking/)

[^1]: 文档来源于[TensorFlow代码阅读指南](http://jcf94.com/download/TensorFlow-SourceCode-Reading.pdf)。
