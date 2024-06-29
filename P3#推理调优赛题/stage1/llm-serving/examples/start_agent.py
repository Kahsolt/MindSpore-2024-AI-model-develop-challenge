import sys
import argparse
from multiprocessing import Queue
from mindspore_serving.agent.agent_multi_post_method_task1 import startup_agents as startup_agents_task1
from mindspore_serving.agent.agent_multi_post_method_task2 import startup_agents as startup_agents_task2
from mindspore_serving.config.config import ServingConfig, check_valid_config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='YAML config files')
    parser.add_argument('--task', default=1, type=int)
    args = parser.parse_args()
    
    startup_queue = Queue(1024)
    config = ServingConfig(args.config)
    if not check_valid_config(config):
        sys.exit(1)
    print("load yaml sucess!")

    if args.task == 1:
        startup_agents_task1(config, startup_queue)
    elif args.task == 2:
        startup_agents_task2(config, startup_queue)

    started_agents = 0
    while True:
        value = startup_queue.get()
        print("agent : %f started" % value)
        started_agents = started_agents + 1
        if started_agents >= len(config.serving_config.agent_ports):
            print("all agents started")
            break
