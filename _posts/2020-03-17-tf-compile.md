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

### 7.1 设置python脚本启动断点

在要调的 python 代码前面加上如下一段代码，用于获取待调试的python脚本进程号并暂停脚本运行，点击查看[示例](/assets/tensorflow/test_debug.py)。

```python
import os
PID = os.getpid()
print('Program pid:', PID)
print('Pause here to enter DBG')
os.system("read _")
```

接着执行`gdb -p PID`即可进行调试。


> `os.system("read _")`相当于人为地打了一处断点，设置完python调试命令后，在gdb模式中输入`c`指令（可在输入`c`指令前设置一些C/C++文件中的断点，如`break TF_NewBuffer`），然后再在python脚本运行窗口中按Enter键即可让python程序继续运行。

### 7.2 加载python调试指令

* 方法一：

为了可以使用`py-list`之类的python调试指令，进入gdb模式后，需要执行如下代码：

```python
(gdb) python
>import sys
# "/Python-3.7.0/Tools/gdb/libpython.py"
>sys.path.append('/Python-3.7.0/Tools/gdb')
>import libpython
>end
(gdb) ...
```

* 方法二：

为了方便起见，可以选择将[libpython.py](/assets/tensorflow/libpython.py)文件拷贝到gdb命令执行时所在的目录下，然后执行如下命令完成python调试指令的加载:

```python
(gdb) python
>import sys
>sys.path.append('.')
>import libpython
>end
(gdb) ...
```

* 方法三：

为了省略每次运行gdb后都需要进行python调试指令的加载，可以在HOME目录下添加`.gdbinit`配置文件，内容如下所示：

```python
# 加载python调试指令
python
import sys
sys.path.append('/Python-3.7.0/Tools/gdb')
import libpython
end
# 保存历史命令
set history filename ~/.gdb_history
set history save on
```

这样每次运行gdb时，即可自动加载python调试指令。

* 方法四（推荐）：

为了最大化减少gdb启动后运行的设置命令数，可以在gdb命令执行时所处目录（一般为用户工程项目路径）下新建`.gdbinit`配置文件，并将[libpython.py](/assets/tensorflow/libpython.py)放置在同一目录下，最后设置`.gdbinit`文件为如下内容:

```python
# 加载python调试指令
python
import sys
sys.path.insert(0, ".")
import libpython
end

# 设置tensorflow源码目录，以便查找代码
set directories /work/study/tf-learn/tensorflow/
```

设置上述gdb初始化配置文件后运行gdb命令时会出现如下类似警告（此时亦可发现当前目录下的`.gdbinit`文件配置命令并没有执行）:

```
warning: File "/work/study/tf-learn/tf-test/.gdbinit" auto-loading has been declined by your `auto-load safe-path' set to "$debugdir:$datadir/auto-load".
To enable execution of this file add
        add-auto-load-safe-path /work/study/tf-learn/tf-test/.gdbinit
line to your configuration file "/root/.gdbinit".
To completely disable this security protection add
        set auto-load safe-path /
line to your configuration file "/root/.gdbinit".
```

根据警告提示，需要在HOME目录下也新建一个`.gdbinit`配置文件，其内容如下所示：

```python
# 保存历史命令
set history filename ~/.gdb_history
set history save on
# 自动加载任意目录下的.gdbinit文件配置内容
set auto-load safe-path /
```

### 7.3 gdb调试时注意事项：

* 运行python脚本不能在tensorflow源码根目录下，否则会出错。但是需要在tensorflow源码根目录下存放一个对应的软连接文件(`ln -s python脚本文件 tensorflow/python脚本文件`)，以便使用`py-list`时可以查看脚本源码内容。
* 执行`gdb -p PID`命令最佳方案：**在tensorflow源码根目录下运行gdb**。否则，需要在gdb模式下使用`set directories /work/study/tf-learn/tensorflow/`指令设置tensorflow源码根目录路径。
* TensorFlow的gdb调试方法详见[此文档](/assets/tensorflow/TensorFlow-SourceCode-Reading.pdf)[^1]。
* 给类成员函数设置断点的方法：
    - 需要加上命名空间，写法如`b tensorflow::DirectSession::Run`；
    - 对于带有匿名命名空间的断点设置写法示例：`b tensorflow::(anonymous namespace)::ExecutorState::ScheduleReady`，其第二个命名空间为`namespace {}`。


## 8. 安装GDB 8.3并高亮显示源码

### 8.1 安装支持source-highlight的GDB 8.3

* 源码编译并安装source-highlight

```shell
apt install libboost-dev
ln -s /usr/lib/x86_64-linux-gnu/libboost_regex.so.1.58.0 /usr/lib/x86_64-linux-gnu/libboost_regex.so

wget http://ftp.gnu.org/gnu/src-highlite/source-highlight-3.1.8.tar.gz
tar zxvf source-highlight-3.1.8.tar.gz

cd source-highlight-3.1.8
autoreconf -i
mkdir build
cd build
../configure
make -j
make install
```

* 源码编译并安装GDB 8.3[^2]

```shell
apt install texinfo wget

wget http://ftp.gnu.org/gnu/gdb/gdb-8.3.tar.gz
tar zxvf gdb-8.3.tar.gz
cd gdb-8.3

mkdir build && cd build/
../configure --prefix=/usr/local/gdb83 --enable-source-highlight=yes --enable-tui=yes --enable-gold=yes --enable-ld=yes --enable-libada --enable-libssp --enable-lto --enable-vtable-verify --enable-werror

make -j
make install
ln -s /usr/local/gdb83/bin/gdb  /usr/bin/gdb
ln -s /usr/local/gdb83/bin/gdbserver  /usr/bin/gdbserver
```

### 8.2 使用gdb的tui模式

直接使用`gdb -p PID`调试代码，在需要的时候使用切换键`ctrl+x a`调出gdbtui，再次使用`ctrl+x a`则退出gdbtui模式[^3]。

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

## 10 附录（docker容器中的一些配置文件）

### 10.1. apt软件包中国源(`/etc/apt/sources.list`的内容)

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

### 10.2. pip中国源(`~/.pip/pip.conf`内容)

```bash
[global]
trusted-host = mirrors.aliyun.com
index-url = https://mirrors.aliyun.com/pypi/simple
```

## 参考资料

* [Python开发必备神器之一：virtualenv](https://codingpy.com/article/virtualenv-must-have-tool-for-python-development/)
* [TensorFlow 拆包（一）：Session.Run](http://jcf94.com/2018/01/13/2018-01-13-tfunpacking/)
* [从源代码构建TensorFlow](https://www.tensorflow.org/install/source?hl=zh-cn)
* [Bazel安装方法](https://www.jianshu.com/p/bc542266aff3)
* [gdb调试python进程(包括core dump调试)](https://blog.csdn.net/haima1998/article/details/89962435)
* [gdb调试命令总结](https://www.cnblogs.com/wuyuegb2312/archive/2013/03/29/2987025.html)
* [gdb在类成员函数上设置断点](https://menrfa.wordpress.com/2012/01/26/%E4%BD%BF%E7%94%A8gdb%E5%9C%A8%E6%9F%90%E5%87%BD%E6%95%B0%E4%B8%8A%E8%AE%BE%E7%BD%AE%E6%96%AD%E7%82%B9%E9%81%87%E5%88%B0%E7%9A%84%E9%97%AE%E9%A2%98%E5%92%8C%E8%A7%A3%E5%86%B3%E5%8A%9E%E6%B3%95/)
* [100个gdb小技巧](https://wizardforcel.gitbooks.io/100-gdb-tips/content/)

[^1]: 文档来源于[TensorFlow代码阅读指南](http://jcf94.com/download/TensorFlow-SourceCode-Reading.pdf)。
[^2]: 此处参考[编译并安装GDB 8.3](https://medium.com/@simonconnah/compiling-and-installing-gdb-8-3-on-ubuntu-19-04-eac597e4cfb8)。
[^3]: 此处参考[在gdb中显示源码(gdbtui使用方法)](http://mingxinglai.com/cn/2013/07/gdbtui)。
