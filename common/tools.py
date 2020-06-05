# -*- coding: utf-8 -*-

import csv
import os


class Tools:

    def __init__(self):
        self.csv_dirname = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'csv' + os.sep

    def get_csv_info(self, filepath):
        info = []
        file_abs_path = self.csv_dirname + filepath
        if os.path.exists(file_abs_path):
            with open(self.csv_dirname + filepath, 'r') as f:
                reader = csv.reader(f)
                # 逐行读取csv文件
                for i in reader:
                    info.append(i)
            if info:
                return info
            else:
                raise Exception("文件数据为空")
        else:
            raise FileNotFoundError



if __name__ == "__main__":

    t = Tools()
    s = t.get_csv_info('my.csv')
    print(s)
