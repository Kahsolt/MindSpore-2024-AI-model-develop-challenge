#!/usr/bin/env bash

# 4 NPU launch
# see logs at /home/ma-user/work/mindformers/research/output/msrun_log/
cd /home/ma-user/work/mindformers/research/
bash ../scripts/msrun_launcher.sh \
  "llama3/run_llama3.py \
  --config /home/ma-user/work/run_llama3_8b_8k_800T_A2_64G_lora_dis_256.yaml \
  --load_checkpoint /home/ma-user/work/llama3-8B.ckpt \
  --auto_trans_ckpt False \
  --use_parallel True \
  --run_mode finetune \
  --train_data /home/ma-user/work/train-fastchat256.mindrecord" 4


# see param_cnt
cd /home/ma-user/work/mindformers/research/output/msrun_log
cat worker_0.log | grep "Network Parameters"


# merge ckpts
# see merged file at /home/ma-user/work/mindformers/research/output/checkpoint/rank_0
cd /home/ma-user/work/mindformers/
python mindformers/tools/transform_ckpt.py \
  --src_ckpt_strategy /home/ma-user/work/mindformers/research/output/strategy/ \
  --src_ckpt_dir /home/ma-user/work/mindformers/research/output/checkpoint/ \
  --dst_ckpt_dir /home/ma-user/work/mindformers/research/output/checkpoint/ \
  --prefix "new_"
