#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/31 

# 验证是否调度中存在气泡：假定单 token 推理时间固定，模拟计算给定请求序列的最小耗时
# 结论: 气泡时间不到 2%，根本原因还是序列太长，模型推理推理时间瓶颈

import json
from tqdm import tqdm
from mindformers import LlamaTokenizer

# 单 token 推理时间
#RTS = 0.04      # 依 llm-serving
RTS = 0.025     # 依 mindformers
# 每秒请求数量
QPS = 0.5


tokenizer = LlamaTokenizer("../../performance_serving/tokenizer.model")
with open("../../performance_serving/alpaca_5010.json", "r", encoding="utf-8") as fh:
  alpaca_data = json.load(fh)[:1500]

output_token_lengths = []
for data in tqdm(alpaca_data):
  input_ = data["instruction"] + ":" + data["input"] if data["input"] else data["instruction"]
  output_token_lengths.append(len(tokenizer.tokenize(data["output"])))

ts_total = 0
ts_infer = 0
ts_bubble = 0
for length in output_token_lengths:
  sample_ts = length * RTS
  ts_infer += sample_ts
  if sample_ts < QPS:
    ts_bubble += QPS - sample_ts
  ts_total += max(sample_ts, QPS)

# [RTS = 0.04]
# infer  time: 3923.44s (98.183%)
# bubble time:   72.58s (1.816%)
# total  time: 3996.02s
# [RTS = 0.025]
# infer  time: 2452.15
# bubble time:  118.575
# total  time: 2570.725
print('infer  time:', ts_infer)
print('bubble time:', ts_bubble)
print('total  time:', ts_total)
