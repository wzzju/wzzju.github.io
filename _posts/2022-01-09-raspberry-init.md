---
layout: post
title: Raspberry Pi初始化开发流程
subtitle: 无显示屏设备联网与配置
date: 2022-01-09
author: YuChen
comments: true
categories: [ "RaspberryPi" ]
---

## 1. 工具准备

* 在[software/operating-systems](https://www.raspberrypi.com/software/operating-systems)上下载`Raspberry Pi OS with desktop`的torrent文件，并使用[qBittorrent](https://github.com/qbittorrent/qBittorrent/tags)工具打开得到的torrent文件以下载raspios-xx.zip文件，解压后可得到对应的raspios-xx.img文件。
* 使用[SDFormatter](https://www.sdcard.org/downloads/formatter/eula_windows)格式化准备好的SD卡（建议8GB以上）。
* 使用[Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager)将raspios-xx.img文件写入到SD卡中。操作步骤如下：
>1) 选择img镜像文件 --> 2) 选择设备 --> 3) 点击写入，等待显示“写入成功” 的对话框出现。

## 2. 预设SD卡
完成上述步骤后，SD卡在系统中显示为boot分区（200+MB），并且SD卡其余存储空间被隐藏。

### 2.1 开启SSH服务
在SD卡boot分区根目录创建一个名为`ssh`的空白文本文档。若不进行此步操作，则会显示`Network error: Connection refused`。

### 2.2 显示设置
在SD卡boot分区中找到`config.txt`文件，修改如下内容：

```shell
# 使用HDMI端口连接到显示器，如果发现画面四周存在黑边，可以通过将该值设为1来避免
disable_overscan=1

# 强制树莓派使用HDMI端口，即使树莓派没有检测到显示器连接仍然使用HDMI端口
hdmi_force_hotplug=1

# hdmi_group = 1 ：使用CEA分辨率，hdmi_group = 2 ：使用DMT分辨率
hdmi_group=2
# hdmi_mode=51 ：分辨率设置为1600x1200  60Hz
hdmi_mode=51

# 强制使用HDMI模式而不是DVI模式，这使得DMT模式下音频可以正常工作
hdmi_drive=2

# 增强HDMI信号
config_hdmi_boost=4

# 注释掉以下两条语句，避免使用VNC Viewer连接树莓派时只能显示很小的窗口
#dtoverlay=vc4-kms-v3d
#max_framebuffers=2
```

### 2.3 WiFi连接预设
在SD卡boot分区创建`wpa_supplicant.conf`文件，并写入如下内容（确保所使用WiFi加密类型为WPA/WPA2-PSK）：

```shell
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="WiFi名称"
    key_mgmt=WPA-PSK
    psk="WiFi密码"
    priority=1
}
```

在树莓派通电后，会自动将boot分区的`wpa_supplicant.conf`文件内容添加到`/etc/wpa_supplicant/wpa_supplicant.conf`文件中，以便进行WiFi的自动连接。

完成上述设置，将准备好的SD卡插入到树莓派中。启动电源后，红灯亮表示供电正常，绿灯闪烁表示在读取SD卡。

## 3. 设置树莓派系统

* 登录路由器管理网站（如192.168.1.1），查看树莓派连接到WiFi后分配到的IP地址。
> 路由器管理网站：状态 --> 用户侧信息 --> 终端下挂设备信息 --> 查看raspberrypi的IP地址
* 使用`ssh pi@树莓派IP地址`登录树莓派以获取树莓派系统终端（初始密码为`raspberry`）。

### 3.1 设置apt中国源
* 修改树莓派系统中的`/etc/apt/sources.list`内容，将其替换为如下内容：
```shell
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ bullseye main contrib non-free rpi
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ bullseye main contrib non-free rpi
```
* 修改树莓派系统中的`/etc/apt/sources.list.d/raspi.list`内容，将其替换为如下内容：
```shell
deb http://mirror.tuna.tsinghua.edu.cn/raspberrypi/ bullseye main
deb-src http://mirror.tuna.tsinghua.edu.cn/raspberrypi/ bullseye main
```

### 3.2 设置pip中国源
创建`~/.pip/pip.conf`文件，填入如下内容：
```shell
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

## 4. 开启VNC服务
使用ssh登录树莓派系统，获取树莓派终端，进行如下操作：
* 输入`sudo raspi-config`命令，打开树莓派配置工具用于开启VNC服务。
> 选择`3 Interface Options` --> 选择`I3 VNC` --> 提示是否要开启VNC，选择<Yes> --> 开启后，可使用Tab键选择`Finish`结束
* 输入`sudo raspi-config`命令，打开树莓派配置工具用于设置VNC显示分辨率。
> 选择`2 Display Options` --> 选择`D1 Resolution` --> 选择`DMT Mode 51` --> 确定<OK>后，可使用Tab键选择`Finish`结束

### 4.1 设置开机自启VNC服务
* 在树莓派终端上输入`sudo vim /etc/init.d/vncserver`命令，并填入如下内容：

```shell
#!/bin/sh
### BEGIN INIT INFO
# Provides:          vncserver
# Required-Start:    $local_fs
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start/stop vncserver
### END INIT INFO
 
# More details see:
# http://www.penguintutor.com/linux/vnc
 
### Customize this entry
# Set the USER variable to the name of the user to start vncserver under
export USER='pi'
### End customization required
 
eval cd ~$USER
 
case "$1" in
  start)
    # 启动命令行：设置分辨率、控制台号码或其它参数
    # -depth 24 用于设置图像质量，-geometry 1600x1200 用于设置分辨率
    su $USER -c '/usr/bin/vncserver -depth 24 -geometry 1600x1200 :1'
    echo "Starting VNCServer for $USER "
    ;;
  stop)
    # 终止命令行：此处控制台号码应与与启动时保持一致
    su $USER -c '/usr/bin/vncserver -kill :1'
    echo "VNCServer stopped"
    ;;
  *)
    echo "Usage: /etc/init.d/vncserver {start|stop}"
    exit 1
    ;;
esac
exit 0
```

* 使用`sudo chmod 755 /etc/init.d/vncserver`命令设置vncserver文件的权限
* 使用`sudo update-rc.d vncserver defaults`命令添加VNC服务为开机启动项
* 使用` sudo reboot`命令重启树莓派。重启后，可使用[VNC Viewer](https://www.realvnc.com/en/connect/download/viewer)远程连接树莓派的图形界面系统

## 5. 安装Wiring Pi库
使用ssh登录树莓派系统，获取树莓派终端，执行如下命令：
```shell
cd /tmp && wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
```

## 参考资料

* [树莓派3B+(一)](https://www.cnblogs.com/cruelty_angel/p/10705511.html)
* [树莓派update更新失败](https://www.jianshu.com/p/6d770d913d69)
* [树莓派VNC详细配置教程](https://www.cnblogs.com/mlzheng/p/15670314.html)
* [解决Raspberry Pi只能在默认640×480模式下显示的问题](http://www.roboby.com/raspberry-pi-640x480.html)
* [树莓派C语言点亮LED教程](https://www.cnblogs.com/JiYF/p/12459640.html)
* [树莓派Python语言点亮LED教程](https://blog.csdn.net/github_35160620/article/details/52140967)
* [使用python构建简单的http上传下载服务](https://github.com/freelamb/simple_http_server)
