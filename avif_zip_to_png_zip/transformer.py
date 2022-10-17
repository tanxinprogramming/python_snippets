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
import shutil
import zipfile


class Transformer(LoggerBase):
    def __init__(self, directory_path: str):
        super().__init__()
        self.directory_path = directory_path
        self.temp_directory_path = os.path.abspath('temp')
        self._add_console_handler()

    def one_avif_to_one_png(self, file_path: str):
        self.logger.debug(f'transform {file_path}')
        if not file_path.lower().endswith('.avif'):
            return file_path
        new_file_path = self.change_extension(file_path, 'png')
        picture = pillow_avif.AvifImagePlugin.Image.open(file_path)
        picture.save(new_file_path, 'PNG')
        return new_file_path

    def zip_avif_to_zip_png(self, file_path: str):
        self.logger.info(f'正在解压 {file_path}')
        # 解压到temp文件夹
        zip = zipfile.ZipFile(file_path)
        zip.extractall(self.temp_directory_path)
        zip.close()
        # 转换为png
        self.logger.info(f'开始转换 {file_path}')
        file_paths = []
        for root_base, _, file_names in os.walk(self.temp_directory_path):
            for file_name in file_names:
                old_file_path = self.one_avif_to_one_png(os.path.join(root_base, file_name))
                new_file_path = os.path.join(self.temp_directory_path, os.path.basename(old_file_path))
                shutil.move(old_file_path, new_file_path)
                file_paths.append(new_file_path)
        # 打包到源文件夹
        new_file_name = os.path.basename(file_path).replace('AVIF', 'PNG')
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        self.logger.info(f'开始打包 {new_file_path}')
        zip = zipfile.ZipFile(new_file_path, 'w', zipfile.ZIP_STORED)
        for file_path in file_paths:
            zip.write(file_path, os.path.basename(file_path))
        zip.close()
        # 删除临时文件
        self.logger.info('删除临时文件')
        self.clear_temp_directory(self.temp_directory_path)

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

    def clear_temp_directory(self, directory_path: str):
        for item_name in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item_name)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                self.clear_temp_directory(item_path)
                os.rmdir(item_path)


if __name__ == '__main__':
    directory_path = r'M:\漫画\新建文件夹\[丸山朝ヲ 棚架ユウ るろお] 転生したら剣でした'
    Transformer(directory_path).run()
