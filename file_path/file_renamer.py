# -*- coding: utf-8 -*-
"""
@editor: PyCharm
@project: python_snippet
@file: file_renamer.py
@author: tanxin
@create_time: 2022/10/15 19:56
@version: 1.0
@description:
"""
import os


class FileRenamer:
    def __init__(self, file_path: str):
        file_name = os.path.basename(file_path)
        self.file_name_without_extension, self.extension = os.path.splitext(file_name)
        self.path = os.path.dirname(file_path)

    def change_extension(self, new_extension: str) -> str:
        if not new_extension.startswith('.'):
            new_extension = '.' + new_extension
        return os.path.join(self.path, self.file_name_without_extension + new_extension)

    def add_prefix(self, prefix: str) -> str:
        return os.path.join(self.path, prefix + self.file_name_without_extension + self.extension)

    def add_suffix(self, prefix: str) -> str:
        return os.path.join(self.path, prefix + self.file_name_without_extension + self.extension)

    def add_prefix_and_suffix(self, prefix: str, suffix: str) -> str:
        return os.path.join(self.path, prefix + self.file_name_without_extension + suffix + self.extension)

    def change_directory_path(self, directory_path: str):
        return os.path.join(directory_path, self.file_name_without_extension + self.extension)

    def change_directory_path_and_add_prefix_and_suffix(self, directory_path: str, prefix: str, suffix: str):
        return os.path.join(directory_path, prefix + self.file_name_without_extension + suffix + self.extension)