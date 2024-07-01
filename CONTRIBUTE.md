# Contribution Guide

----

欢迎各位旁友加入比赛队伍 🤗🎉

这个比赛有点大——三道题，且相互弱相关——我们不得不建立一个统一的repo来方便管理。


### 计算资源

比赛所用的主要计算资源是华为的 ModelArts 平台 [https://console.huaweicloud.com/modelarts/](https://console.huaweicloud.com/modelarts/)

华为有 ttm 自己的一套软硬件组合拳，和我们所熟悉的平台架构相比有如下的术语对应关系：

```
    PyTorch    <--->    MindSpore
  nvidia-smi   <--->     npu-smi
  CUDA+cuDNN   <--->      CANN
     VRAM      <--->       HBM
  NVIDIA GPU   <--->   Ascend NPU (昇腾)   <-  实际性能等于4倍大树莓派 (嘘🤫
Intel/AMD CPU  <--->  Kunpeng CPU (鲲鹏)
    x86_64     <--->     aarch64
```

赛事主办方目前为 3 道题目一共提供 1+3+3=7 张 1000 共计 7000 块钱的代金券，华子相对而言还是比较大气的，实验资源相对充裕：

| 配置 | 单价 | 可用实验时间 | 说明 |
| :-: | :-: | :-: | :-: |
| 1*Ascend(32G) +  24 core CPU  192G RAM |  21.723 | 322.23h | 最低配置，可以跑推理优化题 |
| 1*Ascend(64G) +  24 core CPU  192G RAM |  39.491 | 177.25h | |
| 2*Ascend(32G) +  48 core CPU  384G RAM |  43.439 | 161.14h | |
| 2*Ascend(64G) +  48 core CPU  384G RAM |  78.975 |  88.63h | |
| 4*Ascend(32G) +  96 core CPU  768G RAM |  86.871 |  80.57h | 可以跑模型微调题 |
| 4*Ascend(64G) +  96 core CPU  768G RAM | 157.943 |  44.31h | |
| 8*Ascend(32G) + 192 core CPU 1536G RAM | 173.736 |  40.29h | |
| 8*Ascend(64G) + 192 core CPU 1536G RAM | 315.882 |  22.16h | 最高配置，金子做的 |

⚠ 但有一个毛病就是只能队长申请代金券，所以想要玩玩云平台的可以找我小窗要账号 ;)


### 代码贡献指南

我们有两个仓库，照顾到翻墙苦难人，请主要关注 **Gitee** 这个源进行开发：

- 开发仓库 Gitee: [https://gitee.com/Kahsolt/mind-spore-2024-ai-model-develop-challenge](https://gitee.com/Kahsolt/mind-spore-2024-ai-model-develop-challenge)
- 镜像仓库 Github: [https://github.com/Kahsolt/MindSpore-2024-AI-model-develop-challenge](https://github.com/Kahsolt/MindSpore-2024-AI-model-develop-challenge)

目前计划，主要的团队合作方式将以**任务**的形式发布：

- 推荐使用 [ForkApp](https://git-fork.com/) 作为 git 前端工具
- 时常关注仓库中的 `task/*` 分支 (用 git fetch 刷新)
  - 可以看看模板分支: `task/_tmpl`
  - task 分支的第一个分叉提交会包含一个文件 `TODO.md` (可能出现在任何地方，用 ForkApp 找找)
- 你需要按照 `TODO.md` 的指示完成代码，**然后删掉这个 `TODO.md` 文件** 并向主分支 `master` 提一个 PullRequest
- 当 PR 被合并后就可以删除这个分支了，请把本地也切回 `master` 然后更新 `git pull --rebase`

----
2024年7月1日
