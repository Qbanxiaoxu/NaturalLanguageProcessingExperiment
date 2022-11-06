# # import re
# #
# # import zhon.hanzi
# #
# # str = "１９９７年 ， 是 中国 发展 历史 上 非常 重要 的 很 不 平凡 的 一 年 。 \n中国 人民 决心 继承 邓 小平 同志 的 遗志 ， 继续 把 建设 有 中国 特色 社会主义 事业 推向 前进 。 中国 政府 顺利 恢复 对 香港 行使 主权 ， 并 按照 “ 一国两制 ” 、 “ 港人治港 ” 、 高度 自治 的 方针 保持 香港 的 繁荣 稳定 。 中国 共产党 成功 地 召开 了 第十五 次 全国 代表大会 ， 高举 邓小平理论 伟大 旗帜 ， 总结 百年 历史 ， 展望 新 的 世纪 ， 制定 了 中国 跨 世纪 发展 的 行动 纲领 。"
# # print(re.findall(zhon.hanzi.sentence, str, re.S))
#
# import re
# import zhon.hanzi
#
# # import re
# #
# #
# # def cut_sentences(content):
# #     sentences = re.split(r'([，。！？])', content)
# #     while '。' in sentences:
# #         sentences.remove('。')
# #     while '！' in sentences:
# #         sentences.remove('！')
# #     while '，' in sentences:
# #         sentences.remove('，')
# #     while '？' in sentences:
# #         sentences.remove('？')
# #     while '' in sentences:
# #         sentences.remove('')
# #     return sentences
# #
# #
# # content = '在处理文本时，会遇到需要将文本以 句子 为单位进行切分（分句）的场景，而文本又可以分为 中文文本 和 英文文本 ，处理的方法会略有不同。\n本文会介绍 Python 是如何处理 分句 的。'
# # sentences = cut_sentences(str)
# # print(sentences)
# import os
# import re
#
# import zhon.hanzi
# from zhon.pinyin import punctuation
#
#
# def read_file(fpath):
#     try:
#         if os.path.exists(fpath):
#             with open(fpath, 'r', encoding="utf-8") as f:
#                 file = f.read()
#                 f.close()
#         else:
#             print('文件不存在')
#     except UnicodeDecodeError:
#         with open(fpath, 'r', encoding="gbk") as f:
#             file = f.read()
#             f.close()
#     else:
#         print('读取成功')
#     return file
#
#
# # t, sentences = read_file("E://Python/自然语言处理/实验三/训练语料/1998人民日报（分词）.txt")
# # print(t)
# # print("\n\n\n\n\n")
# # print(sentences)
# def getfile():
#     sentence = '[{characters}{radicals}{non_stops}]*{sentence_end}'.format(
#         characters=zhon.hanzi.characters, radicals=zhon.hanzi.radicals, non_stops=zhon.hanzi.non_stops + " ",
#         sentence_end=zhon.hanzi._sentence_end)
#
#     rst = re.findall(sentence, read_file("E://Python/自然语言处理/实验三/训练语料/1998人民日报（分词）.txt"))
#     return rst
# # print(rst)
#
#
# # for sen in rst:
# #     eosBos.append(re.split(" ", sen))
# # print(eosBos)
# # print(zhon.hanzi.stops)
#
#
# def Modify(s):
#     s_modify1 = ""
#     for stop in zhon.hanzi.stops:
#         s_modify1 = s.replace(stop, "<EOS>")
#     s_modify1=s_modify1.strip()
#     s_modify2 = "<BOS> " + s_modify1
#     return re.split(" ",s_modify2)
#
#
# s = "  １９９７年 ， 是 中国 发展 历史 上 非常 重要 的 很 不 平凡 的 一 年 。"
# # print(Modify(s))
# # print(re.split(" ", Modify(s)))
# # eosbos=[]
# # rst=getfile()
# # for sen in rst:
# #     eosbos.append(Modify(sen))
# # print(eosbos)
# def modify_fb(sentence):
#     for stop in zhon.hanzi.stops:
#         sentence=sentence.replace(stop, "")
#     s_modify=re.split("\|",sentence)
#     while "" in s_modify:
#         s_modify.remove("")
#     return s_modify
# def getfile_fb():
#     sentence = '[{characters}{radicals}{non_stops}]*{sentence_end}'.format(
#         characters=zhon.hanzi.characters, radicals=zhon.hanzi.radicals, non_stops=zhon.hanzi.non_stops + " "+"|",
#         sentence_end=zhon.hanzi._sentence_end)
#
#     rst = re.findall(sentence, read_file("E://Python/自然语言处理/实验三/语料库_BMM/诺贝尔奖即将揭晓 这些华人科学家被看好.txt"))
#     return rst
#
# file=getfile_fb()
# print(file)
# fb_file=[]
# for sen in file:
#     fb_file.append(modify_fb(sen))
# print(fb_file)
from 实验三.disambiguation import disambiguation

if __name__ == '__main__':
    new_path = "E://Python/自然语言处理/实验三/消歧语料库语料库/"
    disambiguation(new_path)