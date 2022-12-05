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
        self.get_prf()
        """
        分词结果
        """

    @staticmethod
    def to_region(lst):
        region = []
        start = 0
        for word in lst:
            end = start + len(word)
            region.append((start, end))
            start = end
        return region

    def get_correct_number(self, list_MM, list_jieba):
        a = self.to_region(list_MM)
        b = self.to_region(list_jieba)
        res = set(a) & set(b)
        return len(res)

    def get_prf(self):
        word_num = 0
        word_correct_num = 0
        word_standard_num = 0
        # sentence_num0 = 0
        # sentence_num1 = 0
        for file in self.RESULT.keys():
            for sentence in self.RESULT[file]:
                word_num += len(sentence)
                # sentence_num0 += 1
            for sentence1 in self.JIEBALIST[file]:
                word_standard_num += len(sentence1)
                #     sentence_num1 += 1
            for i in range(len(self.RESULT[file])):
                # print("sentence_1:{0} \n sentence_2:{1}".format(self.RESULT[file][i], self.JIEBALIST[file][i]))
                word_correct_num += self.get_correct_number(self.RESULT[file][i], self.JIEBALIST[file][i])

        # print("sentence_num0:{0}  sentence_num1:{1}".format(sentence_num0,sentence_num1))
        p = word_correct_num / word_num
        r = word_correct_num / word_standard_num
        f = (2 * p * r) / (r + p)
        print("word_num:{0}\tword_standard_num:{1}\tword_correct_num:{2}\t\n".format(word_num, word_standard_num,
                                                                                     word_correct_num))
        print("P:{0:.2%}\tR:{1:.2%}\tF:{2:.2%}\t\n".format(p, r, f))
