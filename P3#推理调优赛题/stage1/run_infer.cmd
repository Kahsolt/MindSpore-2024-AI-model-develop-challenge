@ECHO OFF

REM To debug on Windows, you typically open three command shells:
REM   1. cd llm-serving; run examples/start_agent.py
REM   2. cd llm-serving; run examples/server_app_post.py
REM   3. cd performance_serving; run test_serving_performance.py
REM The workdir is fixed to satisfy hard-coded path config, so be careful! :(


REM launch llm-serving
CD "%WORK%\llm-serving"

REM start one by one
python examples/start_agent.py --task 1 --config configs\llama\llama_7b_kbk_pa_dyn_debug.yaml
python examples/server_app_post.py --config configs\llama\llama_7b_kbk_pa_dyn_debug.yaml


REM run performance_serving
CD "%WORK%\performance_serving"

REM test task 1
python test_serving_performance.py --task 1 -X 1 -T 5
python test_serving_performance.py --task 1 -X 1 -T 50
python test_serving_performance.py --task 1 -X 0.5 -T 200
python test_serving_performance.py --task 1 -X 0.5 -T 3000

REM test task 2
python test_serving_performance.py --task 2 -X 0.1 -T 50
python test_serving_performance.py --task 2 -X 0.1 -T 1000
