# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27
import os


class FileOperation:
    @staticmethod
    def read_file(fpath):
        """
        读取txt文件，包括换行符
        :param fpath:
        :return:
        """
        try:
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding="utf-8") as f:
                    file = f.read()
                    f.close()
                    print("--------------" + fpath + '——读取成功' + "--------------")
            else:
                print('文件不存在')
        except UnicodeDecodeError:
            with open(fpath, 'r', encoding="gbk") as f:
                file = f.read()
                f.close()
                print("--------------" + fpath + '——读取成功' + "--------------")
        return file

    @staticmethod
    def read_file_by_line(fpath):
        """
        读取txt文件，不包括每行的'\n'换行符
        :param fpath: 文件路径
        :return:
        """
        try:
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding="utf-8") as f:
                    file = f.readlines()
                    f.close()
                    print("--------------" + fpath + '——读取成功' + "--------------")
            else:
                print('文件不存在')
        except UnicodeDecodeError:
            with open(fpath, 'r', encoding="gbk") as f:
                file = f.readlines()
                f.close()
                print("--------------" + fpath + '——读取成功' + "--------------")
        file_line = ""
        for fl in file:
            file_line += fl.strip("\n")
        return file_line

    @staticmethod
    def write_to_file(fpath, contents):
        """
        写入文件
        :param fpath:文件路径+文件名
        :param contents: 文件内容
        :return:
        """
        try:
            if len(contents) != 0:
                with open(fpath, 'w', encoding="utf-8") as f:
                    f.write(contents)
            else:
                print(fpath+'——内容为空')
        except UnicodeEncodeError:
            if len(contents) != 0:
                with open(fpath, 'w', encoding="gbk") as f:
                    f.write(contents)
            else:
                print(fpath + '——内容为空')
        else:
            print(fpath + "——文件保存成功")
