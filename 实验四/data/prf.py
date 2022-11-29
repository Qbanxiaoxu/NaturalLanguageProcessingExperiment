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
        """
        分词结果
        """

    # @staticmethod
    # def to_region(lst):
    #     region = []
    #     start = 0
    #     for word in lst:
    #         end = start + len(word)
    #         region.append((start, end))
    #         start = end
    #     return region
    #
    # def get_correct_number(list_MM, list_jieba):
    #     a = to_region(list_MM)
    #     b = to_region(list_jieba)
    #     res = set(a) & set(b)
    #     return len(res)
    #
    # def get_prf(word_num, word_correct_num, word_standard_num):
    #     p = word_correct_num / word_num
    #     r = word_correct_num / word_standard_num
    #     f = (2 * p * r) / (r + p)
    #     print("word_num:{0}\tword_standard_num:{1}\tword_correct_num:{2}\t\n".format(word_num, word_standard_num,
    #                                                                                  word_correct_num))
    #     print("P:{0:.2%}\tR:{1:.2%}\tF:{2:.2%}\t\n".format(p, r, f))
