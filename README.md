声明：本博客模板参考于[Cogs and Levers](https://github.com/tuttlem/tuttlem.github.io)、[Hux Blog
](https://github.com/huxpro/huxpro.github.io)以及[Jun711 blog](https://github.com/Jun711/jun711.github.io)。

* 运行`./new-post.sh Blog Title`脚本创建新博客。
* 运行`run-docker.sh`脚本开启本地预览（启动预览容器）。

开启jekyll本地服务：`jekyll serve --watch --port 8888`

本地浏览：http://localhost:8888

jekyll可用配置选项说明:

```bash
jekyll serve
# => 开发服务将会运行在http://localhost:4000/
# 自动生成更新会被开启，如果不想开启请使用`--no-watch`。

jekyll serve --no-watch
# => 等同于`jekyll serve`，但是内容更改时不会自动生成新的。

jekyll serve --livereload
# LiveReload将在更新后刷新浏览器页面。

jekyll serve --incremental
# Incremental将会匹配更改部分，执行部分构建以减少自动生成更新时间。

jekyll serve --detach
# => 等同于`jekyll serve`，但是不会再当前终端中显示运行状态，而是转为后台模式。
#    如果你需要关闭服务，你可以`kill -9 $PID`。
#    如果你不知道PID，那么就执行`ps aux | grep jekyll`并关闭这个实例。
```
