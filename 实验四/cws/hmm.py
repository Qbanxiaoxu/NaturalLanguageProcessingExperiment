# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27
import os

from 实验四.config import T_PATH, O_PATH, EX_T_PATH
from 实验四.data.data import Data


class Hmm:
    data = Data(T_PATH, O_PATH, EX_T_PATH)
    tc_file_name = os.listdir(data.trainingCorpusPath)  # 训练语料文件名

    def __init__(self):
        """
        训练语料
        """
        self.TAG = ['B', 'M', 'E', 'S']  # B：分词词首；M：分词词中；E：分词词尾；S：单个词分词
        """
        TAG
        隐含状态 S
        """
        self.observations = self._observation_set()
        """
        观察序列 O
        包含所有训练语料中的字的集合
        """
        self.A = {}
        """
        State transition probability matrix A
        {'B':{'B':xx,'M':xx.'E':xx,'S':xx}}
        """
        self.B = self._B_matrix()
        """
        Observation probability matrix
        用双层字典实现矩阵
        """
        self.PI = {}
        """
        初始状态概率向量
        字典存储
        """
        self.TC_TAG = self._tc_tag()

    def _observation_set(self):
        """
        Finding observation sequence
        :return:
        """

        observations = set()
        # ii=[]
        for tc_file in self.tc_file_name:
            for content in self.data.T[tc_file]:
                for character in content:
                    observations.add(character)
                    # ii.append(character)
        # print(len(ii))
        return observations

    def _B_matrix(self):
        """
        观测概率矩阵
        输出概率矩阵
        :return:字典
        """
        B = {}
        for tc_file in self.tc_file_name:
            b = {}
            for character_tag in self._tc_tag()[tc_file]:
                if character_tag[1] + character_tag[0] not in b.keys():
                    b[character_tag[1] + character_tag[0]] = 1
                else:
                    b[character_tag[1] + character_tag[0]] += 1
            B[tc_file] = b
        l=0
        l1 = 0
        l2=0
        for cc in self.tc_file_name:
            l += len(B[cc])
            l2+=len(self._tc_tag()[cc])
        l1 = len(self._observation_set())
        print(l / l1)
        return B

    def _tc_tag(self):
        """
        将训练语料中的字添加标记
        用元组存储(字，TAG)
        :return:
        """
        # B：分词词首；M：分词词中；E：分词词尾；S：单个词分词
        mark_tc = {}
        for tc_file in self.tc_file_name:
            mark_tc_list = []
            for content in self.data.T[tc_file]:
                if len(content) == 1:
                    tup_content = (content, 'S')
                    mark_tc_list.append(tup_content)
                if len(content) == 2:
                    tup_content1 = (content[0], 'B')
                    tup_content2 = (content[1], 'E')
                    mark_tc_list.append(tup_content1)
                    mark_tc_list.append(tup_content2)
                if len(content) >= 3:
                    tup_content1 = (content[0], 'B')
                    tup_content2 = (content[-1], 'E')
                    mark_tc_list.append(tup_content1)
                    mark_tc_list.append(tup_content2)
                    for character in content[1:-1]:
                        tup_content = (character, 'M')
                        mark_tc_list.append(tup_content)
            mark_tc[tc_file] = mark_tc_list
        return mark_tc
