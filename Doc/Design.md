# 多维笔记



## 设计目标

我们常常会需要记录一些信息:

> 自己这些天做了什么？
>
> 有哪些事情是想做还没做的？

我们常常会需要报告一些信息：

>上个月15号到这个月15号我做了什么？
>
>上个月1号到这个月1号我做了什么？
>
>今年上半年我干了些啥？
>
>2020年一整年我干了些啥？

我们记录自己做了什么时，通常习惯按天来记。（比如你的日志

我们报告自己做了什么时，通常想要按照类目来讲述。（比如你的月报

我们记录自己打算做什么时，通常也想要按照类目来写TODO-List。

**如此一来，信息在不同结构间转换时，就变得非常麻烦，本软件的目的就是为了避免这种麻烦。**



## 架构设计

### 不重复造轮子

记录日志信息，最好的工具是流式的，能够处理简单的hierarchical结构，md就不错，推荐Typora。

记录结构化信息，最好的工具是思维导图，能够处理非常复杂的Hierachical结构，比如xmind。

记录思路和设计细节，最好的工具是综合功能强大的笔记软件，能：

- 处理好各种格式的信息
- 有结构化的管理机制
- 能够跨平台
- 要有强大的引用功能，包括http引用、内部引用，甚至是机器内本地引用

能做到这些的有且只有Onenote，世界上最好的笔记软件（作者个人观点）。

### 还差一只胶水

所以，我们其实就差一只胶水了，本软件就是这只胶水，我们：

- 在Xmind中定义框架结构
- 在Typora（md编辑器）中撰写每日日志
- 在Onenote中撰写详细的设计案，并提供引用链接。
- 用软件生成我们想要的整合信息。

### 杂想



## 开发思路



### 素材

Github客户端下载地址：https://desktop.github.com/

virtualenv介绍文档：https://virtualenv.pypa.io/en/latest/user_guide.html#introduction

vscode配置virtualenv：https://code.visualstudio.com/docs/python/python-tutorial#_install-and-use-packages

xmindSDK：https://pypi.org/project/xmind-sdk/

xmindSDK-github：https://github.com/xmindltd/xmind-sdk-python

一篇SDKDemo的文档：https://www.codestudyblog.com/cnb2010b/1007195356.html

将xmind文件转成可编程数据类型 ：https://tobyqin.cn/posts/2018-07-01/parse-xmind-to-programmable-data-type/

xmindparser的git：https://github.com/tobyqin/xmindparser



没什么用的素材：

将纯文本转化为静态网站和博客：https://www.jekyll.com.cn/

Jenkins Pipeline 一点通 https://tobyqin.cn/posts/2021-02-01/jenkins-pipeline/

一个老哥的Blog：https://tobyqin.cn/

xmind转换到testlink https://github.com/tobyqin/xmind2testlink

TestLink Open Source Test Management https://www.testlink.org/

### 准备工作

#### 构建项目


#### 构建venv

```
py -3 -m venv .venv

.venv\scripts\activate

# 如果activate失败，执行下面的语句来提升权限
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

```

选择VSCode的Interpreter为上面的虚拟环境

#### 安装xmindSDK

-- 安装后，果然不出我所料，8年前的项目，已经不支持最新版本的xmind的，旧版用xml，新版转到json了，弃用。

#### 安装xmindParser

从git上获取即可：https://github.com/tobyqin/xmindparser

本地放在LibSrc目录下，可以用python setup.py installl来安装（如果不需要改它源码的话），直接安装在env当中最好















































