# -*- coding: utf-8 -*-
# author：xxp time:2022/11/6
import formatcorpus

T, F, B = formatcorpus.T, formatcorpus.F, formatcorpus.B
single_frequency_dict = formatcorpus.single_frequency()
double_frequency_dict = formatcorpus.double_frequency()


def get_single_frequency(word):
    if word not in single_frequency_dict.keys():
        return 0
    else:
        return single_frequency_dict[word]


def get_double_frequency(double_word):
    if double_word not in double_frequency_dict.keys():
        return 0
    else:
        return double_frequency_dict[double_word]


def two_gram(sentence):
    p = 1
    bos_num = get_single_frequency("<BOS>")
    for i, word in enumerate(sentence):
        if i == 0:
            pre_word_num = get_double_frequency("<BOS>" + word)
            if pre_word_num == 0:
                p = 0
                break
            else:
                p = p * (pre_word_num / bos_num)
        else:
            pre_word_num = get_double_frequency(sentence[i - 1] + word)
            word_num = get_single_frequency(sentence[i - 1])
            if pre_word_num and word_num:
                p = p * (pre_word_num / word_num)
            else:
                p = 0
                break
    last_word_num = get_single_frequency(sentence[-1])
    last_double_num = get_double_frequency(sentence[-1] + "<EOS>")
    if last_word_num and last_double_num:
        p = p * (last_double_num / last_word_num)
    else:
        p = 0
    return p


def two_gram_smoothing(sentence):
    if two_gram(sentence) == 0:
        V = len(T)
        p = 1
        bos_num = get_single_frequency("<BOS>")
        for i, word in enumerate(sentence):
            if i == 0:
                pre_word_num = get_double_frequency("<BOS>" + word)
                p = p * ((pre_word_num + 1) / bos_num + V)
            else:
                pre_word_num = get_double_frequency(sentence[i - 1] + word)
                word_num = get_single_frequency(sentence[i - 1])
                p = p * ((pre_word_num + 1) / (word_num + V))
        last_word_num = get_single_frequency(sentence[-1])
        last_double_num = get_double_frequency(sentence[-1] + "<EOS>")
        p = p * ((last_double_num + 1) / (last_word_num + V))
        return p
    else:
        return 0
