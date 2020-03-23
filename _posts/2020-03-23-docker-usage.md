---
layout: post
title: Docker容器/镜像备份命令
date: 2020-03-23
comments: true
categories: [ "Docker" ]
---

#### 保存容器修改

```bash
sudo docker commit -a "paddle" -m "backup" d194406b113f paddlepaddle/paddle:latest-gpu-cuda10.0-cudnn7-dev
# -a:修改者信息 -m:注释、说明 紧跟着当前操作的容器id 最后是要生成的新的镜像名称
```

#### 保存镜像

```bash
sudo docker save -o paddle_v100.tar paddlepaddle/paddle:latest-gpu-cuda10.0-cudnn7-dev
```

#### 导入镜像

```bash
sudo docker load<paddle_v100.tar
```

#### 导出容器

```bash
docker export -o my_container.tar <CONTAINER ID>
或者
docker export <CONTAINER ID> > my_container.tar
```

#### 导入容器为镜像

```bash
cat my_container.tar | docker import - image_name:tag
```

> 示例：
>
> ```bash
> cat docker-backup/paddle_dev_img.tar | sudo /usr/bin/docker import - paddlepaddle/paddle:vim-dev&
> ```

#### 查看导入的镜像

```bash
docker images
```

#### 运行导入的镜像

```bash
sudo nvidia-docker run --ulimit core=-1 --security-opt seccomp=unconfined --net=host --name container_name -it -v $PWD/.cache:/root/.cache -v $PWD:/work image_name:tag /bin/bash
```

> `ulimit -c unlimited` —— 调试使用，生成core dump

> 示例：
>
> ```
> sudo docker run --ulimit core=-1 --security-opt seccomp=unconfined --net=host --name paddle_gpu -it -v $PWD/.cache:/root/.cache -v $PWD:/work paddlepaddle/paddle:vim-dev /bin/bash
> ```

#### Docker中的关于cuda的配置

```bash
export LD_LIBRARY_PATH=/root/.virtualenvs/paddlepaddle-venv/lib/python2.7/site-packages/paddle/libs:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/work/cuda/cuda-9.0/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/work/cuda/cudnn/cudnn_v7/cuda/lib64:$LD_LIBRARY_PATH
export LIBRARY_PATH=/work/cuda/cuda-9.0/lib64:$LIBRARY_PATH
export LIBRARY_PATH=/work/cuda/cudnn/cudnn_v7/cuda/lib64:$LIBRARY_PATH
export CPLUS_INCLUDE_PATH=/work/cuda/cuda-9.0/include:$CPLUS_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=/work/cuda/cudnn/cudnn_v7/cuda/include:$CPLUS_INCLUDE_PATH
export PATH=/work/cuda/cuda-9.0/bin:$PATH
```

