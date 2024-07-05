#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/04 

# 挑选训练数据
# - 中文 80w + 英文 9993 = 总计 809993
# - 中文都是小学数学模板式简短问答
# - 英文是长问答，基本定论不可能回答正确

from argparse import ArgumentParser
from utils import *
from judger import get_problem_template


def stats_pattern_problem_count():
  # [359347, 39207, 39227, 45, 19709, 40080, 20028, 8665, 100, 6275, 6266]
  pairs_raw_ch = load_dataset_raw()
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


def write_data_subset(subset, fp:Path):
  print(f'>> write file: {fp}')
  with open(fp, 'w', encoding='utf-8') as fh:
    for s in subset:
      qa = { 'problem': s[0], 'solution': s[1] }
      fh.write(json.dumps(qa, ensure_ascii=False, indent=None))
      fh.write('\n')


def make_testset():
  if DATASET_TEST_FILE.exists():
    print('>> ignore due to file exists')
    return
  samples = load_dataset_raw()
  subset = random.sample(samples, 200)
  write_data_subset(subset, DATASET_TEST_FILE)


def make_trainset_uniform_pick():
  # [359347, 39207, 39227, 45, 19709, 40080, 20028, 8665, 100, 6275, 6266]
  pairs_raw_ch = load_dataset_raw()
  pattern_problems: Dict[int, List] = {}
  for prb, ans in pairs_raw_ch:
    idx, tmpl = get_problem_template(prb, ans)
    if idx not in pattern_problems:
      pattern_problems[idx] = []
    pattern_problems[idx].append((prb, ans))

  subset = []
  for i in range(11):
    subprbs = pattern_problems[i]
    if i == 0:
      st = random.sample(subprbs, 5000)
    elif len(subprbs) < 1000:
      st = subprbs
    else:
      st = random.sample(subprbs, 1500)
    st.sort()
    subset.extend(st)
  nlen = len(subset)
  print('len(subset):', nlen)

  write_data_subset(subset, BASE_PATH / f'data_uniform_pick_{nlen}.json')


if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--split', default='test', choices=['test', 'train'])
  parser.add_argument('--maker', choices=['uniform_pick'])
  args = parser.parse_args()

  suffix = f'_{args.maker}' if args.maker else ''
  maker = globals()[f'make_{args.split}set{suffix}']
  maker()
