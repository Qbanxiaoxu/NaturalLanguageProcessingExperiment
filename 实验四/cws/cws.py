# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27

"""
实现语料库分词
将分词后的语料库写入文件
"""
import os
import jieba
import numpy as np

from 实验四.cws.hmm import Hmm
from 实验四.data.data import Data
from 实验四.config import EX_T_PATH, T_PATH, O_PATH, RESULT_PATH
from 实验四.data.fileoperations import FileOperation


class CWS:
    # data = Data(T_PATH, O_PATH, EX_T_PATH)
    file_name = os.listdir(O_PATH)  # 训练语料文件名
    result_file = {}
    jieba_file = {}

    def __init__(self, data):
        self.data = data
        self.corpus_sentence_list = self.data.origin_file_by_sentence
        self.Hmm = Hmm(data)
        self.cws()

    def viterbi(self, sentence):
        A = self.Hmm.A
        B = self.Hmm.B
        PI = self.Hmm.PI
        state = ['B', 'M', 'E', 'S']
        result_dict = {}
        # 初始化结果字典
        for x in sentence:
            result_dict[x] = {}
            for s in state:
                result_dict[x][s] = 0
        best_node = []  # 记录最佳结点
        T = len(sentence)
        for t in range(0, T):
            w = sentence[t]
            if w == sentence[0]:  # 计算初始概率
                for s in state:
                    if w in (dict(B[s])).keys():
                        result_dict[w][s] = PI[s] * B[s][w]
                dict_temp = dict(result_dict[w])
                a = max(zip(dict_temp.values(), dict_temp.keys()))
                best_node.append(list(a))
            else:
                b_node = best_node[t - 1][1]
                b_pro = best_node[t - 1][0]
                for s in state:
                    if w in (dict(B[s])).keys():
                        result_dict[w][s] = PI[s] * A[state.index(b_node)][state.index(s)] * b_pro
                        # result_dict[w][s] = PI[s] * A[b_node][s] * b_pro  # 最佳结点*转移概率*PI
                dict_temp = dict(result_dict[w])
                a = max(zip(dict_temp.values(), dict_temp.keys()))
                best_node.append(list(a))
        temp = []
        for x in best_node:
            temp.append(x[1])
        sentence_partition = ''
        for i in range(0, T):
            sentence_partition += sentence[i]
            if temp[i] == 'S' or temp[i] == 'E':
                sentence_partition += '|'
        sentence_partition_list = sentence_partition.split("|")[:-1]
        return sentence_partition_list, sentence_partition

    def cws(self):
        for tc_file in self.file_name:
            file_list = []
            jieba_list = []
            file_str = ''
            for sentence in self.corpus_sentence_list[tc_file]:
                result_list, result_str = self.viterbi(sentence)
                jieba_temp = jieba.lcut(sentence)
                file_list.append(result_list)
                jieba_list.append(jieba_temp)
                file_str += result_str
            self.result_file[tc_file] = file_list
            self.jieba_file[tc_file] = jieba_list
            # FileOperation.write_to_file(RESULT_PATH + tc_file, file_str)
