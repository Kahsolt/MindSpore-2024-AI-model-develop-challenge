# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np


def main(args_param):
    # npy 文件夹路径，
    base_path = args_param.base_path  # 基准npy文件的路径
    new_path = args_param.new_path  # 新生成的npy文件的路径

    # 使用os.listdir()函数读取文件夹中的所有文件和子文件夹
    files_b = sorted(os.listdir(base_path))     # keep sorted by timestamp
    files_n = sorted(os.listdir(new_path))

    print("基准npy文件数量：", len(files_b))
    print("新生成的npy文件的数量：", len(files_n))
    if len(files_b) != len(files_n):        # nlen = 214
        print(f"WARN: length mismatch files_new {len(files_n)} != files_base {len(files_b)}")

    res_list = []
    for index, v_n in enumerate(files_n):
        print(f"[{index+1}/{len(files_n)}] ", end='')
        v_b = files_b[index]
        s_n = v_n.split('_')
        s_b = v_b.split('_')
        if s_b[1] == s_n[1] and s_b[2] == s_n[2]:
            data_b = np.load(os.path.join(base_path, v_b), allow_pickle=True)
            data_n = np.load(os.path.join(new_path, v_n),  allow_pickle=True)

            if not 'original element-wise implementation':
                if len(data_b.shape) == 3:
                    da = [tensor.asnumpy() for tensor in data_b[0][0]]
                    da1 = [tensor.asnumpy() for tensor in data_n[0][0]]
                elif len(data_b.shape) == 2:
                    da = [tensor.asnumpy() for tensor in data_b[0]]
                    da1 = [tensor.asnumpy() for tensor in data_n[0]]
            else:
                da = data_b.astype(np.float32)
                da1 = data_n.astype(np.float32)

            res = np.allclose(da, da1, atol=5e-03, equal_nan=False)
            res_list.append(res)
            print("pass" if res else "FAILED FAILED FAILED!!")

    print(f">> Done: {sum(res_list)} / {len(files_n)} / {len(files_b)} (passed / tested / total)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_path", type=str, default="file_npy_base")
    parser.add_argument("--new_path", type=str, default="file_npy_new")
    args = parser.parse_args()
    main(args)
