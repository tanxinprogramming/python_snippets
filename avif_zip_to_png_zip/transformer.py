# -*- coding: utf-8 -*-
"""
@editor: PyCharm
@project: avif_zip_to_png_zip
@file: transformer.py
@author: tanxin
@create_time: 2022/10/15 15:50
@version: 1.0
@description: zip文件，且文件名包含avif的文件，转换为png的zip
"""

from log.logger_base import LoggerBase

from PIL import Image
import pillow_avif

import os
import logging
import zipfile


class Transformer(LoggerBase):
    def __init__(self, directory_path: str):
        super().__init__()
        self.directory_path = directory_path
        self.temp_directory_path = os.path.abspath('temp')
        self._add_console_handler()

    def one_avif_to_one_png(self, file_path: str):
        if not file_path.lower().endswith('.avif'):
            return file_path
        new_file_path = self.change_extension(file_path, 'png')
        picture = Image.open(file_path)
        picture.save(new_file_path, 'PNG')
        return new_file_path

    def zip_avif_to_zip_png(self, file_path: str):
        # 解压到temp文件夹

        self.temp_directory_path
        # 转换为png

        # 打包到源文件夹

        # 删除临时文件
        pass

    def transform_directory(self):
        need_to_change_file_paths = []
        for item_name in os.listdir(self.directory_path):
            item_path = os.path.join(self.directory_path, item_name)
            if item_name.lower().endswith('.zip') and 'avif' in item_name.lower() and zipfile.is_zipfile(item_path):
                need_to_change_file_paths.append(item_path)
        self.logger.debug(need_to_change_file_paths)
        for file_path in need_to_change_file_paths:
            self.zip_avif_to_zip_png(file_path)

    def run(self):
        self.transform_directory()

    def change_extension(self, file_path: str, new_extension: str):
        file_name = os.path.basename(file_path)
        file_name = os.path.splitext(file_name)[0]
        file_name = file_name + (new_extension if new_extension.startswith('.') else ('.' + new_extension))
        return os.path.join(os.path.dirname(file_path), file_name)


if __name__ == '__main__':
    directory_path = r'M:\漫画\新建文件夹\[丸山朝ヲ 棚架ユウ るろお] 転生したら剣でした'
    Transformer(directory_path).run()
