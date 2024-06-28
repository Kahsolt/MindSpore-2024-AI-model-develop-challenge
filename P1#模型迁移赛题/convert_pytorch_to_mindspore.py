#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/02/05

# naive trans-literation from PyTorch to Mindspore

import sys
from pathlib import Path

# read
fp = Path(sys.argv[1])
assert fp.is_file() and fp.suffix == '.py'
with open(fp, 'r', encoding='utf-8') as fh:
  text = fh.read()


# process
if 'class/func name diff':
  text = text.replace('def forward(', 'def construct(')
  text = text.replace('nn.Module', 'nn.Cell')
  text = text.replace('nn.Linear', 'nn.Dense')
  text = text.replace('torch.tensor', 'mindspore.tensor')
  text = text.replace('torch.from_numpy', 'Tensor.from_numpy')
  text = text.replace('torch.Tensor', 'mindspore.Tensor')
  text = text.replace('torch.LongTensor', 'mindspore.Tensor')
  text = text.replace('torch.FloatTensor', 'mindspore.Tensor')
  text = text.replace('torch.BoolTensor', 'mindspore.Tensor')
  text = text.replace('torch.bool', 'mindspore.bool_')
  text = text.replace('torch.float32', 'mindspore.float32')
  text = text.replace('torch.long', 'mindspore.int64')
  text = text.replace('torch.manual_seed(', 'mindspore.set_seed(')
  text = text.replace('is_torch_available', 'is_mindspore_available')
  text = text.replace('require_torch', 'require_mindspore')
  text = text.replace('require_torchaudio', 'require_librosa')
  text = text.replace('require_soundfile', 'require_librosa')
  text = text.replace('for param in self.parameters()', 'for name, param in self.parameters_and_names()')
if 'func usage diff':
  text = text.replace('.train()', '.set_train(True)')
  text = text.replace('.eval()', '.set_train(False)')
  text = text.replace('.transpose(', '.swapaxes(')
  text = text.replace('.size()', '.shape')
if 'func param diff':
  text = text.replace('nn.Dropout(', 'nn.Dropout(p=')
  text = text.replace('return_tensors="pt"', 'return_tensors="ms"')
  text = text.replace('bias=', 'has_bias=')
  text = text.replace(', eps=', ', epsilon=')
  text = text.replace(', dim=', ', axis=')
  text = text.replace('.size(-1)', '.shape[-1]')
  text = text.replace('.size(0)', '.shape[0]')
  text = text.replace('.size(1)', '.shape[1]')
  text = text.replace('.size(2)', '.shape[2]')
  text = text.replace('.size(3)', '.shape[3]')
  text = text.replace('.size(4)', '.shape[4]')
if 'do not need':
  text = text.replace('.cuda()', '')
  text = text.replace('.cpu()', '')
  text = text.replace('.numpy()', '')
  text = text.replace('.detach()', '')
  text = text.replace('.contiguous()', '')
  text = text.replace('.to(device)', '')
  text = text.replace('.to(torch_device)', '')
  text = text.replace(', device=torch_device', '')
  text = text.replace('with torch.no_grad():', '# TODO: remove line')
if 'lib diff':
  text = text.replace('torch.allclose', 'np.allclose')
  text = text.replace('torch.finfo', 'np.finfo')
  text = text.replace('torch.', 'ops.')
if 'fix back':
  text = text.replace('.argmax(logits, axis=', '.argmax(logits, dim=')
  text = text.replace('.argmax(outputs, axis=', '.argmax(outputs, dim=')
if 'strings':
  text = text.replace('PyTorch', 'MindSpore')
if 'imports':
  text = text.replace('from ...utils import', 'from ....utils import')


# write
MS_IMPORTS = '''
import numpy as np
import mindspore
from mindspore import ops
import mindspore.nn as nn
from mindspore.nn import CrossEntropyLoss

from mindnlp.modules.functional import finfo
'''

with open(fp, 'w', encoding='utf-8') as fh:
  fh.write(MS_IMPORTS + text)

print('> Done!')
