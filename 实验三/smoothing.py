# 判断两个分词结果是否相同
def is_equal(wordSeg1, wordSeg2):
    if wordSeg1 == wordSeg2:
        return True
    else:
        return False


def word_frequency(word):  # 计算词出现的频度
    return 0


def get_probability(wordSeg):  # 计算句子出现的概率
    return 0


# 判断分词的句子是否存在数据稀疏问题，若存在，用加1方法处理
def smoothing(wordSeg, v):  # wordSeg是分词结果,v为被考虑语料的词汇量
    p = get_probability(wordSeg)
    # 如果句子出现的概率为0，判断出现了数据稀疏，使用加一进行平滑处理
    smoothing_p = 1
    if p == 0:
        for i, element in enumerate(wordSeg):
            if i == 0:
                smoothing_p = smoothing_p * (word_frequency('<BOS>' + element) + 1) / (v + word_frequency('<BOS>'))
                print(smoothing_p)
            else:
                smoothing_p = smoothing_p * (word_frequency(wordSeg[i - 1] + element) + 1) / (
                            v + word_frequency(wordSeg[i - 1]))
    smoothing_p = smoothing_p * (word_frequency(wordSeg[-1] + '<EOS>') + 1) / (v + word_frequency(wordSeg[-1]))
    return smoothing_p


if __name__ == '__main__':
    test = ['Cher', 'read', 'a', 'book']
    p = smoothing(test, 11)
    print("{:.5f}".format(p))
