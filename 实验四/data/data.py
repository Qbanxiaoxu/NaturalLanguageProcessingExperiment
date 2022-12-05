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
        self.T, self.T_FILE_STR = self.format_corpus()
        self.OC, self.origin_file_by_sentence = self.origin_corpus()

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
                FileOperation.write_to_file(self.trainingCorpusPath + file_name, format_file_content)
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

    def format_corpus(self):
        """
        以列表形式或字符串形式返回训练语料字符
        :return:
        """
        self.expand_training_corpus()
        trainingName = os.listdir(self.trainingCorpusPath)
        trainingFiles = {}
        training_file_str = {}
        for tName in trainingName:
            temp = re.split(" ", FileOperation.read_file_by_line(self.trainingCorpusPath + tName))
            # for word in temp:
            #     if word in zhon.hanzi.punctuation:
            #         temp.remove(word)
            while '' in temp:
                temp.remove('')
            trainingFiles[tName] = temp
            training_file_str[tName] = ''.join(trainingFiles[tName])
        return trainingFiles, training_file_str

    def origin_corpus(self):
        """
        语料库中的内容不含换行符
        :return:
        """
        originFiles = {}
        originFiles_by_sentence = {}
        for oName in self.originFileName:
            originFiles[oName] = FileOperation.read_file_by_line(self.originFilePath + oName)
            temp = re.findall(zhon.hanzi.sentence, originFiles[oName])
            # file = []
            # for sentence in temp:
            #     file.append(re.split(r',|，', sentence[:-1]))
            originFiles_by_sentence[oName] = temp
        return originFiles, originFiles_by_sentence
