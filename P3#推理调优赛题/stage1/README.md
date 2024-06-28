# LLaMA2-7b 推理调优


#### 环境构建

- `conda create -n llm python==3.9.19`
- install [MindSpore](https://www.mindspore.cn/install), for exmaple
  - `pip install https://ms-release.obs.cn-north-4.myhuaweicloud.com/2.2.14/MindSpore/cpu/x86_64/mindspore-2.2.14-cp39-cp39-win_amd64.whl --trusted-host ms-release.obs.cn-north-4.myhuaweicloud.com -i https://pypi.tuna.tsinghua.edu.cn/simple`
  - `python -c "import mindspore;mindspore.set_context(device_target='CPU');mindspore.run_check()"`
- run mindformers
  - `cd mindformers`
  - `pip -r requirements.txt`
  - `run.cmd`
- run llm-serving
  - `cd llm-serving`
  - `python setup.py bdist_wheel`
  - `pip install dist\mindspore_serving-2.1.0-py39-none-any.whl`


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

- 见 [performance_serving/alpaca_data.json](performance_serving/alpaca_data.json)
- 共计 52002 个问答测试样例, 三个字段 instruction/input/output

----
by Armit
2024/06/11 
