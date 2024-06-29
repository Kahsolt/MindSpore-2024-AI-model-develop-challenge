# LLaMA2-7b 推理调优

----

### 资源材料下载

⭐实验手册⭐: [2024昇腾AI大赛MindSpore赛道实验指导手册.pdf](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/2024昇腾AI大赛MindSpore赛道实验指导手册.pdf)  

⚠ **以下资源链接仅供参考引用，不要手动下载**，后面 [实验操作](#实验操作环境构建--测试流程) 章节会告诉你如何用脚本自动化下载！！

- LLaMA2-7b
  - checkpoint: [llama2_7b.ckpt](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/llama2_7b.ckpt)
  - tokenizer: [tokenizer.model](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/tokenizer.model)
- frameworks
  - runtime: [mindspore](https://gitee.com/mindspore/mindspore), (contest: [mindspore-2.3.0rc2-cp39-cp39-linux_aarch64.whl](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/mindspore-2.3.0rc2-cp39-cp39-linux_aarch64.whl), **NOT for x86_64**)
  - application: [mindformers](https://gitee.com/mindspore/mindformers), (contest: [mindformers.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/mindformers.zip))
  - deploy: [LLM-serving](https://gitee.com/mindspore/llm-serving), (contest: [llm-serving.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/llm-serving.zip))
- judger code: [performance_serving.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/performance_serving.zip)

#### 软件架构概览

⚠ 最终评测在 Ascend910b4 设备上，其指令集架构为 aarch64

```txt
各资源的层次依赖关系：
|           performance_serving                |
|==============================================|  <- http
|                      server_app_post (http)  |
|  llm-serving  ===============================|  <- tcp + shared_mem
|                          agent (tcp)         |
|----------------------------------------------|
|               mindformers                    |
|----------------------------------------------|
| mindspore | llama2_7b.ckpt & tokenizer.model |

服务端: llm-serving 会启动两个子服务，其间通过共享内存实现数据传递
  - server_app_post (http): request -> llm_server -> request_engine (queue) -> worker -[tcp]-> agent
  - agent (tcp): shared_mem data -> mindformer model
客户端: performance_serving
  - 为每个测试样例创建一个进程，间隔一定时间依次启动以模拟正常业务环境下的请求发送序列
```


### 实验操作：环境构建 & 测试流程

> 🎉 我们已经魔改了代码，可以兼容支持在 云端Linux+Ascend 或 本地Windows+CPU 两个环境下跑 :)

> 推理优化的主要修改目标: llm-serving > mindformers > mindspore > performance_serving
> *) 我们删除了 performance_serving 中部分冗余无用的代码逻辑，可能会导致评分略微偏高；但主办方校验时可以用原repo来测，接口是兼容的

⚪ 两个环境的区别

```
软硬件环境不同:
- 本地: Windows + CPU (32G RAM)
- 云端: Linux + Ascend 
  - CPU: Kunpeng-920, 192 core (4 sockets * 48 core-per-socket), 192G RAM; aarch64
  - NPU: Ascend-910b4, 32G HBM
使用的配置文件不同:
- 本地
  - llm-serving\configs\llama\llama_7b_kbk_pa_dyn_debug.yaml
  - mindformers\configs\llama2\predict_llama2_7b_debug.yaml
- 云端
  - llm-serving\configs\llama\llama_7b_kbk_pa_dyn.yaml
  - mindformers\configs\llama2\predict_llama2_7b.yaml
```

#### 本地 (打桩调试)

> 打桩调试不需要下载笨重的 llama2_7b.ckpt 也可以进行 ;)

⚪ 安装

- `conda create -n llm python==3.9.19`
- `conda activate llm`
- `pip install -r requirements.txt`
- 跑脚本 `material\download.cmd`
  - 把 `material\file_npy_base.zip` 解压到 `.\file_npy_base\`
  - 关于 llama2_7b.ckpt 和 tokenizer.model 的处理，请参考注释
  - 其他资源目前看来不用下载，应该都已经嵌入本仓库了

⚪ 实验

- 启动命令行环境 `init.cmd`
- 参考 `run.cmd` 和 [experiments](./experiments/) 目录


#### 云上 (实测)

⚪ 安装

- overwrite `llm-serving`, `mindformers` and `performance_serving` with this repo's modified version

⚪ 实验

ℹ 另外参考 [run.sh](./run.sh)

- 初始化命令行环境 (⚠ 云实验环境不保存系统状态，每次都要重装包)
  - `source ./init.sh`
- 启动 llm-serving 服务
  - `cd /home/ma-user/work/llm-serving/`
  - `python examples/start.py --task 1 --config /home/ma-user/work/llm-serving/configs/llama/llama_7b_kbk_pa_dyn.yaml`
- 速度测试: 测数据集 [performance_serving/alpaca_5010.json](performance_serving/alpaca_5010.json) 前 1500 个样本的推理时长
  - `cd /home/ma-user/work/performance_serving/`
  - `python test_serving_performance.py --task 1 -X 0.5 -T 3000`
  - 基准设置: -X 0.5 -T 3000, 推理时间: 3551.9252s (⚠ 必须保证 -X 乘以 -T 等于 1500，可自行改动)
- 精度测试: 测数据集 [performance_serving/alpaca_521.json](performance_serving/alpaca_521.json) 前 500 个样本的推理 logits 结果
  - `cd /home/ma-user/work/performance_serving/`
  - `python test_serving_performance.py --task 2 -X 0.1 -T 5000`
    - ⚠ 此处 `-X 0.1 -T 5000` 为固定的竞赛设置不可改动
  - logits 校验: `python acc_allclose.py --base_path /home/ma-user/work/file_npy_base --new_path /home/ma-user/work/file_npy`


----
by Armit
2024/06/11 
