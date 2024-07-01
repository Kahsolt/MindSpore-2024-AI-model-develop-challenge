# wtm 到底哪里卡了

复现本目录下的实验 RUN_LEVEL=1~6，分析整理数据，看哪个等级差之间时间差最大

推荐使用的 test_serving_performance.py 配置

```
-X 1 -T 30
-X 3 -T 10
-X 10 -T 3
-X 30 -T 1
```

注意到 llm-serving\examples\server_app_post.py 的默认请求走的是 SSE 协议 + /generate_stream  
再测一下另外三种情况：


```
        SSE        |        SSE        |
  /generate_stream |     /generate     |
----------------------------------------
      non-SSE      |      non-SSE      |
  /generate_stream |     /generate     |
```

修改 performance_serving\test_serving_performance.py 的第 219 行实现 stream=False 
修改 performance_serving\test_serving_performance.py 的第 278 行实现 non-SSE (随便乱改就行)
