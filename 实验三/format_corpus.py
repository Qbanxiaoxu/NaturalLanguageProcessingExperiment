import os
import re

import jieba
import zhon.hanzi

trainingCorpusPath = "E://Python/自然语言处理/实验三/训练语料/"
fmmFilePath = "E://Python/自然语言处理/实验三/语料库_FMM/"
bmmFilePath = "E://Python/自然语言处理/实验三/语料库_BMM/"
originFilePath = "E://Python/自然语言处理/实验三/语料库/"
extraTrainingCorpusPath = "E://Python/自然语言处理/实验三/训练语料扩充/"
fmmFileName = os.listdir(fmmFilePath)
bmmFileName = os.listdir(bmmFilePath)
originFileName = os.listdir(originFilePath)
extraTrainingFileName = os.listdir(extraTrainingCorpusPath)
sentence_structure = '[{characters}{radicals}{non_stops}]*{sentence_end}'.format(
    characters=zhon.hanzi.characters, radicals=zhon.hanzi.radicals, non_stops=zhon.hanzi.non_stops + " " + "|",
    sentence_end=zhon.hanzi._sentence_end)  # 定义中文句子结构


def read_file(fpath):  # 读取文件，返回字符串
    try:
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding="utf-8") as f:
                file = f.read()
                f.close()
                print("--------------" + fpath + '——读取成功' + "--------------")
        else:
            print('文件不存在')
    except UnicodeDecodeError:
        with open(fpath, 'r', encoding="gbk") as f:
            file = f.read()
            f.close()
            print("--------------" + fpath + '——读取成功' + "--------------")
    return file


def modify_t(sentence):  # 在训练语料句子的前后加上<EOS>和<BOS>，返回切分为词的句子列表
    s_modify1 = ""
    for stop in zhon.hanzi.stops:
        s_modify1 = sentence.replace(stop, "<EOS>")
    s_modify1 = s_modify1.strip()
    s_modify2 = "<BOS> " + s_modify1
    return re.split(" ", s_modify2)


def modify_fb(sentence):  # 处理分词语料中的句子，切分为词，返回存储句子的列表
    for stop in zhon.hanzi.stops:
        sentence = sentence.replace(stop, "")
    s_modify = re.split("\|", sentence)
    while "" in s_modify:
        s_modify.remove("")
    return s_modify


# 处理语料库（训练语料和分词语料），将语料库中的文件和文件内容处理存为字典，返回对应三种字典
def format_corpus():
    # expand_training_corpus()
    trainingName = os.listdir(trainingCorpusPath)
    trainingFiles = {}  # 存储训练语料处理后的结果
    fmmFiles = {}  # 存储fmm分词处理后的结果
    bmmFiles = {}  # 存储bmm分词处理后的结果
    for fName in fmmFileName:
        fmmFilesContent = []
        fContent = re.findall(sentence_structure, read_file(fmmFilePath + fName))  # 将.txt文件中句子提取出来，存为列表
        for f_content in fContent:
            fmmFilesContent.append(modify_fb(f_content))  # 处理列表中的句子
        fmmFiles[fName] = fmmFilesContent
    for bName in bmmFileName:
        bmmFilesContent = []
        bContent = re.findall(sentence_structure, read_file(bmmFilePath + bName))
        for b_content in bContent:
            bmmFilesContent.append(modify_fb(b_content))
        bmmFiles[bName] = bmmFilesContent
    for tName in trainingName:
        eosBos = []
        tContent = re.findall(sentence_structure, read_file(trainingCorpusPath + tName))
        for t_content in tContent:
            eosBos.append(modify_t(t_content))
        trainingFiles[tName] = eosBos
    return trainingFiles, fmmFiles, bmmFiles


T, F, B = format_corpus()  # 字典形式存储分词语料和训练语料


def single_frequency():
    single_frequency_dict = {}
    for tContent in T.values():
        if tContent:
            for sentence in tContent:
                if sentence:
                    for word in sentence:
                        if word not in single_frequency_dict.keys():
                            single_frequency_dict[word] = 1
                        else:
                            single_frequency_dict[word] += 1
    return single_frequency_dict


def double_frequency():
    double_frequency_dict = {}
    for tContent in T.values():
        if tContent:
            for sentence in tContent:
                if sentence:
                    for i, word in enumerate(sentence):
                        if i == 0:
                            double_word = "<BOS>" + word
                        else:
                            double_word = sentence[i - 1] + word
                        if double_word not in double_frequency_dict.keys():
                            double_frequency_dict[double_word] = 1
                        else:
                            double_frequency_dict[double_word] += 1
    return double_frequency_dict


def expand_training_corpus():
    if extraTrainingFileName:
        for file_name in extraTrainingFileName:
            file_content = read_file(extraTrainingCorpusPath + file_name)
            format_file = jieba.lcut(file_content)
            format_file_content = ""
            temp_file = []
            for word in format_file:
                temp_file.append(word)
                temp_file.append(" ")
            format_file_content.join(temp_file)
            try:
                with open(extraTrainingCorpusPath + file_name, 'w', encoding='utf-8') as f:
                    f.write(format_file_content)
            except UnicodeEncodeError:
                with open(extraTrainingCorpusPath + file_name, 'w', encoding='gbk') as f:
                    f.write(format_file_content)
            else:
                print("---------------" + extraTrainingCorpusPath + file_name + "——写入完成" + "---------------")
    else:
        return
