import os
import json
import time
import threading
import argparse
from typing import List

import requests
import numpy as np
from mindformers import LlamaTokenizer
import log

DEBUG_WIN = os.getenv('DEBUG_WIN')

time_now = time.strftime("%Y-%m-%d-%H_%M", time.localtime())
LOGGER = log.logger_for_test("test_llama", f"./testLog/test_performance_{time_now}.log")
LLAMA2_tokenizer = "./tokenizer.model"  # 换模型不需要换tokenizer

RESULT = []
CompletedProgress = 0
Tokenizer = LlamaTokenizer(LLAMA2_tokenizer)
HEADERS = {"Content-Type": "application/json", "Connection": "close"}


def get_text_token_num(tokenizer, text):
    tokens = tokenizer.tokenize(text)
    num_tokens = len(tokens)
    # print("token num in text is ", num_tokens)
    return num_tokens


def poisson_random_s(interval):
    poisson_random_ms = np.random.poisson(interval * 1000, 1000)[0]
    LOGGER.info(f"poisson random interval time is {poisson_random_ms / 1000}s")
    return poisson_random_ms / 1000


# 延迟tms定时器
def delayMsecond(t):
    t = t * 1000  # 传入s级别
    start, end = 0, 0
    start = time.time_ns()  # 精确至ns级别
    while end - start < t * 1000000:
        end = time.time_ns()


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)
        try:
            return json.loads(self.result)
        except Exception:
            return None


class LargeModelClient:

    def __init__(self, port):
        self.url_generate_all = f'http://localhost:{port}/models/llama2/generate'
        self.url_generate_stream = f'http://localhost:{port}/models/llama2/generate_stream'

    def send_request(self, testcase, all_counts):
        global CompletedProgress

        inputs = testcase["input"]
        # inputs = "<s><|User|>:{}<eoh>\n<|Bot|>:".format(inputs)
        para = {}
        return_full_text = testcase["return_full_text"] if "return_full_text" in testcase else False
        do_sample = testcase["do_sample"]
        max_new_tokens = testcase["max_new_tokens"] if "max_new_tokens" in testcase else False
        topk_k = testcase["topk_k"] if "topk_k" in testcase else False
        top_p = testcase["top_p"] if "top_p" in testcase else False
        temperature = testcase["temperature"] if "temperature" in testcase else False
        stream = testcase["stream"]
        if max_new_tokens:
            para["max_new_tokens"] = max_new_tokens
        if temperature:
            para["temperature"] = temperature
        if topk_k:
            para["topk_k"] = topk_k
        if top_p:
            para["top_p"] = top_p
        para["do_sample"] = do_sample
        para["return_full_text"] = return_full_text
        body = {
            "inputs": inputs,
            "parameters": para,
        }
        # print("testcase:", testcase)
        # print('body:', body)

        if stream:
            res = self.return_stream(body, stream)      # <- this way
        else:
            res = self.return_all(body, stream)
        CompletedProgress += 1

        if DEBUG_WIN:
            print(f"{res}\nTest Progress --> {CompletedProgress}/{all_counts}")
        else:
            LOGGER.info(f"{res}\nTest Progress --> {CompletedProgress}/{all_counts}")
        RESULT.append(res)
        return res

    def return_all(self, request_body, stream):
        url = self.url_generate_stream if stream else self.url_generate_all

        start_time = time.time()
        resp = requests.request("POST", url, data=json.dumps(request_body), headers=HEADERS)
        resp_text = resp.text
        resp.close()
        res_time = time.time() - start_time

        # print(resp_text)

        return {
            "input": request_body["inputs"],
            "resp_text": json.loads(resp_text)["generated_text"],
            "res_time": res_time,
        }

    def return_stream(self, request_body, stream):      # <- this way
        url = self.url_generate_stream if stream else self.url_generate_all
        return_full_text = request_body["parameters"]["return_full_text"]

        # 时间测量：请求发起 - 数据接收完毕
        start_time = time.time()
        resp = requests.request("POST", url, data=json.dumps(request_body), headers=HEADERS, stream=True)
        resp_list: List[str] = []
        resp_last: str = None
        first_token_time = None
        for i, line in enumerate(resp.iter_lines(decode_unicode=True)):
            '''
            # `line` is a json response, example:
            {
                "event":"message",
                "retry":30000,
                "data":[
                    {
                        "details":null,
                        "generated_text":"",
                        "tokens":{
                            "id":209,
                            "logprob":1.0,
                            "special":true,
                            "text":""
                        },
                        "top_tokens":[
                            {
                            "id":209,
                            "logprob":1.0,
                            "special":true,
                            "text":""
                            }
                        ]
                    }
                ]
            }
            '''
            if not line: continue
            if i == 0:
                first_token_time = time.time() - start_time
                LOGGER.info(f"first_token_time is {first_token_time}")
            if return_full_text:
                resp_last = line
            else:
                resp_list.append(line)
        res_time = time.time() - start_time

        parse = lambda resp: json.loads(resp)["data"]["generated_text"]
        if return_full_text:
            resp_text = parse(resp_last)
        else:
            resp_text = ''.join([parse(resp) for resp in resp_list])
        # print("******stream completeness result********")
        # print(resp_text)

        return {
            "input": request_body["inputs"],
            "resp_text": resp_text,
            "res_time": res_time,
            "first_token_time": first_token_time,
        }


def generate_thread_tasks(testcases, all_count, port) -> List[MyThread]:
    client = LargeModelClient(port)
    thread_tasks = []
    i = 0
    k = 0
    while True:
        #print(k, ":", all_count)
        if i > len(testcases) - 1: i = 0
        thread_tasks.append(MyThread(client.send_request, (testcases[i], all_count)))
        i += 1
        k += 1
        if k == all_count: break
    LOGGER.info(f"thread_tasks length is {len(thread_tasks)}")
    return thread_tasks


def test_main(port, inputs, outputs, x, out_dir, test_all_time=3600):
    print('start Test...')
    testcases = []
    for i, input_string in enumerate(inputs):
        testcase = {
            "input": input_string, 
            "do_sample": False, 
            "return_full_text": True, 
            "stream": True,     # <- this way
            "max_new_tokens": get_text_token_num(Tokenizer, outputs[i]),
        }
        testcases.append(testcase)
    LOGGER.info(f"testcases length is {len(testcases)}")

    # 每次发送的间隔时间
    interval = round(1 / x, 2)
    # 1h内一共需要发送多少次请求
    all_counts = int(test_all_time * x)
    print('all_counts:', all_counts)
    # 为每个推理样本生成一个线程
    thread_tasks = generate_thread_tasks(testcases, all_counts, port)

    # NOTE: 时间测量 开始第一个任务 - 结束最后一个任务
    start_time = time.time()
    LOGGER.info(f"Start send request, avg interval is {interval}")
    for task in thread_tasks:   # 顺次开始线程
        task.start()
        delayMsecond(poisson_random_s(interval))
    for task in thread_tasks:   # 等待全部完成
        task.join()
    end_time = time.time()
    LOGGER.info(f"All Tasks Done; Exec Time is {end_time - start_time}")

    if not os.path.exists(out_dir): os.makedirs(out_dir)
    save_fp = os.path.join(out_dir, f"result_{x}_x.json")
    with open(save_fp, "w+", encoding='utf-8') as fh:
        json.dump(RESULT, fh, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test serving performance")
    parser.add_argument("-X", "--qps", help='x req/s', required=True, type=float)
    parser.add_argument("-P", "--port", help='port, default is 8000', default=8835, type=int)
    parser.add_argument("-O", "--out_dir", help='dir for saving results', default="./")
    parser.add_argument("-T", "--test_time", help='test all time, default 1h', required=False, type=int, default=3600)
    parser.add_argument("--task", required=True, type=int, choices=[1, 2])
    args = parser.parse_args()

    if args.task == 1:
        fp = "./alpaca_5010.json"
    elif args.task == 2:
        fp = "./alpaca_521.json"
    with open(fp, encoding='utf-8') as fh:
        alpaca_data = json.load(fh)

    INPUTS_DATA = []
    OUTPUTS_DATA = []
    for data in alpaca_data:
        input_ = data["instruction"] + ":" + data["input"] if data["input"] else data["instruction"]
        INPUTS_DATA.append(input_)
        OUTPUTS_DATA.append(data["output"])

    test_main(args.port, INPUTS_DATA, OUTPUTS_DATA, args.qps, args.out_dir, args.test_time)
