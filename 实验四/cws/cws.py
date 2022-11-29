# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27

"""
实现语料库分词
将分词后的语料库写入文件
"""
import os

from 实验四.data.data import Data
from 实验四.config import EX_T_PATH, T_PATH, O_PATH, RESULT_PATH
from 实验四.data.fileoperations import FileOperation


class CWS:
    data = Data(T_PATH, O_PATH, EX_T_PATH)
    file_name = os.listdir(O_PATH)  # 训练语料文件名
    result_file = {}

    def __init__(self):
        self.corpus_sentence_list = self.data.origin_file_by_sentence

    def viterbi(self, sentence):
        """
        输入sentence，是实现分词
        :param sentence:
        :return:HMM分词结果，分词列表和字符串形式，例如：我|爱|我|的|祖国|
        """

        return [], ''

    def cws(self):
        for tc_file in self.file_name:
            file_list = []
            file_str = ''
            for list_file in self.corpus_sentence_list[tc_file]:
                for sentence in list_file:
                    result_list, result_str = self.viterbi(sentence)
                    file_list.append(result_list)
                    file_str += result_str
            self.result_file[tc_file] = file_list
            FileOperation.write_to_file(RESULT_PATH + tc_file, file_str)
