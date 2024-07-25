#!/usr/bin/env bash

## ↓↓↓ 数据准备

# data source
export TRAIN_DATA_DB=train-unipick17145.mindrecord
export TRAIN_DATA_IN_JSON=data_uniform_pick_17145.json
export TRAIN_DATA_OUT_JSON=data_uniform_pick_17145.out.json

export TRAIN_DATA_DB=train-arith15000.mindrecord
export TRAIN_DATA_IN_JSON=data_arith_15000.json
export TRAIN_DATA_OUT_JSON=data_arith_15000.out.json

# make train data db
cd /home/ma-user/work/
python data_converter.py \
  --data_path /home/ma-user/work/$TRAIN_DATA_IN_JSON \
  --output_path /home/ma-user/work/$TRAIN_DATA_OUT_JSON

cd /home/ma-user/work/mindformers/research/llama3
python llama_preprocess.py \
  --dataset_type qa \
  --input_glob /home/ma-user/work/$TRAIN_DATA_OUT_JSON \
  --model_file /home/ma-user/work/tokenizer.model \
  --seq_length 256 \
  --output_file /home/ma-user/work/$TRAIN_DATA_DB


#############################################################################################################


## ↓↓↓ 训练

# 1 NPU launch
# see logs at /home/ma-user/work/mindformers/research/output/log/rank_0/info.log
# see middle checkpoint at /home/ma-user/work/mindformers/research/output/checkpoint/
# see final checkpoint at /home/ma-user/work/mindformers/research/output/checkpoint_network/
cd /home/ma-user/work/mindformers/research/
python llama3/run_llama3.py \
  --config llama3/run_llama3_8b_8k_800T_A2_64G_lora_dis_256_single.yaml \
  --load_checkpoint /home/ma-user/work/llama3-8B.ckpt \
  --auto_trans_ckpt False \
  --run_mode finetune \
  --train_data /home/ma-user/work/$TRAIN_DATA_DB

# see param_cnt
cat /home/ma-user/work/mindformers/research/output/log/rank_0/info.log | grep "Network Parameters"

# save run outputs
mkdir /home/ma-user/work/finetune_logs
mv /home/ma-user/work/mindformers/research/output /home/ma-user/work/finetune_logs/run-[REPLACE_WITH_ID]
