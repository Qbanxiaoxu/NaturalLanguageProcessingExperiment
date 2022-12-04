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
        # self.cws()

    @staticmethod
    def transition(A):
        T = []
        for x in A.keys():
            lista = []
            for y in A[x].keys():
                lista.append(A[x][y])
            T.append(lista)
        return np.array(T)

    def viterbi(self, sentence):
        """
        输入sentence，是实现分词
        :param sentence:
        :return:HMM分词结果，分词列表和字符串形式，例如：我|爱|我|的|祖国|
        """

        # A = self.transition(self.Hmm.A)  # A状态转移概率矩阵
        A = np.array(self.Hmm.A)
        B = self.Hmm.B
        # PI = np.array(self.Hmm.PI.values())
        PI = np.array(self.Hmm.PI)
        state = self.Hmm.STATE
        result = []  # 对句子分词后的结果
        # psi最佳前驱结点，delta最大路径
        delta = [[0 for _ in range(4)] for _ in range(len(sentence))]
        psi = [[0 for _ in range(4)] for _ in range(len(sentence))]
        for t in range(len(sentence)):
            if t == 0:
                psi[t][:] = [0, 0, 0, 0]
                for i in range(0, 4):
                    delta[t][i] = PI[i] * B[state[i]][sentence[t]]

            else:
                for i in range(4):
                    temp = [delta[t - 1][j] * A[j][i] for j in range(A)]

                    delta[t][i] = max(temp) * B[state[i]][sentence[t]]

                    psi[t][i] = temp.index(max(temp))
        status = []  # 保存最优状态链
        it = delta[-1].index(max(delta[-1]))
        status.append(it)

        for t in range(len(delta) - 2, -1, -1):
            it = psi[t + 1][status[0]]
            status.insert(0, it)

        sentence_partition = ''
        for t in range(len(sentence)):
            sentence_partition += sentence[t]
            if (status[t] == '2' or status[t] == '3') and t != len(sentence) - 1:
                sentence_partition += '|'

        result = sentence_partition.split('|')
        return result, sentence_partition

    def cws(self):
        for tc_file in self.file_name:
            file_list = []
            jieba_list = []
            file_str = ''
            for list_file in self.corpus_sentence_list[tc_file]:
                for sentence in list_file:
                    result_list, result_str = self.viterbi(sentence)
                    jieba_list = jieba.lcut(sentence)
                    file_list.append(result_list)
                    jieba_list.append(jieba_list)
                    file_str += result_str
            self.result_file[tc_file] = file_list
            self.jieba_file[tc_file] = jieba_list
            # FileOperation.write_to_file(RESULT_PATH + tc_file, file_str)
