---
layout: post
title: git常用功能总结
date: 2020-05-17
comments: true
toc: true
categories: [ "git" ]
---

### 1. 首次配置git

```shell
# 为计算机上的每个仓库设置 Git 用户名，查看配置使用 git config --global user.name
git config --global user.name "Mona Lisa"
# 为计算机上的每个仓库设置电子邮件地址，查看配置使用 git config --global user.email
git config --global user.email "email@example.com"

# 下面的两个操作将覆盖某一个仓库中的全局 Git 配置设置，但不会影响任何其他仓库
# 为一个仓库设置 Git 用户名，查看使用 git config user.name
git config user.name "Mona Lisa" 
# 为一个仓库设置电子邮件地址，查看使用 git config user.email
git config user.email "email@example.com" 

```

### 2. 设置github 代理

```shell
export https_proxy=http://x.x.x.x:p
export http_proxy=http://x.x.x.x:p
```

### 3. 关闭git的SSL验证

```shell
git config --global http.sslVerify false
```

### 4. git cherry-pick 流程

```shell
# develop分支合入自己的pr后，进行如下操作：

# 1. 切换到develop主分支，并拉取最新代码
git checkout develop
git fetch upstream
git rebase upstream/develop

# 2. 获取待cherry-pick pr的squash commit id
git log

# 3. 切换到所需cherry-pick的目标分支
git fetch upstream release/1.7:fuse_bn_act
git checkout fuse_bn_act

# 4. 执行cherry-pick
git cherry-pick ${target_commit_id}

git log #（Optional）验证cherry-pick成功与否
git diff HEAD^ # （Optional）查看cherry-pick的内容

# 5. 提交cherry-pick代码
git push origin fuse_bn_act
```

### 5. cherry-pick一个PR

下面以pr链接 [https://github.com/PaddlePaddle/Paddle/pull/24602](https://github.com/PaddlePaddle/Paddle/pull/24602) 为例进行讲解。

* 拷贝pr链接并在链接后面加上`.patch`，然后在浏览器中打开该组合链接。例如：  [https://github.com/PaddlePaddle/Paddle/pull/24602.patch](https://github.com/PaddlePaddle/Paddle/pull/24602.patch) 。
* 浏览器地址框将会自动转换URL为如下内容：[https://patch-diff.githubusercontent.com/raw/PaddlePaddle/Paddle/pull/24602.patch](https://patch-diff.githubusercontent.com/raw/PaddlePaddle/Paddle/pull/24602.patch) 。
* 使用这个新生成的URL链接将pr对应的补丁cherry-pick到本地分支，使用命令如下：`curl https://patch-diff.githubusercontent.com/raw/PaddlePaddle/Paddle/pull/24602.patch | git am`。

完整实例如下：

```shell
git fetch upstream release/1.8:fix_amp
git checkout fix_amp
curl https://patch-diff.githubusercontent.com/raw/PaddlePaddle/Paddle/pull/24602.patch | git am
```

### 6. git tag用法

```shell
# 1. 查看本地分支标签
git tag / git tag -l / git tag --list

# 2. 查看远程所有标签
git ls-remote --tags

# 3. 给当前分支打标签
git tag v1.0.0

# 4. 给特定的某个commit版本打标签
git tag v1.0.0 039bf8b
# 4.1 打tag时添加注释
git tag v1.0.0 039bf8b -m "add tags information"

# 5. 删除本地某个标签
git tag -d v1.0.0 / git tag --delete v1.0.0

# 6. 删除远程的某个标签
git push origin :v1.0.0 / git push origin -d v1.0.0

# 7. 将本地标签一次性推送到远程
git push origin --tags

# 8. 将本地某个特定标签推送到远程
git push origin v1.0.0

# 9. 查看某一个标签的提交信息
git show v1.0.0

```

### 7. 创建新分支

```shell
# 基于当前分支创建新分支
git checkout -b newBranch

# 根据某个commit创建本地分支
git checkout db5d3131 -b newBranch

# 根据某个tag创建本地分支
git checkout v2.4.1 -b newBranch

# 根据某个远程分支创建本地分支方法1(自动切换到新分支)
git checkout remotes/origin/r2.2 -b newBranch

# 根据某个远程分支创建本地分支方法2(不会自动切换到新分支)
git fetch upstream release/1.7:newBranch
```

### 8. 删除本地/远程分支

* 删除本地分支

  ```shell
  # 切换到 develop 分支
  git checkout develop
  
  # 删除 my-branch 分支
  git branch -D my-branch
  ```

* 删除远程分支

  ```shell
  git push origin :my-branch
  ```

### 9. 减少commit数到方法

* 使用`git commit --amend`补充上次的commit。

* 本地进行squash commits。

  ```shell
  # Squash commits locally with
  git rebase -i origin/master~4 master
  # then force push with
  git push origin +master
  ```

### 10. \-\-force 和 + 的不同之处

引用自 [`git push`](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force) 文档:

> Note that `--force` applies to all the refs that are pushed, hence using it with `push.default` set to `matching` or with multiple push destinations configured with `remote.*.push` may overwrite refs other than the current branch (including local refs that are strictly behind their remote counterpart). To force a push to only one branch, use a `+` in front of the refspec to push (e.g `git push origin +master` to force a push to the `master` branch).

### 11. 将PR与Issue相关联

若PR解决了某个Issue问题，可在该PR的**第一个**评论框中加上：`fix #issue_number`，这样当该PR被合并后，会自动关闭对应的Issue。关键词包括：close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved，可自行选择合适的词汇。

### 12. 使用二分法和git定位引入bug的PR

详见[二分法调试脚本](/assets/tools/binary_search_debug.py)。

### 13. git diff中文乱码
```shell
# 显示status编码
git config --global core.quotepath false
# 图形界面编码
git config --global gui.encoding utf-8
# 提交信息编码
git config --global i18n.commit.encoding utf-8
# 输出log编码
git config --global i18n.logoutputencoding utf-8
# git log默认使用less分页，对less命令进行utf-8编码
export LESSCHARSET=utf-8
```

## 参考资料

* [How to squash commits in git after they have been pushed?](https://stackoverflow.com/questions/5667884/how-to-squash-commits-in-git-after-they-have-been-pushed)
* [在 Git 中设置用户名](https://help.github.com/cn/github/using-git/setting-your-username-in-git)
* [设置提交电子邮件地址](https://help.github.com/cn/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address)
* [Closing issues via commit messages](https://help.github.com/articles/closing-issues-via-commit-messages)
* [git push文档](https://git-scm.com/docs/git-push#Documentation/git-push.txt---force)
* [Git 更安全的强制推送，--force-with-lease](https://blog.csdn.net/WPwalter/article/details/80371264)
* [修复git diff正文中文乱码](https://www.jianshu.com/p/fc8162ed1e3d)
