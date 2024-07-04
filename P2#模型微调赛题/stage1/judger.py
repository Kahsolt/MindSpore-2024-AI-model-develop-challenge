#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/05 

'''
NOTE: 完成这个脚本，需要先学习正则表达式的 匹配match 和 提取findall
'''

import numpy as np
from utils import *

# 浮点数误差容忍阈值
EPS = 1e-8


def check_match(problem:str, solution:str, predict:str) -> bool:
  return predict == solution


def check_correct(problem:str, solution:str, predict:str) -> bool:
  '''
    假设模型输入问题 problem，标准答案 solution，模型输出 predict，本函数判断该 predict 是否符合回答模板，并且数学意义上计算准确
    在这个函数里你需要
      1. 判断 problem 符合哪个模板，参考 PROBLEM_TEMPLATES 中的 Q 模板
      2. 判断 predict 是否符合对应的 A 模板
      3. 判断 predict 中数值与 solution 相比是否准确
    回答 "正确" 的定义：
      - predict 中的数学运算结果与 solution 一致
      - 这意味着要把其中的浮点数字符串抽取出来，转换为真的 float 类型，然后用 np.isclose 比较 (误差阈值为EPS)
      - 具体比较哪一部分因问题模板而异，因此会有一个很大的 if-else 结构
  '''

  return False


def get_acc(problems:List[str], solutions:List[str], predicts:List[str], strict:bool=True) -> float:
  '''
    本函数计算一组输入输出的平均正确率
     - strict=True 时调用 check_match
     - strict=False 时调用 check_correct
  '''
  return 0.0



if __name__ == '__main__':
  # 你的代码实现应该能通过下述单元测试 :)

  problems = [
    '解方程 -1x + -17 = 0',
    '计算 -7431.41 / 6769.29 等于多少？',
    '求以下数据的平均值：[70, 18, 94]',
    '去年销售额为 32 万元，今年销售额增加了 28%，请计算今年的销售额。',
  ]
  solutions = [
    '方程的解为：-17.0',
    '-7431.41 / 6769.29 = -1.097812325960329665297246831',
    '平均值为 60.666666666666664',
    '40.96',
  ]
  predicts = [
    '方程的解为：-17.0',
    '-7431.41 / 6769.29 = -1.0978123333333333333',
    '平均值为 60.666666666666666',
    '40.96000',
  ]
  assert np.isclose(get_acc(problems, solutions, predicts, strict=True ), 1/4, atol=EPS)
  assert np.isclose(get_acc(problems, solutions, predicts, strict=False), 3/4, atol=EPS)
