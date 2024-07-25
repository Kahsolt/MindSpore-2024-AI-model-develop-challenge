# LLaMA3-8b 模型微调

----

### 资源材料下载

⭐实验手册⭐: [2024昇腾AI大赛MindSpore赛道实验指导手册.pdf](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/2024昇腾AI大赛MindSpore赛道实验指导手册.pdf)  

⚠ **以下资源链接仅供参考引用，不要手动下载**，参考脚本 [material/download.cmd](./material/download.cmd) 来自动化下载！！

- LLaMA3-8b
  - checkpoint: [llama3-8B.ckpt](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/llama3-8B.ckpt)
  - tokenizer: [tokenizer.model](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/tokenizer.model)
- pretrain dataset
  - SQuAD: [squad1.1.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/squad1.1.zip)
- finetune dataset
  - 转换前: [train.json](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/train.json)
  - 微调数据集转换后: [train-data-conversation.json](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/train-data-conversation.json)
  - 微调配置文件参考: [run_llama3_8b_8k_800T_A2_64G_lora_dis_256.yaml](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/run_llama3_8b_8k_800T_A2_64G_lora_dis_256.yaml)
- frameworks
  - mindspore（或者使用官网mindspore2.3.0RC2）：[mindspore-2.3.0rc2-cp39-cp39-linux_aarch64.whl](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/mindspore-2.3.0rc2-cp39-cp39-linux_aarch64.whl)
  - mindformers 比赛固定版: [mindformers.zip](https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/mindformers.zip)

```txt
各资源的层次依赖关系：
|               mindformers                    |
|----------------------------------------------|
| mindspore | llama3_8b.ckpt & tokenizer.model |

数据集处理：
- 原始评估数据集: dev-v1.1.json -> squad8192.mindrecord
- 微调数据集: train.json -> train-data-conversation.json -> train-fastchat256.mindrecord

[基线参考]
原始权重性能指标：
  - 原始评估任务 SQuAD
    - F1 score: 59.87023775108988, Em score: 44.17029511369134
    - 选手需要保证微调后的模型的原有能力得分大于等于原始指标的90%的得分
      - F1 score: 53.88321397598089, Em score: 39.75326560232221
  - 微调任务
    - Accuracy: 20%
基线配置微调的训练速度：
  - 9万条数据集
  - 4卡 (训练需要 4/8 卡机，推理只需单卡)
  - LoRA微调（微调参数量大概3million）
  - 6小时
  - seq_len=256
  - batch_size=64
  - epoch=5

[需要关注的文件]
- mindformers\research\llama3
```

# LoRA Notes

- Attn 是低秩序的，可用 LoRA；FFW 是高秩的，不太能 LoRA
- LoRA+: 记 ΔW = A*B，则矩阵 B (out) 的学习率要比矩阵 A (in) 大，比如 2^4 倍


#### references

- 使用LoRA（低秩自适应）微调LLM的实用技巧: http://lonepatient.top/2023/11/30/practical-tips-for-finetuning-llms
- 一文读懂 Llama2 提示词结构与编写指南: https://www.53ai.com/news/qianyanjishu/786.html
- 如何训练LLaMA2: https://blog.csdn.net/qq_27149279/article/details/131981984

----
by Armit
2024/06/21 
