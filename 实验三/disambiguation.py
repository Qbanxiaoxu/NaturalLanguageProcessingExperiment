# -*- coding: utf-8 -*-
# author：xxp time:2022/11/6
import os

import jieba

import two_gram
import format_corpus
import prf


def write_to_file(fpath, sentence):
    temp_sentence = ""
    for word in sentence:
        temp_sentence = temp_sentence + word + "|"
    new_sentence = temp_sentence[:-1]
    try:
        if not os.path.exists(fpath):
            with open(fpath, 'w') as f:
                f.write(new_sentence)
                f.close()
        else:
            with open(fpath, 'a') as f:
                f.write("。" + new_sentence)
                f.close()
    except UnicodeEncodeError:
        print(fpath + "——写入失败")
    else:
        print(fpath + "——写入完成")


def disambiguation(path):
    file_name = format_corpus.originFileName
    word_number = 0  # 分词数
    correct_number = 0  # 正确分词数
    standard_number = 0  # jieba分词数
    for fName in file_name:
        fmm_file = format_corpus.F[fName]
        bmm_file = format_corpus.B[fName]
        for i in range(len(bmm_file)):
            if fmm_file[i] and bmm_file[i]:
                if fmm_file[i] != bmm_file[i]:
                    fmm_probability = two_gram.two_gram_smoothing(fmm_file[i])
                    bmm_probability = two_gram.two_gram_smoothing(bmm_file[i])
                    if fmm_probability > bmm_probability:
                        ambiguity_sentence = fmm_file[i]
                    else:
                        ambiguity_sentence = bmm_file[i]

                    temp_sentence = ""
                    for word in ambiguity_sentence:
                        temp_sentence = temp_sentence + word
                    new_sentence = temp_sentence
                    jieba_list = jieba.lcut(new_sentence)
                    standard_number += len(jieba_list)

                    word_number += len(ambiguity_sentence)
                    correct_number += prf.get_correct_number(ambiguity_sentence, jieba_list)
                    write_to_file(path + fName, ambiguity_sentence)
                else:
                    temp_sentence = ""
                    for word in fmm_file[i]:
                        temp_sentence = temp_sentence + word
                    new_sentence = temp_sentence
                    jieba_list = jieba.lcut(new_sentence)
                    standard_number += len(jieba_list)

                    word_number += len(fmm_file[i])
                    correct_number += prf.get_correct_number(fmm_file[i], jieba_list)
                    write_to_file(path + fName, fmm_file[i])
    prf.get_prf(word_number, correct_number, standard_number)


if __name__ == '__main__':
    new_path = "E://Python/自然语言处理/实验三/消歧语料库/"
    disambiguation(new_path)
