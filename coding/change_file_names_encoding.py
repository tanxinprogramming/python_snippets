# -*- coding: utf-8 -*-
"""
@editor: PyCharm
@project: 日文乱码文件名改为gbk
@file: transformer.py
@author: tanxin
@create_time: 2022/1/12 19:13
@version: 1.0
@description:
"""
import os


class FileNameCodingChanger:
    def __init__(self, directory: str, coding_dict: dict):
        self.directory = directory
        self.coding_from = coding_dict['from']
        self.coding_to = coding_dict['to']

    def run(self):
        walker = os.walk(self.directory, False)
        for level in walker:
            # print(level)
            for d in level[1]:
                self.rename(d, level)
            for f in level[2]:
                self.rename(f, level)

    def rename(self, f, level):
        new_name = f.encode(self.coding_to).decode(self.coding_from)
        old_path = os.path.join(level[0], f)
        new_path = os.path.join(level[0], new_name)
        print(old_path, new_path)
        os.rename(old_path, new_path)


if __name__ == '__main__':
    _coding_dict1 = {
        'from': 'shift-jis',  # 文件名本来的编码
        'to': 'gbk',  # 系统编码
    }
    _coding_dict2 = {
        'from': 'gbk',
        'to': 'shift-jis',
    }
    _directory = r'D:\game\galgame\workspace\install\Bloodroot 101201'
    FileNameCodingChanger(_directory, _coding_dict1).run()
