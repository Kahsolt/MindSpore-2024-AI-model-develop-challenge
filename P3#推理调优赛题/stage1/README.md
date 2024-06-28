# LLaMA2-7b 推理调优


#### 环境构建

⚪ 本地 (打桩调试)

- `conda create -n llm python==3.9.19`
- run `material\download.cmd` and unzip everything under this repo root
- `run_init.cmd`

⚪ 云上 (实测)

⚠ 云实验环境不保存系统状态，每次重启都要重新安装 python lib

- see [run_init.sh](./run_init.sh) and [run_infer.sh](./run_infer.sh)
- overwrite `llm-serving`, `mindformers` and `performance_serving` with this repo's modified version


#### 资源材料

⚠ 最终评测在 Ascend910b4 设备上，其指令集架构为 aarch64

- LLaMA2-7b model distro
  - checkpoint: [llama2_7b.ckpt](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/llama2_7b.ckpt)
  - tokenizer: [tokenizer.model](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/tokenizer.model)
- frameworks:
  - runtime: [mindspore](https://gitee.com/mindspore/mindspore), (contest: [mindspore-2.3.0rc2-cp39-cp39-linux_aarch64.whl](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/mindspore-2.3.0rc2-cp39-cp39-linux_aarch64.whl), **NOT for x86_64**)
  - application: [mindformers](https://gitee.com/mindspore/mindformers), (contest: [mindformers.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/mindformers.zip))
  - deploy: [LLM-serving](https://gitee.com/mindspore/llm-serving), (contest: [llm-serving.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/llm-serving.zip))
- judger code: [performance_serving.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic3-infer/performance_serving.zip)


#### 测试数据集

- 速度测试: 测数据集 [performance_serving/alpaca_5010.json](performance_serving/alpaca_5010.json) 前 1500 个样本的推理时长
  - 测试命令: `python test_serving_performance.py --task 1 -X 0.5 -T 3000`
  - 基准设置: -X 0.5 -T 3000, 推理时间: 3551.9252s (⚠ 必须保证 -X 乘以 -T 等于 1500，可自行改动)
- 精度测试: 测数据集 [performance_serving/alpaca_521.json](performance_serving/alpaca_521.json) 前 500 个样本的推理 logits 结果
  - logits 保存命令: `python test_serving_performance.py --task 2 -X 0.1 -T 5000`
    - ⚠ 此处 `-X 0.1 -T 5000` 为固定的竞赛设置不可改动
  - logits 校验命令: `python acc_allclose.py --base_path /home/ma-user/work/file_npy_base --new_path /home/ma-user/work/file_npy_new`

----
by Armit
2024/06/11 
