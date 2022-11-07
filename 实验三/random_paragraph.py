import random
import two_gram
import format_corpus


def random_order(paragraph):
    p1 = two_gram.two_gram_smoothing(paragraph)  # 打乱前的概率
    print("打乱前句子：", paragraph)
    random.shuffle(paragraph)  # 将原列表打乱语序
    print("打乱后句子：", paragraph)
    p2 = two_gram.two_gram_smoothing(paragraph)  # 打乱后的概率
    print("打乱语序前句子的概率为：{0:.30%}".format(p1))
    print("打乱语序后句子的概率为：{0:.30%}".format(p2))


def random_paragraph():
    if len(format_corpus.originFileName) - 1 <= 0:
        random_file_num = 0
    else:
        random_file_num = random.randint(0, len(format_corpus.originFileName) - 1)
    random_file_name = format_corpus.originFileName[random_file_num]
    if random.randint(0, 1):
        random_file = format_corpus.B[random_file_name]
    else:
        random_file = format_corpus.F[random_file_name]
    if len(random_file) - 1 <= 0:
        random_sentence_num = 0
    else:
        random_sentence_num = random.randint(0, len(random_file) - 1)
    random_sentence = random_file[random_sentence_num]  # 下标会超出范围？？？
    random_order(random_sentence)


if __name__ == '__main__':
    random_paragraph()
