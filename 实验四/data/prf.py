# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27

"""
根据已经处理好的分词结果
计算prf值
参考标准为jieba分词结果
"""
from 实验四.cws.cws import CWS


class CalculatePRF:
    def __init__(self):
        self.RESULT = CWS.result_file
        self.JIEBALIST = CWS.jieba_file
        """
        分词结果
        """

    @staticmethod
    def get_sum(dic):
        len_list = 0
        for i in dic:
            # print("i",i)
            # print("c[i]",dic[i])
            for j in dic[i]:
                # print("j",j)
                len_list += len(j)
        return len_list

    @staticmethod
    def to_region(lst):
        region = []
        start = 0
        # print("lst",lst)
        for sentence in lst:
            for word in sentence:
                # print("word",word)
                end = start + len(word)
                region.append((start, end))
                start = end
                # print("start , end",start , end)
        # print("region",region)
        return region

    def get_correct_number(self, list_MM, list_jieba):
        # print("list_MM",list_MM)
        # print("list_jieba",list_jieba)
        a = self.to_region(list_MM)
        b = self.to_region(list_jieba)
        # print("a,b",a,b)
        res = set(a) & set(b)
        # print("res",res)
        return len(res)

    def get_correct_sum(self, dic1, dic2):
        num = 0
        for i in dic1:
            num += self.get_correct_number(dic1[i], dic2[i])
            # print("dic1[i]",dic1[i])
            # print("dic2[i]",dic2[i])
            # print("get_correct_number(dic1[i],dic2[i])",get_correct_number(dic1[i],dic2[i]))
        return num

    def get_prf(self):
        word_num = self.get_sum(self.RESULT)
        word_correct_num = self.get_correct_sum(self.RESULT, self.JIEBALIST)
        word_standard_num = self.get_sum(self.JIEBALIST)
        p = word_correct_num / word_num
        r = word_correct_num / word_standard_num
        f = (2 * p * r) / (r + p)
        print("word_num:{0}\tword_standard_num:{1}\tword_correct_num:{2}\t\n".format(word_num, word_standard_num,
                                                                                     word_correct_num))
        print("P:{0:.2%}\tR:{1:.2%}\tF:{2:.2%}\t\n".format(p, r, f))
