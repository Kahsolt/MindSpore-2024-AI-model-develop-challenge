@ECHO OFF

REM make a tiny dataset (128 samples)
CD "%WORK%\mindformers\research\llama3"
python llama_preprocess.py ^
  --dataset_type qa ^
  --input_glob "%WORK%\material\train-data-conversation_128.json" ^
  --model_file "%WORK%\mindformers\checkpoint_download\llama\tokenizer.model" ^
  --seq_length 256 ^
  --output_file "%WORK%\material\train-fastchat256_128.mindrecord"


REM run a tiny train
CD "%WORK%\mindformers\research"
python llama3/run_llama3.py ^
  --config "%WORK%\mindformers\research\llama3\run_llama3_8b_debug.yaml" ^
  --train_data "%WORK%\material\train-fastchat256_128.mindrecord" ^
  --auto_trans_ckpt False ^
  --use_parallel False ^
  --run_mode finetune
