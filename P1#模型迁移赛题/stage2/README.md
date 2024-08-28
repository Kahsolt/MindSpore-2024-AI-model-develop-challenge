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

[优化技术]
- 绑核 (默认必开)
- 默认的 `ms.ops` 算子包改用 `ms.mint` 算子包的实现
  - 等价算子替换更优的实现方式
  - 规避很慢的算子如 `ops.Gather`
- 静态化
  - 局部静态化 `@ms.jit` (~= 一组小算子组成的函数捆绑为一个大算子)
  - 全图静态化 (适合静态 shape 模型，较难)
- 模型量化 (训练后量化)
- 自定义 Ascend 算子 (~= 写CUDA算子)
```

| Model | File size |
| :-: | :-: |
| [BERT (base-uncase)](https://huggingface.co/google-bert/bert-base-uncased)                 | 440   MB |
| [Clip](https://huggingface.co/openai/clip-vit-base-patch32)                                | 605   MB |
| [T5 (3b)](https://huggingface.co/google-t5/t5-3b)                                          | 11.4  GB |
| [Mixtral (7b)](https://huggingface.co/mistralai/Mistral-7B-v0.1)                           | 14.48 GB |
| [Qwen2-MoE (Qwen1.5-MoE-A2.7B/Total 14.3B)](https://huggingface.co/Qwen/Qwen1.5-MoE-A2.7B) | 28.65 GB |


### references

- 培训视频: https://meeting.tencent.com/v2/cloud-record/share?id=0e734e7a-a23e-4fd2-bab9-a8203abea8f7&from=3&record_type=2
- mindspore 套件文档
  - 高性能算子库 mindspore.mint: https://www.mindspore.cn/docs/zh-CN/r2.3.1/api_python/mindspore.mint.html
  - 静态图
    - https://www.mindspore.cn/docs/zh-CN/r2.3.1/note/static_graph_syntax_support.html
    - https://www.mindspore.cn/tutorials/zh-CN/r2.3.1/beginner/accelerate_with_static_graph.html
  - 模型压缩 Golden Stick: https://www.mindspore.cn/golden_stick/docs/zh-CN/r0.5.0/index.html
  - 自定义算子: https://www.mindspore.cn/tutorials/experts/zh-CN/r2.3.1/operation/op_custom.html

----
by Armit
2024/08/16 
