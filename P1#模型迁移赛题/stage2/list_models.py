#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/08/19 

import os
os.environ['MINDNLP_CACHE'] = './mindnlp/.mindnlp'

import mindspore as ms
from mindnlp.transformers import *

get_param_cnt = lambda model: sum(x.numel() for x in model.parameters() if x.requires_grad)

print('[Param Cnt]')

# https://huggingface.co/google-bert/bert-base-uncased (440MB)
model = BertModel.from_pretrained('google-bert/bert-base-uncased')
pcnt = get_param_cnt(model)
print(f'  Bert: {pcnt}')    # => 109482240

# https://huggingface.co/openai/clip-vit-base-patch32 (605MB)
#model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
#tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-base-patch32")
#print(f'  CLIP: {pcnt}')

# https://huggingface.co/google-t5/t5-3b (11.4GB)
#model = T5Model.from_pretrained('google-t5/t5-3b')
#print(f'  T5: {pcnt}')

# https://huggingface.co/mistralai/Mistral-7B-v0.1 (14.48GB)
#model = MixtralForCausalLM.from_pretrained('mistralai/Mistral-7B-v0.1')
#print(f'  Mixtral: {pcnt}')

# https://huggingface.co/Qwen/Qwen1.5-MoE-A2.7B (28.65GB)
#model = Qwen2MoeForCausalLM.from_pretrained("Qwen/Qwen1.5-MoE-A2.7B", ms_dtype=ms.float16, mirror='gitee')
#tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-MoE-A2.7B", use_fast=False)
#print(f'  Qwen2MoE: {pcnt}')
