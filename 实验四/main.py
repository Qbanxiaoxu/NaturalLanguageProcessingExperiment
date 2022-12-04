# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27
import os

from 实验四.cws.cws import CWS
from 实验四.data.data import Data
from 实验四.config import EX_T_PATH, T_PATH, O_PATH
from 实验四.data.prf import CalculatePRF

if __name__ == '__main__':
    data = Data(T_PATH, O_PATH, EX_T_PATH)
    cws = CWS(data)
    prf = CalculatePRF()
