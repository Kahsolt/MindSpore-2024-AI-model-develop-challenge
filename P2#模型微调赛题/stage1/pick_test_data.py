#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/05 

# 做一个本地测试集 (200样例)

from utils import *

import random
import numpy as np
SEED = 114514
random.seed(SEED)
np.random.seed(SEED)

samples = load_dataset_raw()
subset = random.sample(samples, 200)

print(f'>> write file: {DATASET_TEST_FILE}')
with open(DATASET_TEST_FILE, 'w', encoding='utf-8') as fh:
  for s in subset:
    qa = {
      'problem': s[0],
      'solution': s[1],
    }
    fh.write(json.dumps(qa, ensure_ascii=False, indent=None))
    fh.write('\n')
