import warnings ; warnings.filterwarnings(action='ignore', category=UserWarning)

import os
import numpy as np
import argparse


def extract_file_segment(file_names, separater="_"):
    file_seg_dict = {}
    for file_name in file_names:
        pred_time, seq, token = file_name.split(separater)
        output_id = f"{seq}_{token}"
        if output_id not in file_seg_dict.keys():
            file_seg_dict[output_id] = [file_name]
        else:
            file_seg_dict[output_id].append(file_name)
            file_seg_dict[output_id] = sorted(file_seg_dict[output_id])
    print("=========== 完成文件名字段提取与重排 =============")
    return file_seg_dict


def check_file_length(files_new, files_base):
    if len(files_new) != len(files_base):
        raise ValueError(f"生成logits文件数量({len(files_new)})与基线logits文件数量({len(files_base)})不符，请重新检查数据。")
    else:
        # 如果条件满足，我们正常执行后续代码
        print("数据长度满足条件，继续下面操作。")


def find_deepest_ndarray(arr):  
    if isinstance(arr, np.ndarray) and arr.ndim > 0:  # 检查arr是否是NumPy数组且不是零维数组  
        # 假设arr内只有一个元素，且这个元素是NumPy数组  
        first_element = arr[0]  
        if isinstance(first_element, np.ndarray):  # 如果第一个元素是NumPy数组，则递归查找  
            return find_deepest_ndarray(first_element)  
        else:  # 如果第一个元素不是NumPy数组，那么arr就是最深层的数组  
            return arr  
    else:  
        # 如果arr不是NumPy数组或者已经是零维数组，返回None或者抛出异常（取决于你的需求）  
        return None 


class LogitsChecker:

    def __init__(self, file_seg_dict_new, file_seg_dict_base):
        self.correct_num = 0  # 正确匹配数
        self.unmatched_groups = []  # 未匹配logits对
        self.file_seg_dict_new = file_seg_dict_new
        self.file_seg_dict_base = file_seg_dict_base

    def _check_logits(self, logits_new_path, logits_base_path):
        # 获取logits文件
        logits_new = np.load(logits_new_path, allow_pickle=True)
        logits_base = np.load(logits_base_path, allow_pickle=True)
        logits_new = logits_new                       # NOTE: we directly saved NDdarray[np.float32] :)
        logits_base = logits_base.astype(np.float32)  # NDdarray[ms.Tensor] to NDdarray[np.float32]

        # logits验证，绝对值千分之五
        res = np.allclose(logits_new, logits_base, atol=5e-03, equal_nan=False)

        if res:
            self.correct_num += 1
            print("精度验证通过！")
        else:
            self.unmatched_groups.append([logits_base_path, logits_new_path])
            print("精度验证失败！")
            # print(f"如下为两个logits文件：\n选手生成: {logits_new[0]} \n基线：{logits_base[0]}")
        
        return res

    def check_logits(self, base_path, new_path):
        print("=========== 开始检查logits =============")
        for key_base, values_base in self.file_seg_dict_base.items():
            print(f"当前序列与token编号: {key_base}")
            if key_base not in self.file_seg_dict_new.keys():
                print("----------无法在选手生成的logits文件中找到符合的文件，请重新检查数据。----------")
                self.unmatched_groups.append([value_base, 'Null'] for value_base in values_base)
                continue
            for value_base in values_base:
                curr_value_new = self.file_seg_dict_new[key_base].pop(0)
                print(f"基线文件：{value_base} vs 选手生成文件：{curr_value_new}")
                logits_new_path = os.path.join(new_path, curr_value_new)
                logits_base_path = os.path.join(base_path, value_base)
                res = self._check_logits(logits_new_path, logits_base_path)

    def __call__(self, *args, **kwargs):
        base_path, new_path = args
        self.check_logits(base_path, new_path)


def main(args_param):
    # npy 文件夹路径，
    base_path = args_param.base_path  # 基准npy文件的路径
    new_path = args_param.new_path  # 新生成的npy文件的路径

    # 使用os.listdir()函数读取文件夹中的所有文件和子文件夹
    files_b = os.listdir(base_path)
    files_n = os.listdir(new_path)

    print("=========== 检查基线logits文件数量与选手生成logits文件数量 =============")

    print("基准npy文件数量：", len(files_b))
    print("新生成的npy文件的数量：", len(files_n))

    check_file_length(files_n, files_b)

    print("=========== 开始进行选手生成文件名字段提取与重排 =============")
    seg_dict_n = extract_file_segment(files_n)
    print("=========== 开始进行基线文件名字段提取与重排 =============")
    seg_dict_b = extract_file_segment(files_b)

    logits_checker = LogitsChecker(seg_dict_n, seg_dict_b)
    logits_checker(base_path, new_path)

    if logits_checker.correct_num == len(files_b):
        print("模型精度OK，通过测试。")
    else:
        print(f"模型精度不OK，测试不通过。{logits_checker.correct_num}/{len(files_b)}")
        print("未匹配的logits对如下：")
        for unmatched_group in logits_checker.unmatched_groups:
            unmatched_group_list = list(unmatched_group)
            print(f"基线文件：{unmatched_group_list[0][0]}, 选手生成文件：{unmatched_group_list[0][1]}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_path", type=str, default="file_npy_base")
    parser.add_argument("--new_path", type=str, default="file_npy")
    args = parser.parse_args()

    main(args)
