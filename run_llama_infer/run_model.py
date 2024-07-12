#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/12 

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
from mindformers import MindFormerConfig, LlamaConfig, LlamaForCausalLM

# use relative path ↓↓↓
TOKENIZER_V2_PATH = './checkpoint_download/llama2/tokenizer.model'
TOKENIZER_V3_PATH = './checkpoint_download/llama3/tokenizer.model'
CKPT_V2_PATH = './checkpoint_download/llama2/llama2_7b.ckpt'
CKPT_V3_PATH = './checkpoint_download/llama3/llama3_8b.ckpt'
CONFIG_V2_PATH = './predict_llama2_7b.yaml'
CONFIG_V3_PATH = './predict_llama3_8b.yaml'


''' CmdArgs '''
parser = ArgumentParser()
parser.add_argument('-V', '--version', default=2, type=int, choices=[2, 3], help='llama version, 2 or 3')
parser.add_argument('-C', '--cfg_file', help='path to predict_llama_*.yaml')
parser.add_argument('-F', '--vocab_file', help='path to tokenizer.model')
parser.add_argument('--fast', action='store_true', help='use fast version of llama2 tokenizer')
parser.add_argument('-M', '--ckpt_file', help='path to llama_*.ckpt checkpoint')
parser.add_argument('--skip_load', action='store_true', help='skip load llama_*.ckpt')
parser.add_argument('--seq_length', default=16, type=int, help='seq_length')
parser.add_argument('--max_length', default=8, type=int, help='max length for predict output')
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
tokenizer: Union[LlamaTokenizer, LlamaTokenizerFast, Llama3Tokenizer]


''' Model '''
if args.version == 2:
  fp = args.cfg_file or CONFIG_V2_PATH
elif args.version == 3:
  fp = args.cfg_file or CONFIG_V3_PATH
config = MindFormerConfig(fp)
model_config = LlamaConfig(**config.model.model_config)
model_config.seq_length = args.seq_length           # = total_workspace_len = input_len + max_ouput_len
model_config.max_decode_length = args.max_length    # = max_ouput_len
if args.skip_load:
  model_config.checkpoint_name_or_path = None
model = LlamaForCausalLM(model_config)


''' Main Loop '''
try:
  while True:
    txt = input('>> input your sentence: ').strip()
    if not txt: continue
    inputs = tokenizer.encode(txt)
    print(f'>> input_ids({len(inputs)}): {inputs}')
    outputs = model.generate(inputs, max_new_tokens=model_config.max_decode_length, do_sample=False)[0]
    print(f'>> output_ids({len(outputs)}): {outputs}')
    generated = tokenizer.decode(outputs)
    print(f'>> generated({len(generated)}): {generated}')
except KeyboardInterrupt:
  print('[Exit by Ctrl+C]')
