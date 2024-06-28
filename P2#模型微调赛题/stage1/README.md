# LLaMA2-8b 模型微调


#### 环境构建


#### 资源材料

⚠ 最终评测在 Ascend910b4 设备上，其指令集架构为 aarch64

- 操作指导手册：https://2024-ascend-innovation-contest-mindspore-backup.obs.cn-southwest-2.myhuaweicloud.com/2024%E6%98%87%E8%85%BEAI%E5%88%9B%E6%96%B0%E5%A4%A7%E8%B5%9BMindSpore%E8%B5%9B%E9%81%93%E5%AE%9E%E9%AA%8C%E6%8C%87%E5%AF%BC%E6%89%8B%E5%86%8C.docx
- Llama3-8b
  - checkpoint：https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/llama3-8B.ckpt
  - tokenizer文件下载链接：https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/tokenizer.model
- 微调数据集
  - 转换前：https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/train.json
  - 微调数据集转换后：https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/train-data-conversation.json
- mindspore版本下载链接（或者使用官网mindspore2.3.0RC2）：https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/mindspore-2.3.0rc2-cp39-cp39-linux_aarch64.whl
- mindformers版本下载链接：https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/mindformers.zip
- 微调配置文件参考链接：https://2024-ascend-innovation-contest-mindspore.obs.cn-southwest-2.myhuaweicloud.com/topic2-finetune/run_llama3_8b_8k_800T_A2_64G_lora_dis_256.yaml

----
by Armit
2024/06/21 
