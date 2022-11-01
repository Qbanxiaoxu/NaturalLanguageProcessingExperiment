import os
import re

import zhon.hanzi


def read_file(fpath):
    try:
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding="utf-8") as f:
                file = f.read()
                f.close()
        else:
            print('文件不存在')
    except UnicodeDecodeError:
        with open(fpath, 'r', encoding="gbk") as f:
            file = f.read()
            f.close()
            print('读取成功')
    else:
        print('读取成功')
    return file


def modify_t(sentence):
    s_modify1 = ""
    for stop in zhon.hanzi.stops:
        s_modify1 = sentence.replace(stop, "<EOS>")
    s_modify1 = s_modify1.strip()
    s_modify2 = "<BOS> " + s_modify1
    return re.split(" ", s_modify2)


def modify_fb(sentence):
    for stop in zhon.hanzi.stops:
        sentence = sentence.replace(stop, "")
    s_modify = re.split("\|", sentence)
    while "" in s_modify:
        s_modify.remove("")
    return s_modify


# 将语料中的每个句子进行分词处理，返回列表
def format_corpus():
    sentence = '[{characters}{radicals}{non_stops}]*{sentence_end}'.format(
        characters=zhon.hanzi.characters, radicals=zhon.hanzi.radicals, non_stops=zhon.hanzi.non_stops + " " + "|",
        sentence_end=zhon.hanzi._sentence_end)
    trainingCorpusPath = "E://Python/自然语言处理/实验三/训练语料/"
    fmmFilePath = "E://Python/自然语言处理/实验三/语料库_FMM/"
    bmmFilePath = "E://Python/自然语言处理/实验三/语料库_BMM/"
    trainingName = os.listdir(trainingCorpusPath)
    fmmFileName = os.listdir(fmmFilePath)
    bmmFileName = os.listdir(bmmFilePath)
    trainingFiles = {}
    fmmFiles = {}
    bmmFiles = {}
    for fName in fmmFileName:
        fmmFilesContent = []
        fContent = re.findall(sentence, read_file(fmmFilePath + fName))
        for f_content in fContent:
            fmmFilesContent.append(modify_fb(f_content))
        fmmFiles[fName] = fmmFilesContent
    for bName in bmmFileName:
        bmmFilesContent = []
        bContent = re.findall(sentence, read_file(bmmFilePath + bName))
        for b_content in bContent:
            bmmFilesContent.append(modify_fb(b_content))
        bmmFiles[bName] = bmmFilesContent
    for tName in trainingName:
        eosBos = []
        tContent = re.findall(sentence, read_file(trainingCorpusPath + tName))
        for t_content in tContent:
            eosBos.append(modify_t(t_content))
        trainingFiles[tName] = eosBos
    return trainingFiles, fmmFiles, bmmFiles


if __name__ == '__main__':
    t, f, b = format_corpus()
    print(t)
    print(f)
    print(b)
