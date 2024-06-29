@ECHO OFF

REM To debug on Windows, you typically open three command shells:
REM   1. cd llm-serving; run examples/start_agent.py
REM   2. cd llm-serving; run examples/server_app_post.py
REM   3. cd performance_serving; run test_serving_performance.py
REM The %workdir% is fixed to satisfy hard-coded path config, so be careful! :(


REM launch llm-serving
CD "%WORK%\llm-serving"

REM start services one by one
python examples/start_agent.py --task 1 --config configs\llama\llama_7b_kbk_pa_dyn_debug.yaml
python examples/server_app_post.py --config configs\llama\llama_7b_kbk_pa_dyn_debug.yaml

REM test llm-serving
curl 127.0.0.1:8835/models/llama2/generate ^
  -X POST ^
  -d "{\"inputs\":\" I love Beijing, because\",\"parameters\":{\"max_new_tokens\":56, \"do_sample\":\"True\", \"return_full_text\":\"True\"}, \"stream\":\"True\"}" ^
  -H "Content-Type: application/json"


REM run performance_serving
CD "%WORK%\performance_serving"

REM test task 1 (--task should match with start_agent.py)
python test_serving_performance.py --task 1 -X 1 -T 1
python test_serving_performance.py --task 1 -X 1 -T 5
python test_serving_performance.py --task 1 -X 1 -T 50
python test_serving_performance.py --task 1 -X 0.5 -T 100
python test_serving_performance.py --task 1 -X 0.5 -T 200

REM test task 2 (--task should match with start_agent.py)
python test_serving_performance.py --task 2 -X 0.2 -T 250
python test_serving_performance.py --task 2 -X 0.1 -T 500


REM test precision
CD "%WORK%"
python acc_allclose.py --base_path file_npy_base --new_path file_npy
