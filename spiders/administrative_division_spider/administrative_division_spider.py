# -*- coding:utf-8 -*-
# author: tan xin

from log.logger_base import LoggerBase

import requests
import pandas
import lxml.html

import json5
import os
import logging


class AdministrativeDivisionSpider(LoggerBase):
    def __init__(self, save_directory_path: str = None):
        super().__init__(default_level=logging.DEBUG)
        self._add_console_handler()
        if save_directory_path is None:
            save_directory_path = os.path.dirname(__file__)
        self.save_directory_path = save_directory_path
        with open('settings.json5', 'r', encoding='utf-8') as f:
            settings = json5.load(f)
        self.url = settings['url']
        self.output_types = settings['outputTypes']
        self.logger.debug(f'url: {self.url}')
        self.logger.debug(f'url: {self.output_types}')
        self.headers = {
            "Host": "www.mca.gov.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }
        self.result = []

    def parse(self, response: requests.Response):
        self.logger.debug('parse')
        html = lxml.html.etree.HTML(response.text)
        tr = html.xpath(r"//tr[@height=19]")
        result = list()
        province = ''
        city = ''
        for i in range(len(tr)):
            self.logger.debug(i)
            number = ''.join(tr[i].xpath(r"./td[2]//text()")).strip()
            area_name = ''.join(tr[i].xpath(r"./td[3]//text()")).strip()
            # 分类
            if number[-4:] == '0000':
                level = '省级'
            elif number[-2:] == '00':
                level = '市级'
            else:
                level = '市级或县级'

            # 确定的等级
            if level == '省级':
                province = number
                city = ''
                up = ''
            elif level == '市级':
                city = number
                up = province
            else:
                if city == '':
                    up = province
                    level = '市级'
                else:
                    up = city
                    level = '县级'
            result.append((number, level, area_name, up))
        self.result = result

    def export_mssql(self):
        if 'mssql' in self.output_types:
            file_path = os.path.join(self.save_directory_path, 'AdministrativeDivisionSpider.sql')
            self.logger.info(f'导出mssql: {file_path}')
            # 求最长的名字
            longest = 0
            for i in range(len(self.result)):
                if longest < len(self.result[i][2]):
                    longest = len(self.result[i][2])

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f'''drop table if exists administrative_division
                
create table administrative_division
(
    number char(6) not null primary key,
    level nchar(2) not null,
    name nchar({longest}) not null,
    up char(6) null
)
go\n''')
                row = 0
                for item in self.result:
                    if row == 0:
                        f.write('''insert into administrative_division(number, level, name, up)
        values\n''')
                    row = row + 1
                    if row > 1:
                        f.write('\n, ')
                    f.write(item.__str__())
                    if row >= 900:
                        row = 0
                        f.write('\n')

    def export_xlsx(self):
        if 'excel' in self.output_types:
            file_path = os.path.join(self.save_directory_path, 'AdministrativeDivisionSpider.xlsx')
            self.logger.info(f'导出excel: {file_path}')
            df = pandas.DataFrame(self.result)
            df.columns = ['行政区编号', '行政区等级', '行政区名', '上级行政区编号']
            df.to_excel(file_path)

    def run(self):
        self.logger.debug('run')
        response = requests.get(self.url, headers=self.headers, proxies=None)
        self.parse(response)
        self.export_mssql()
        self.export_xlsx()


if __name__ == '__main__':
    AdministrativeDivisionSpider().run()
