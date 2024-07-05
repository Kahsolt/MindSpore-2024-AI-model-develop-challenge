#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/07/05 

# 我们在 4 卡机上训练，单卡机上测试推理，所以需要传递这个该死的权重文件
# 如何将开发环境Notebook A的数据复制到Notebook B中？
#   https://support.huaweicloud.com/modelarts_faq/modelarts_05_3172.html
# OBS 控制台
#   https://console.huaweicloud.com/console/?region=cn-south-1#/obs/manage/vhaktyr/object/list?region=cn-southwest-2

from pathlib import Path
from argparse import ArgumentParser
import moxing as mox

BUCKET_NAME = 'vhaktyr'

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--pull')
  parser.add_argument('--push')
  parser.add_argument('--name', help='overwrite save filename')
  args = parser.parse_args()

  assert (args.pull is None) ^ (args.push is None)

  if args.pull:
    url = f'obs://{BUCKET_NAME}/{args.pull}'
    fn = args.name or Path(args.pull).name
    mox.file.copy(url, fn)
  else:
    assert Path(args.push).is_file()
    fn = args.name or Path(args.push).name
    mox.file.copy(args.push, f'obs://{BUCKET_NAME}/{fn}')
