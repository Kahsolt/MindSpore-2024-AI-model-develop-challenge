# 推理性能提升

    昇思MindSpore模型开发挑战赛【模型迁移赛题】

----

```
[比赛规则]
在精度保持不变的情况下，进行性能比拼，单token推理时间短者胜出
精度保持不变：无法达到官方提供baseline/或模型精度降低的成绩无效，官方提供精度测试的UT
单token推理时间：测试验证1000个token推理的平均时间（不包含prefill和decode的首token）
```

- Stage-2 task:
  - BERT(base-uncase): https://github.com/mindspore-lab/mindnlp/tree/master/mindnlp/transformers/models/bert
  - Mixtral(7b): https://github.com/mindspore-lab/mindnlp/tree/master/mindnlp/transformers/models/mixtral
  - Clip: https://github.com/mindspore-lab/mindnlp/tree/master/mindnlp/transformers/models/clip
  - T5(3b): https://github.com/mindspore-lab/mindnlp/tree/master/mindnlp/transformers/models/t5
  - Qwen2-MoE(Qwen1.5-MoE-A2.7B/Total 14.3B): https://github.com/mindspore-lab/mindnlp/tree/master/mindnlp/transformers/models/qwen2_moe

----
by Armit
2024/08/16 
