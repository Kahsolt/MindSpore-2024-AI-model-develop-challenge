#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/04 

# 挑选训练数据
# - 中文 80w + 英文 9993 = 总计 809993
# - 中文都是小学数学模板式简短问答
# - 英文是长问答，基本定论不可能回答正确

from utils import *

pairs_raw_ch = load_dataset_raw()

# [359347, 39207, 39227, 45, 19709, 40080, 20028, 8665, 100, 6275, 6266]
pattern_problem_count = [0] * len(PROBLEM_TEMPLATES)
for prb, ans in pairs_raw_ch:
  matched = False
  for idx, tmpl in enumerate(PROBLEM_TEMPLATES):
    if tmpl['Q'].match(prb) and tmpl['A'].match(ans):
      pattern_problem_count[idx] += 1
      matched = True
      break
  if not matched:
    print(prb, ans)

print('[pattern_problem_count]')
print(pattern_problem_count)
