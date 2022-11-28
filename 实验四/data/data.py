# -*- coding: utf-8 -*-
# author：xxp time:2022/11/27
import os
import re

import jieba
import zhon.hanzi

from 实验四.data.fileoperations import FileOperation


class Data:
    def __init__(self, t_path, o_path, ex_t_path):
        self.trainingCorpusPath = t_path
        self.originFilePath = o_path
        self.extraTrainingCorpusPath = ex_t_path
        self.originFileName = os.listdir(self.originFilePath)
        self.sentence_structure = '[{characters}{radicals}{non_stops}]*{sentence_end}'.format(
            characters=zhon.hanzi.characters, radicals=zhon.hanzi.radicals, non_stops=zhon.hanzi.non_stops + " ",
            sentence_end=zhon.hanzi._sentence_end)  # 定义中文句子结构
        self.T_SENTENCE = self.format_corpus_by_sentence()  # 字典形式存储训练语料
        self.T = self.jieba_T()
        self.O = self.origin_corpus()

    def expand_training_corpus(self):
        extraTrainingFileName = os.listdir(self.extraTrainingCorpusPath)
        if extraTrainingFileName:
            for file_name in extraTrainingFileName:
                file_content = FileOperation.read_file(self.extraTrainingCorpusPath + file_name)
                format_file = jieba.lcut(file_content)
                temp_file = []
                for word in format_file:
                    temp_file.append(word)
                format_file_content = " ".join(temp_file)
                FileOperation.write_to_file(self.trainingCorpusPath + file_name,format_file_content)
                # try:
                #     with open(self.trainingCorpusPath + file_name, 'w', encoding='utf-8') as f:
                #         f.write(format_file_content)
                # except UnicodeEncodeError:
                #     with open(self.trainingCorpusPath + file_name, 'w', encoding='gbk') as f:
                #         f.write(format_file_content)
                # else:
                #     print("---------------" + self.extraTrainingCorpusPath + file_name + "——写入完成" + "---------------")
        else:
            return

    # 处理语料库（训练语料），将语料库中的文件和文件内容处理存为字典，返回对应三种字典
    def format_corpus_by_sentence(self):
        self.expand_training_corpus()
        trainingName = os.listdir(self.trainingCorpusPath)
        trainingFiles = {}  # 存储训练语料处理后的结果
        for tName in trainingName:
            file_content = []
            tContent = re.findall(self.sentence_structure, FileOperation.read_file(self.trainingCorpusPath + tName))
            for t_content in tContent:
                temp = re.split(" ", t_content)
                while '' in temp:
                    temp.remove('')
                file_content.append(temp)
            trainingFiles[tName] = file_content
        return trainingFiles

    def jieba_T(self):
        self.expand_training_corpus()
        trainingName = os.listdir(self.trainingCorpusPath)
        trainingFiles = {}
        for tName in trainingName:
            trainingFiles[tName] = re.split(" ", FileOperation.read_file_by_line(self.trainingCorpusPath + tName))
        return trainingFiles

    def origin_corpus(self):
        originFiles = {}
        for oName in self.originFileName:
            originFiles[oName] = FileOperation.read_file_by_line(self.originFilePath + oName)
        return originFiles
