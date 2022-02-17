---
layout: post
title: "Linux常用命令总结"
date: 2017-11-25
comments: true
toc: true
categories: [ "Linux" ]
---

### 解压与压缩[^compress]

#### 常见压缩格式及对应解压方法
```
.tar 
解包：tar xvf FileName.tar
打包：tar cvf FileName.tar DirName
（注：tar是打包，不是压缩！）
```

```
.gz
解压1：gunzip FileName.gz
解压2：gzip -d FileName.gz
压缩：gzip FileName
```

```
.tar.gz 和 .tgz
解压：tar zxvf FileName.tar.gz
解压（指定解压目录）：tar -C /work/Odroid -xzf FileName.tar.gz
压缩：tar zcvf FileName.tar.gz DirName
```

```
.bz2
解压1：bzip2 -d FileName.bz2
解压2：bunzip2 FileName.bz2
压缩： bzip2 -z FileName
```

```
.tar.bz2
解压：tar jxvf FileName.tar.bz2
压缩：tar jcvf FileName.tar.bz2 DirName
```

```
.bz
解压1：bzip2 -d FileName.bz
解压2：bunzip2 FileName.bz
压缩：未知
```

```
.tar.bz
解压：tar jxvf FileName.tar.bz
压缩：未知
```

```
.Z
解压：uncompress FileName.Z
压缩：compress FileName
```

```
.tar.Z
解压：tar Zxvf FileName.tar.Z
压缩：tar Zcvf FileName.tar.Z DirName
```

```
.zip
解压：unzip FileName.zip
压缩：zip FileName.zip DirName
```

```
.rar
解压：rar x FileName.rar
压缩：rar a FileName.rar DirName
```

```
.lha
解压：lha -e FileName.lha
压缩：lha -a FileName.lha FileName
```

```
.rpm
解包：rpm2cpio FileName.rpm | cpio -div
```

```
.deb
解包：ar p FileName.deb data.tar.gz | tar zxf -
```

```
.tar .tgz .tar.gz .tar.Z .tar.bz .tar.bz2 .zip .cpio .rpm .deb .slp .arj .rar .ace .lha .lzh .lzx .lzs .arc .sda .sfx .lnx .zoo .cab .kar .cpt .pit .sit .sea
解压：sEx x FileName.*
压缩：sEx a FileName.* FileName

sEx只是调用相关程序，本身并无压缩、解压功能，请注意！
```

#### gzip 命令介绍
gzip [选项] 压缩（解压缩）的文件名该命令的各选项含义如下：   

* -c 将输出写到标准输出上，并保留原有文件。
* -d 将压缩文件解压。
* -l 对每个压缩文件，显示下列字段：     压缩文件的大小；未压缩文件的大小；压缩比；未压缩文件的名字。
* -r 递归式地查找指定目录并压缩其中的所有文件或者是解压缩。
* -t 测试，检查压缩文件是否完整。
* -v 对每一个压缩和解压的文件，显示文件名和压缩比。
* -num 用指定的数字 num 调整压缩的速度，-1 或 --fast 表示最快压缩方法（低压缩比），-9 或--best表示最慢压缩方法（高压缩比）。系统缺省值为 6。  

#### gzip指令实例：   

* gzip *       #把当前目录下的每个文件压缩成 .gz 文件。
* gzip -dv *   #把当前目录下每个压缩的文件解压，并列出详细的信息。
* gzip -l *    #详细显示例1中每个压缩的文件的信息，并不解压。
* gzip usr.tar #压缩 tar 备份文件 usr.tar，此时压缩文件的扩展名为.tar.gz。  

### 求某个文件的SHA256校验和

```bash
sha256sum gpslogger-78.zip > gpslogger-78.zip.SHA256
```

### 检查SHA256校验和

```bash
sha256sum -c gpslogger-78.zip.SHA256
```

**注意:** 检查校验和时，源文件(gpslogger-78.zip)和校验和文件(gpslogger-78.zip.SHA256)要放在同一目录下。

#### PGP校验

* 从文件（如Keybase.io）导入PGP的公钥（PGP Public Key）或者直接使用命令` gpg --recv-key 公钥值`（公钥值如76CBE9A9）。  
* 验证完整性和签名的命令如下：

```bash
gpg --verify ~/Downloads/gpslogger-71.apk.asc
```

### 查看目录中所有文件大小总和

```bash
du -sh
```

### 查看磁盘情况

```bash
df -hl
```

### 查看System.map中的符号信息

#### 第一种方法

```bash
sudo cat /boot/System.map-$(uname -r) | grep "vmap_area_list"
```

#### 第二种方法

```bash
cd /proc
sudo cat kallsyms | grep "vmap_area_list"
```

**注意，在第二种方法中若是不加上sudo，输出的地址将全是0。**

#### 第三种方法

```bash
 nm vmlinux | grep "vmap_area_list"
```
如果是自己编译内核，则会拥有内核镜像文件vmlinux（make后生成的）。  

### Ubuntu系统安装软件

#### 离线deb软件包的安装方法

```bash
sudo  dpkg  -i  package.deb
```

dpkg的一些实用使用方法：

```bash
dpkg -i package.deb	安装包
dpkg -r package	删除包
dpkg -P package	删除包（包括配置文件）
dpkg -L package	列出与该包关联的文件
dpkg -l package	显示该包的版本
dpkg –unpack package.deb	解开 deb 包的内容
dpkg -S keyword	搜索所属的包内容
dpkg -l	列出当前已安装的包
dpkg -c package.deb	列出 deb 包的内容
dpkg –configure package	配置包
```

##### 范例
在Ubuntu LTS 14.04下安装OpenJDK：

1. 从[archive.ubuntu.com](http://archive.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/)下载64位deb包:
   * [openjdk-8-jre-headless_8u45-b14-1_amd64.deb](http://archive.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jre-headless_8u45-b14-1_amd64.deb) with SHA256   0f5aba8db39088283b51e00054813063173a4d8809f70033976f83e214ab56c0
   * [openjdk-8-jre_8u45-b14-1_amd64.deb](http://archive.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jre_8u45-b14-1_amd64.deb) with SHA256   9ef76c4562d39432b69baf6c18f199707c5c56a5b4566847df908b7d74e15849
   * [openjdk-8-jdk_8u45-b14-1_amd64.deb](http://archive.ubuntu.com/ubuntu/pool/universe/o/openjdk-8/openjdk-8-jdk_8u45-b14-1_amd64.deb) with SHA256   6e47215cf6205aa829e6a0a64985075bd29d1f428a4006a80c9db371c2fc3c4c
2. 利用`sha256sum -c`命令检查校验和  
3. 安装deb软件包

```bash
sudo apt-get update
#安装所下载的三个deb软件包
sudo dpkg -i {downloaded.deb file}
```
**注意:**使用dpkg命令安装软件时，可能会因为缺少依赖而出现错误，此时只需运行如下命令(安装出错之后运行)：

```bash
sudo apt-get -f install
```

然后重新运行`sudo dpkg -i {downloaded.deb file}`命令，安装所需deb包。

4） 更新默认Java 版本(可选)

```bash
sudo update-alternatives --config java
sudo update-alternatives --config javac
```

#### 使用apt安装和卸载软件

* 查找软件

```bash
apt-cache search keyword
```

* 查询软件状态

```bash
apt-cache policy softname
```

* 安装软件

```bash
apt-get install softname1 softname2 softname3……
```

* 卸载软件

```bash
apt-get remove softname1 softname2 softname3……
```

* 卸载并清除配置

```bash
apt-get remove --purge softname1
```

* 更新软件信息数据库

```bash
apt-get update
```

* 进行系统升级

```bash
apt-get upgrade
```

* 搜索软件包

```bash
apt-cache search softname1 softname2 softname3……
```

##### 范例

使用apt在Ubuntu 版本大于15.04平台下安装OpenJDK：

1. 使用apt命令安装
  ```bash
  sudo apt-get update
  sudo apt-get install openjdk-8-jdk
  ```
2. 更新默认Java 版本(可选)
  ```bash
  sudo update-alternatives --config java
  sudo update-alternatives --config javac
  ```

### 解决Android文件系统只读问题

解除`Read only file system on Android`限制的方法：
1. Simply change ro to rw and add the remount option（root权限）
  ```bash
  mount -o rw,remount /system
  ```
2. Once you are done making changes, you should remount with the original readonly（root权限）.
  ```bash
  mount -o ro,remount /system
  ```

### 远程命令

#### 远程登录

```bash
# 基本用法
ssh user@host
# 若本地用户名与远程用户名一致，登录时可以省略用户名
ssh host
# 指定端口
ssh -p 2222 user@host
```

#### 建立ssh通道

```bash
# 通过localhost:1234直接访问远程的ip:port
ssh -L 127.0.0.1:1234:127.0.0.1:8888 username@address_of_remote

# -L选项中的本地网卡地址是可以省略,例如：
# 在本地主机A1登陆远程云主机B1，并进行本地端口转发。2000端口绑定本地所有网卡
ssh -L 2000:localhost:3000 username@address_of_remote
```

#### 远程复制文件

```bash
# 上传文件
scp 需要上传的文件路径  user@host:/dir

# 上传文件夹
scp -r 需要上传的文件夹路径  user@host:/dir

# 下载文件
scp user@host:/dir/文件名 要拷贝到的地方
# 指定端口
scp -P 2222 user@host:/dir   要拷贝到的地方
```

### update-alternatives切换默认程序

#### 设置默认gcc

```shell
sudo update-alternatives --install /usr/bin/gcc gcc /usr/local/gcc-8.2/bin/gcc 82 --slave /usr/bin/g++ g++ /usr/local/gcc-8.2/bin/g++
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 10 --slave /usr/bin/g++ g++ /usr/bin/g++-10
```


#### 设置默认cmake

```shell
sudo update-alternatives --install /usr/bin/cmake cmake /usr/local/cmake-3.5.0-Linux-x86_64/bin/cmake 305 --slave /usr/bin/ctest ctest /usr/local/cmake-3.5.0-Linux-x86_64/bin/ctest --slave /usr/bin/ccmake ccmake /usr/local/cmake-3.5.0-Linux-x86_64/bin/ccmake --slave /usr/bin/cmake-gui cmake-gui /usr/local/cmake-3.5.0-Linux-x86_64/bin/cmake-gui --slave /usr/bin/cpack cpack /usr/local/cmake-3.5.0-Linux-x86_64/bin/cpack
sudo update-alternatives --install /usr/bin/cmake cmake /usr/local/cmake-3.10.0-Linux-x86_64/bin/cmake 310 --slave /usr/bin/ctest ctest /usr/local/cmake-3.10.0-Linux-x86_64/bin/ctest --slave /usr/bin/ccmake ccmake /usr/local/cmake-3.10.0-Linux-x86_64/bin/ccmake --slave /usr/bin/cmake-gui cmake-gui /usr/local/cmake-3.10.0-Linux-x86_64/bin/cmake-gui --slave /usr/bin/cpack cpack /usr/local/cmake-3.10.0-Linux-x86_64/bin/cpack
```

### 从apt安装gcc-10

* 编辑`/etc/apt/sources.list`，加入如下语句：

```shell
deb http://ftp.hk.debian.org/debian sid main
```

* 运行`sudo apt update`更新安装源，出现密钥验证错误，使用如下命令解决[^gpgerr]：

```
gpg --keyserver hkp://pool.sks-keyservers.net:80 --recv-key 04EE7237B7D453EC
# gpg --keyserver pgpkeys.mit.edu --recv-key 04EE7237B7D453EC
gpg -a --export 04EE7237B7D453EC | sudo apt-key add -
```

之后再次运行`sudo apt update`命令。

* 安装gcc-10

```
sudo apt install gcc-10 g++-10
```

### 使用grep和xargs过滤文件

```bash
ls | grep -v -E "\.py$|doc" | xargs -I {} mv {} ./doc
```

### Ubuntu一行命令换apt源
```shell
sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.163.com\/ubuntu\//g' /etc/apt/sources.list && apt update
```

### sed命令批量替换字符串

```shell
sed -i "s/原字符串/新字符串/g" `grep 原字符串 -rl 所在目录`
# demo: sed -i "s/CHECK(/CHECK_CUDA(/g" `grep CHECK\( -rl .`

grep "CHECK_CUDA(" . -nr

# -i 表示inplace edit，就地修改文件
# -r 表示搜索子目录
# -l 表示输出匹配的文件名
# -n 表示输出匹配的行号
```

### 使用正则表达式查找特定文件

```shell
find ~/.cache/bazel/ -path "*external/org_tensorflow" | grep "_bazel_root/[A-Za-z0-9]*/external/org_tensorflow$"
```

### shell脚本默认参数设置

```shell
SAVE_FILE=xla_pass_${1:-'unspecified'}.csv
GPU_ID=${2:-'0'}
```

### 参考资料

* [Establishing a Build Environment](http://source.android.com/source/initializing.html)
* [Ubuntu中用apt安装和卸载软件](http://blog.csdn.net/ludonghai715/article/details/5657724)
* [Ubuntu .deb包安装方法](http://blog.csdn.net/zhaoyang22/article/details/4235596)
* [Installing newer GCC versions in Ubuntu](https://tuxamito.com/wiki/index.php/Installing_newer_GCC_versions_in_Ubuntu)
* [每天一个linux命令（39）：grep 命令](https://www.cnblogs.com/peida/archive/2012/12/17/2821195.html)
* [linux find -regex 使用正则表达式](https://www.cnblogs.com/jiangzhaowei/p/5451173.html)

[^compress]: 内容引自[inux下解压命令大全](http://www.cnblogs.com/eoiioe/archive/2008/09/20/1294681.html)
[^gpgerr]: [What's the best way to install apt packages from Debian Stretch on Raspbian Jessie?](https://unix.stackexchange.com/questions/274053/whats-the-best-way-to-install-apt-packages-from-debian-stretch-on-raspbian-jess)
