# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27
import os

from 实验四.cws.cws import CWS
from 实验四.cws.hmm import Hmm
from 实验四.data.data import Data
from 实验四.config import EX_T_PATH, T_PATH, O_PATH, RESULT_PATH

if __name__ == '__main__':
    # content="3asijee12"
    # print(content[0])
    # for character in content[1:-1]:
    #     print(character)
    # print(len(Hmm().observations))
    data = Data(T_PATH, O_PATH, EX_T_PATH)
    # print(data.T["1998人民日报（分词）.txt"])
    # print(data.O["新建文本文档.txt"])
    h = CWS(data).cws()

    # print(h)
    # dic_content = {'content': 'B'}
    # print(dic_content)
    # dic_content = {'content0': 'A'}
    # print(dic_content)
    # dic_content = {'content1': 'A'}
    # print(dic_content)
