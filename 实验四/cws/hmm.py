# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27
import os

import zhon.hanzi

from 实验四.config import T_PATH, O_PATH, EX_T_PATH
from 实验四.data.data import Data


class Hmm:
    # data = Data(T_PATH, O_PATH, EX_T_PATH)
    # tc_file_name = os.listdir(data.trainingCorpusPath)  # 训练语料文件名

    def __init__(self, data):
        self.data = data
        self.tc_file_name = os.listdir(data.trainingCorpusPath)  # 训练语料文件名
        """
        训练语料
        """
        self.STATE = ['B', 'M', 'E', 'S']  # B：分词词首；M：分词词中；E：分词词尾；S：单个词分词
        """
        TAG
        隐含状态 S
        """
        self.observations = self._observation_set()
        """
        观察序列 O
        包含所有训练语料中的字的集合
        """
        self.A = self._A_matrix_by_tuple()
        # self.A=self._A_matrix_by_dict()
        """
        State transition probability matrix A
        {'B':{'B':xx,'M':xx.'E':xx,'S':xx}}
        """
        self.B = self._B()
        """
        Observation probability matrix
        用双层字典实现矩阵
        """
        self.PI = self._PI_matrix()
        """
        初始状态概率向量
        字典存储
        """
        # self.STATE_NUM = self._count_state()
        # self.character_num = self._count_character()  # 所有训练语料中字数
        # self.TC_TAG = self._tc_tag_dict()

    def _count_state(self):
        """
        计算各种状态的频次
        :return:
        """
        state_num = {}
        for s in self.STATE:
            state_num[s] = 0
        B = self._B_matrix()
        for state in self.STATE:
            for num_key in B[state].keys():
                state_num[state] += B[state][num_key]
        return state_num

    def _count_character(self):
        """
        训练语料中所有字的数量
        :return:
        """
        TC_TAG = self._tc_tag_tuple()
        count = 0
        for tc_file in self.tc_file_name:
            count += len(TC_TAG[tc_file])
        return count

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

    def _A_matrix_by_tuple(self):
        """
        转移概率矩阵
        :return:
        """
        TC_TAG = self._tc_tag_tuple()
        a = {}
        for tc_file in self.tc_file_name:
            for i, character_tag in enumerate(TC_TAG[tc_file]):
                if i == len(TC_TAG[tc_file]) - 1:
                    break
                if character_tag[1] + TC_TAG[tc_file][i + 1][1] not in a.keys():
                    a[character_tag[1] + TC_TAG[tc_file][i + 1][1]] = 1
                else:
                    a[character_tag[1] + TC_TAG[tc_file][i + 1][1]] += 1
        A0 = []
        for r in self.STATE:
            row = []
            for c in self.STATE:
                if r + c not in a.keys():
                    row.append(0)
                else:
                    row.append(a[r + c])
            A0.append(row)
        A = []
        rows_sum = []
        for row in A0:
            row_sum = 0
            for value in row:
                row_sum += value
            rows_sum.append(row_sum)
        for r in range(len(self.STATE)):
            row_p = []
            for c in range(len(self.STATE)):
                row_p.append(A0[r][c] / rows_sum[r])
            A.append(row_p)

        return A

    def _A_matrix_by_dict(self):
        """
        未算概率
        :return:
        """
        A = {}
        TC_TAG = self._tc_tag_dict()
        for tc_file in self.tc_file_name:
            for i, character in enumerate(self.data.T_FILE_STR[tc_file]):
                if i == len(self.data.T_FILE_STR[tc_file]) - 1:
                    break
                if TC_TAG[tc_file][i][character] + TC_TAG[tc_file][i + 1][
                    self.data.T_FILE_STR[tc_file][i + 1]] not in A.keys():
                    A[TC_TAG[tc_file][i][character] + TC_TAG[tc_file][i + 1][self.data.T_FILE_STR[tc_file][i + 1]]] = 1
                else:
                    A[TC_TAG[tc_file][i][character] + TC_TAG[tc_file][i + 1][self.data.T_FILE_STR[tc_file][i + 1]]] += 1

        return A

    def _B_matrix(self):
        """
        观测频次矩阵
        输出频次矩阵
        :return:字典
        """
        TC_TAG = self._tc_tag_tuple()
        b_B = {}
        b_M = {}
        b_E = {}
        b_S = {}

        for tc_file in self.tc_file_name:
            for character_tag in TC_TAG[tc_file]:
                if character_tag[1] == 'B':
                    if character_tag[0] not in b_B.keys():
                        b_B[character_tag[0]] = 1
                    else:
                        b_B[character_tag[0]] += 1
                if character_tag[1] == 'M':
                    if character_tag[0] not in b_M.keys():
                        b_M[character_tag[0]] = 1
                    else:
                        b_M[character_tag[0]] += 1
                if character_tag[1] == 'E':
                    if character_tag[0] not in b_E.keys():
                        b_E[character_tag[0]] = 1
                    else:
                        b_E[character_tag[0]] += 1
                if character_tag[1] == 'S':
                    if character_tag[0] not in b_S.keys():
                        b_S[character_tag[0]] = 1
                    else:
                        b_S[character_tag[0]] += 1
        B = {'B': b_B, 'M': b_M, 'E': b_E, 'S': b_S}
        return B

    def _B(self):
        """
        输出概率矩阵
        :return:
        """
        state_num = self._count_state()
        B0 = self._B_matrix()
        B = {}
        for state in self.STATE:
            b = {}
            for character in B0[state].keys():
                b[character] = B0[state][character] / state_num[state]
            B[state] = b
        return B

    def _PI_matrix(self):
        """
        初始概率矩阵
        :return:
        """
        pi = {}
        # pi = []
        # s=0
        state_num = self._count_state()
        state_sum = self._count_character()
        for state in self.STATE:
            # s+=state_num[state]
            pi[state] = state_num[state] / state_sum
            # pi.append(state_num[state] / state_sum)
        return pi

    def _tc_tag_tuple(self):
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
                if content in zhon.hanzi.punctuation:
                    continue
                if len(content) == 1:
                    tup_content = (content, 'S')
                    # dic_content= {content: 'S'}
                    mark_tc_list.append(tup_content)
                if len(content) == 2:
                    if content[0] not in zhon.hanzi.punctuation:
                        tup_content1 = (content[0], 'B')
                        mark_tc_list.append(tup_content1)
                        tup_content2 = (content[1], 'E')
                        mark_tc_list.append(tup_content2)
                    else:
                        tup_content1 = (content[0], 'S')
                        mark_tc_list.append(tup_content1)
                        tup_content2 = (content[1], 'S')
                        mark_tc_list.append(tup_content2)
                if len(content) == 3:
                    if content[0] not in zhon.hanzi.punctuation:
                        tup_content1 = (content[0], 'B')
                        mark_tc_list.append(tup_content1)
                        tup_content = (content[1], 'M')
                        mark_tc_list.append(tup_content)
                        tup_content2 = (content[-1], 'E')
                        mark_tc_list.append(tup_content2)
                    else:
                        tup_content1 = (content[0], 'S')
                        mark_tc_list.append(tup_content1)
                        tup_content1 = (content[1], 'B')
                        mark_tc_list.append(tup_content1)
                        tup_content2 = (content[-1], 'E')
                        mark_tc_list.append(tup_content2)
                if len(content) >= 4:
                    if content[0] not in zhon.hanzi.punctuation:
                        tup_content1 = (content[0], 'B')
                        mark_tc_list.append(tup_content1)
                        for character in content[1:-1]:
                            tup_content = (character, 'M')
                            mark_tc_list.append(tup_content)
                        tup_content2 = (content[-1], 'E')
                        mark_tc_list.append(tup_content2)
                    else:
                        tup_content1 = (content[0], 'S')
                        mark_tc_list.append(tup_content1)
                        tup_content1 = (content[1], 'B')
                        mark_tc_list.append(tup_content1)
                        for character in content[2:-1]:
                            tup_content = (character, 'M')
                            mark_tc_list.append(tup_content)
                        tup_content2 = (content[-1], 'E')
                        mark_tc_list.append(tup_content2)

            mark_tc[tc_file] = mark_tc_list
        return mark_tc

    def _tc_tag_dict(self):
        """
        将训练语料中的字添加标记
        用字典存储[字：TAG]
        :return:
        """
        # B：分词词首；M：分词词中；E：分词词尾；S：单个词分词
        mark_tc = {}
        for tc_file in self.tc_file_name:
            mark_tc_list = []
            for content in self.data.T[tc_file]:
                if content in zhon.hanzi.punctuation:
                    continue
                if len(content) == 1:
                    dic_content = {content: 'S'}
                    mark_tc_list.append(dic_content)
                if len(content) == 2:
                    # tup_content1 = (content[0], 'B')
                    if content[0] not in zhon.hanzi.punctuation:
                        dic_content = {content[0]: 'B'}
                        mark_tc_list.append(dic_content)
                        # tup_content2 = (content[1], 'E')
                        dic_content = {content[1]: 'E'}
                        mark_tc_list.append(dic_content)
                    else:
                        dic_content = {content[0]: 'S'}
                        mark_tc_list.append(dic_content)
                        # tup_content2 = (content[1], 'E')
                        dic_content = {content[1]: 'S'}
                        mark_tc_list.append(dic_content)
                if len(content) >= 3:
                    # tup_content1 = (content[0], 'B')
                    if content[0] not in zhon.hanzi.punctuation:
                        dic_content = {content[0]: 'B'}
                        mark_tc_list.append(dic_content)
                        for character in content[1:-1]:
                            dic_content = {character: 'M'}
                            mark_tc_list.append(dic_content)
                        dic_content = {content[-1]: 'E'}
                        mark_tc_list.append(dic_content)
                    else:
                        dic_content = {content[0]: 'S'}
                        mark_tc_list.append(dic_content)
                        dic_content = {content[1]: 'B'}
                        mark_tc_list.append(dic_content)
                        for character in content[2:-1]:
                            dic_content = {character: 'M'}
                            mark_tc_list.append(dic_content)
                        dic_content = {content[-1]: 'E'}
                        mark_tc_list.append(dic_content)

            mark_tc[tc_file] = mark_tc_list
        return mark_tc
