## Mirai Framework for Python

**作为存放 python-mirai v3 版本的本仓库已经不再维护, 若需查看 v4 的开发进度, 请参阅** [Graia Project](https://github.com/GraiaProject) **处获取 v4 版本的最新开发状态**
**顺便, v4 版本的 python-mirai, 正式名字称为 `Graia Framework`**

### 这是什么?
以 OICQ(QQ) 协议驱动的高性能机器人开发框架 [Mirai](https://github.com/mamoe/mirai) 的 Python 接口, 通过其提供的 `HTTP API` 与无头客户端(`Mirai`)交互.

### 开始使用
#### 从 Pypi 安装
``` bash
pip install kuriyama
```

#### 开始开发

由于 `python-mirai` 依赖于 `mirai` 提供的 `mirai-http-api` 插件, 所以你需要先运行一个 `mirai-core` 或是 `mirai-console` 实例以支撑你的应用运行.

现有的文档地址: https://mirai-py.originpages.com/

### 加入开发
`python-mirai` 项目欢迎一切形式上的贡献(包括但不限于 `Issues`, `Pull Requests`, `Good Idea` 等)  
我们希望能有更多优秀的开发者加入到对项目的贡献上来  

你的 `Star` 是对我们最大的支持和鼓励.  
若你在使用的过程中遇到了问题, 欢迎[提出聪明的问题](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md), 也请不要[像个弱智一样提问](https://github.com/tangx/Stop-Ask-Questions-The-Stupid-Ways), 我们希望有人能让这个项目变得更好.  

请各位开发者在开发遇到问题的时候, 请先去看文档, 然后再来说别的.
如果真的是有程序上的错误, 请先判断是否是 `python-mirai` 的问题,
然后在 issue 处新开一个问题, 通常来讲我会很快的回复(github 会给我发邮件).

**若不是 python-mirai 的问题, 请不要在此处或是用 IM 向我征求解决方法, 先向其他项目汇报问题.**  
**强烈建议使用 Github Issues 系统进行问题的汇报, 我这之后将不会受理来自 IM 的问题汇报.**

### 鸣谢
> 这些项目也很棒, 去他们的项目页看看, 点个 `Star` 以鼓励他们的开发工作, 毕竟没有他们也没有 `python-mirai`.

特别感谢 [`mamoe`](https://github.com/mamoe) 给我们带来这些精彩的项目:
 - [`mirai`](https://github.com/mamoe/mirai): 即 `mirai-core`, 一个高性能, 高可扩展性的 QQ 协议库, 同时也是个很棒的机器人开发框架!
 - [`mirai-console`](https://github.com/mamoe/mirai-console): 一个基于 `mirai` 开发的插件式可扩展开发平台, 我们的大多数开发工作基本上都在该项目上完成, 不得不称赞其带来的开发敏捷性.
 - [`mirai-api-http`](https://github.com/mamoe/mirai-api-http): 为该项目提供 `http` 接口的 `mirai-console` 插件, 万物之源 ~~`python-mirai` 的 star 甚至比 httpapi 还高, 去帮帮吧~~

也感谢使用 `NatriumLab` 旗下开源的工具链进行开发的各位开发者, 请积极向上游项目反馈问题, 这对所有人都是有益的.

### 许可证
我们使用 [`GNU AGPLv3`](https://choosealicense.com/licenses/agpl-3.0/) 作为本项目的开源许可证, 而由于原项目 [`mirai`](https://github.com/mamoe/mirai) 同样使用了 `GNU AGPLv3` 作为开源许可证, 因此你在使用时需要遵守相应的规则.  
