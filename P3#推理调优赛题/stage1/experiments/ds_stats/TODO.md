# 测试数据集统计信息

这个比赛是测试性能的，所以我们也需要知道测试数据的大概统计情况

要解决的问题：

- 统计测试数据集句子长度 (以token数量计)

实际需要做的：

- 测试数据在 performance_serving\alpaca_5010.json 和 performance_serving\alpaca_521.json
  - 仔细阅读相关的 README.md 文件，知道哪个数据集是分别对应 task1/task2，且测试时只取固定前 1500/500 条
- 补全本目录下的脚本 vis_stats.py
  - 脚本输入 `-T, --task <1|2>` 输出一堆图和json在 `<filename>\` 目录下
  - 你需要首先初始化一个分词器，参考 performance_serving\test_serving_performance.py 第 21 行
  - 然后读取数据集，预处理参考 performance_serving\test_serving_performance.py 第 269 行
  - 分析样本的 token 序列长度
    - 画直方图 plt.hist
    - 排序后画折线图 plt.plot
    - 统计句子长度的 最大、最小、平均、中位数、众数、方差、标准差 保存为 json
    - 输入句子和输出句子分别统计 plt.subplot

提交内容：

本目录下的代码和生成的统计图表数据
