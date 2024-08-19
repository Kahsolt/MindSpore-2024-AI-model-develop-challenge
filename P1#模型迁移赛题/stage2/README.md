# 推理性能提升

    昇思MindSpore模型开发挑战赛【模型迁移赛题】

----

基础仓库: https://github.com/mindspore-lab/mindnlp  
模型代码: https://github.com/mindspore-lab/mindnlp/tree/master/mindnlp/transformers/models  

```
[比赛规则]
在精度保持不变的情况下，进行性能比拼，单token推理时间短者胜出
精度保持不变：无法达到官方提供baseline/或模型精度降低的成绩无效，官方提供精度测试的UT
单token推理时间：测试验证1000个token推理的平均时间（不包含prefill和decode的首token）
```

| Model | File size |
| :-: | :-: |
| [BERT (base-uncase)](https://huggingface.co/google-bert/bert-base-uncased)                 | 440   MB |
| [Clip](https://huggingface.co/openai/clip-vit-base-patch32)                                | 605   MB |
| [T5 (3b)](https://huggingface.co/google-t5/t5-3b)                                          | 11.4  GB |
| [Mixtral (7b)](https://huggingface.co/mistralai/Mistral-7B-v0.1)                           | 14.48 GB |
| [Qwen2-MoE (Qwen1.5-MoE-A2.7B/Total 14.3B)](https://huggingface.co/Qwen/Qwen1.5-MoE-A2.7B) | 28.65 GB |

----
by Armit
2024/08/16 
