# 写绘图脚本

要解决的问题：

模型推理脚本 test_serving_performance.py 跑完之后会产生于一个 result_*_x.json 文件  
包含了每个测试样例的请求 发送-接收 时间，把它们画出来  

实际需要做的：

- 补全本目录下的 `plot_res_time.py` 脚本
- 脚本输入 `-I, --in_fp <*.json>` 输出 `-O, --out_fp <*.png>`
- 输入文件格式参考 [./task1/result_0.5_x.json](./task1/result_0.5_x.json) 和 [./task2/result_1_x.json](./task2/result_0.1_x.json)
- 对 json 文件中的 first_token_time 和 res_time 字段，输出 plt.plot 绘图

提交应该包含：

- `plot_res_time.py`
- `./task1/result_0.5_x.png`
- `./task2/result_0.1_x.json`
