# -*- coding: utf-8 -*-

import numpy as np
import os
import argparse


def main(args_param):
    # npy 文件夹路径，
    base_path = args_param.base_path  # 基准npy文件的路径
    new_path = args_param.new_path  # 新生成的npy文件的路径

    # 使用os.listdir()函数读取文件夹中的所有文件和子文件夹
    files_b = os.listdir(base_path)
    files_n = os.listdir(new_path)

    print("基准npy文件数量：", len(files_b))
    print("新生成的npy文件的数量：", len(files_n))

    if len(files_b) != len(files_n):
        raise ValueError("两个数据结果长度不等，请重新检查数据。")
    else:
        # 如果条件满足，我们正常执行后续代码
        print("数据长度满足条件，继续下面操作。")

    res_list = []

    for index, v_b in enumerate(files_b):
        print("处理到：", index)
        # print(v_b)
        v_n = files_n[index]
        # print(v_n)
        s_b = v_b.split('_')
        s_n = v_n.split('_')
        if s_b[1] == s_n[1] and s_b[2] == s_n[2]:
            data_b = np.load(os.path.join(base_path, v_b), allow_pickle=True)
            data_n = np.load(os.path.join(new_path, v_n), allow_pickle=True)

            if len(data_b.shape) == 3:
                da = [tensor.asnumpy() for tensor in data_b[0][0]]
                da1 = [tensor.asnumpy() for tensor in data_n[0][0]]
            elif len(data_b.shape) == 2:
                da = [tensor.asnumpy() for tensor in data_b[0]]
                da1 = [tensor.asnumpy() for tensor in data_n[0]]

            res = np.allclose(da, da1, atol=5e-03, equal_nan=False)
            if res:
                print("精度验证通过！")
            else:
                print("精度验证失败！")
            
            res_list.append(res)

    if sum(res_list) == len(files_b):
        print("模型精度OK，通过测试。")
    else:
        print("模型精度不OK，测试不通过。")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--base_path", type=str, default="file_npy_base")
    parser.add_argument("--new_path", type=str, default="file_npy_new")
    args = parser.parse_args()
    main(args)




