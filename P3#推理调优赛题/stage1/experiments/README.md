# 实验

    如无特殊说明，这些实验应该顺序进行

----

```
时间开销比例 [service : model = 1 : 2]
llm-serving time: 3513.11s = 58.55min
mindformer  time: 2395.26s = 39.92min
overhead:                    18.63min
```

----

### run_llama_infer 测试

> 环境: 云端

参考 [run_llama_infer](./run_llama_infer/) 目录


### 基线复现

> 环境: 云端/本地

参考 [baseline_reproduce](./baseline_reproduce/README.md) 目录


### 裸跑测试 / 打桩测试

> 环境: 本地/云端

参考 [bare_run](./bare_run/README.md) 目录


### lprof 测试

> 环境: 本地

参考 [lprof](./lprof/README.md) 目录
