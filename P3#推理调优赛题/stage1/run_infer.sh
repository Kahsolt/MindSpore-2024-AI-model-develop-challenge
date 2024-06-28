#!/usr/bin/env bash

# launch llm-serving (~5min)
# see logs under /home/ma-user/work/llm-serving, agent.log and server.log
# occasionally fails due to OOM, just try again :(
cd /home/ma-user/work/llm-serving/
python examples/start.py --task 1 --config /home/ma-user/work/llm-serving/configs/llama/llama_7b_kbk_pa_dyn.yaml

# test llm-serving
curl 127.0.0.1:8835/models/llama2/generate \
  -X POST \
  -d '{"inputs":" I love Beijing, because","parameters":{"max_new_tokens":56, "do_sample":"True", "return_full_text":"True"}, "stream":"True"}' \
  -H 'Content-Type: application/json'

# run performance_serving
cd /home/ma-user/work/performance_serving/

# test task 1
python test_serving_performance.py --task 1 -X 1 -T 5
python test_serving_performance.py --task 1 -X 0.5 -T 3000

# TODO: kill, reconfigure and restart llm-serving!!
ps -elf | grep python
kill -9 xxx
# swap filename under llm-serving\mindspore_serving\agent
#   - `agent_multi_post_method_save_logits.py`
#   - `agent_multi_post_method.py`

# test task 2
python test_serving_performance.py --task 2 -X 0.2 -T 25
python test_serving_performance.py --task 2 -X 0.1 -T 5000


# you can modify `test.sh`, then run with nohup for these two task!!
nohup sh test.sh > task1.log 2>&1 &
