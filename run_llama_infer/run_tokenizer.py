#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/11 

import sys
from pathlib import Path
from argparse import ArgumentParser
from typing import Union

BASE_PATH = Path(__file__).parent
MF_PATH = BASE_PATH / 'mindformers'
MFR_PATH = MF_PATH / 'research'
sys.path.insert(0, str(MF_PATH))
sys.path.insert(0, str(MFR_PATH))

import mindspore as ms
ms.set_context(mode=ms.GRAPH_MODE, device_target='CPU')
from mindformers import LlamaTokenizer, LlamaTokenizerFast
from llama3.llama3_tokenizer import Llama3Tokenizer

# use relative path ↓↓↓
TOKENIZER_V2_PATH = './checkpoint_download/llama2/tokenizer.model'
TOKENIZER_V3_PATH = './checkpoint_download/llama3/tokenizer.model'


''' CmdArgs '''
parser = ArgumentParser()
parser.add_argument('-V', '--version', default=2, type=int, choices=[2, 3], help='llama version, 2 or 3')
parser.add_argument('-F', '--vocab_file', help='path to tokenizer.model')
parser.add_argument('--fast', action='store_true', help='use fast version of llama2 tokenizer')
args = parser.parse_args()


''' Tokenzier '''
tokenizer: Union[LlamaTokenizer, LlamaTokenizerFast, Llama3Tokenizer]

if args.version == 2:
  fp = args.vocab_file or TOKENIZER_V2_PATH
  tokenizer = (LlamaTokenizerFast if args.fast else LlamaTokenizer)(fp)
elif args.version == 3:
  assert not args.fast, 'llama3 has no fast tokenzier :('
  fp = args.vocab_file or TOKENIZER_V3_PATH
  tokenizer = Llama3Tokenizer(fp)

print('>> vocab_size:', tokenizer.vocab_size)
print('>> vocab_size (with added tokens):', len(tokenizer))


''' Main Loop '''
try:
  while True:
    txt = input('>> input your sentence: ').strip()
    if not txt: continue
    ids = tokenizer.encode(txt)
    print(f'<< token_ids({len(ids)}): {ids}')
    txt_rev = tokenizer.decode(ids)
    print(f'<< txt_rev({len(txt_rev)}): {txt_rev}')
except KeyboardInterrupt:
    print('[Exit by Ctrl+C]')
