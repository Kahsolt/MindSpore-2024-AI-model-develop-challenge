#!/usr/bin/env bash

# eval pretrained ability
cd /home/ma-user/work/mindformers/mindformers/tools/dataset_preprocess/llama/
python squad_data_process.py \
  --input_file /home/ma-user/work/dev-v1.1.json \
  --output_file /home/ma-user/work/squad8192.mindrecord \
  --mode eval \
  --max_length 8192 \
  --tokenizer_type "llama3-8B"

cd /home/ma-user/work/mindformers
python run_mindformer.py \
  --config research/llama3/predict_llama3_8b_800T_A2_64G.yaml \
  --run_mode eval \
  --eval_dataset_dir /home/ma-user/work/squad8192.mindrecord \
  --load_checkpoint /home/ma-user/work/llama3-8B.ckpt \
  --epochs 1 \
  --batch_size 1 \
  --use_parallel False \
  --device_id 0 > test_eval_base.log 2>&1 &


# eval finetuned ability
cd /home/ma-user/work/mindformers/research
python llama3/run_llama3_test.py \
  --config llama3/run_llama3_8b_8k_800T_A2_64G_lora_256_eval.yaml \
  --run_mode predict \
  --use_parallel False \
  --load_checkpoint /home/ma-user/work/new_llama3_8b_lora.ckpt \
  --vocab_file /home/ma-user/work/tokenizer.model \
  --auto_trans_ckpt False \
  --input_dir "/home/ma-user/work/data_2000_1_random.json" > data_test_2000_1.log 2>&1 &
