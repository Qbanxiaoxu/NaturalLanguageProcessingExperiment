# -*- coding: utf-8 -*-
import re
import jieba
import os


class Word_Seg(object):
    def __init__(self, dic):
        self.dic = dic
        self.window_size = len(max(dic, key=len, default=''))

    def FMM(self, s):
        # 获取分词
        def getSeg(s):
            if not s:
                return ''
            if len(s) == 1:
                return s
            if s in self.dic:
                return s
            else:
                small = len(s) - 1
                s = s[0:small]
                return getSeg(s)

        s.strip()
        result_str = ""
        result_len = 0
        while s:
            tmp_str = s[0:self.window_size]
            seg_str = getSeg(tmp_str)
            seg_len = len(seg_str)
            result_len = result_len + seg_len
            # if seg_str.strip():
            #     result_str = result_str + seg_str + '|'
            result_str = result_str + seg_str + '|'
            s = s[seg_len:]
        # result_list = re.split(r'/', result_str[0:-1])
        return result_str

    def BMM(self, text):
        result_str = ''
        # bmm_result = []
        index = len(text)
        piece = ''
        while index > 0:
            for size in range(index - self.window_size, index):
                piece = text[size:index]
                if piece in self.dic:
                    index = size + 1
                    break
            index -= 1
            result_str = piece + '|' + result_str
        #     bmm_result.append(piece)
        # bmm_result.reverse()
        return result_str


def implement_FMM(root, fname, dic, word_num, word_standard_num, word_correct_num):
    wordSeg = Word_Seg(dic)
    # root_FMM = root + '_FMM/'  # FMM处理生成的语料库根目录
    root_FMM = root + '语料库_FMM/'
    # list_result=[]
    for name in fname:
        fcontent = ""
        fpath = root + "语料库/" + name
        with open(fpath, 'r', encoding='UTF-8') as f:
            fcontent += f.read()  # 先读取文件
        list_standard = jieba.lcut(fcontent)
        word_standard_num += len(list_standard)
        fmm_fcontent = ""
        fmm_fcontent += wordSeg.FMM(fcontent)
        list_fmm = fmm_fcontent.split("|")
        while '' in list_fmm:
            list_fmm.remove('')
        word_num += len(list_fmm)
        word_correct_num += get_correct_number(list_fmm, list_standard)
        try:
            with open(root_FMM + name, 'w') as f:
                f.write(fmm_fcontent)
        except UnicodeEncodeError:
            print("FMM处理：" + name + "——文件写入失败")
        else:
            print("FMM处理：" + name + "——文件写入完成")
    print("\nFMM分词处理PRF值分别为：")
    get_PRF(word_num, word_standard_num, word_correct_num)


# 将fname列表中的所有文件进行BMM分词处理并保存在新的文件夹
def implement_BMM(root, fname, dict, word_num, word_standard_num, word_correct_num):
    wordSeg = Word_Seg(dict)
    root_BMM = root + '语料库_BMM/'
    for name in fname:
        fcontent = ""
        fpath = root + "语料库/" + name
        with open(fpath, 'r', encoding='UTF-8') as f:
            fcontent += f.read()  # 先读取文件
        list_standard = jieba.lcut(fcontent)
        word_standard_num += len(list_standard)
        bmm_fcontent = ""
        bmm_fcontent += wordSeg.BMM(fcontent)
        list_bmm = bmm_fcontent.split("|")
        while '' in list_bmm:
            list_bmm.remove('')
        word_num += len(list_bmm)
        word_correct_num += get_correct_number(list_bmm, list_standard)
        try:
            with open(root_BMM + name, 'w') as f:
                f.write(bmm_fcontent)
        except UnicodeEncodeError:
            print("BMM处理：" + name + "——文件写入失败")
        else:
            print("BMM处理：" + name + "——文件写入完成")
    print("\nBMM分词处理PRF值分别为：")
    get_PRF(word_num, word_standard_num, word_correct_num)


# 获取文件中的正确分词数

def to_region(lst):
    region = []
    start = 0
    for word in lst:
        end = start + len(word)
        region.append((start, end))
        start = end
    return region


def get_correct_number(list_MM, list_jieba):
    a = to_region(list_MM)
    b = to_region(list_jieba)
    res = set(a) & set(b)
    return len(res)


def jieba_dict(root, fname, dict_path):  # 用jieba将root下的所有文件生成标准分词,并将词典中没有的词加入词典
    def isChinese(contents):
        zhmodel = re.compile('[^\u4e00-\u9fa5]')  # 检查中文
        match = zhmodel.search(contents)
        if match:
            return False
        else:
            return True

    for name in fname:
        fcontent = ''
        fpath = root + '语料库/' + name
        with open(fpath, 'r', encoding='UTF-8') as f:
            fcontent += f.read()  # 读取文本并进行处理
        list_jieba = jieba.lcut(fcontent)
        num = len(get_dict(dict_path))
        for word in list_jieba:
            init_dict = get_dict(dict_path)
            if isChinese(word) & (word not in init_dict):
                num += 1
                word_str = ""
                word_str += str(num) + ' ' + word
                with open(dict_path, 'a') as f:
                    f.write('\n' + word_str)
        print("字典添加：" + name + "——分词结果，文件写入完成")


def get_dict(fpath):
    with open(fpath, 'r') as f:
        dic_content = f.readlines()
    dic_lst = []
    for i in dic_content:
        i = ''.join(re.findall('[\u4e00-\u9fa5]', i))
        if len(i) != 0:
            dic_lst.append(i)
    return dic_lst


# 获取根目录下所有文件的文件名
def read_file(root):
    file_name = os.listdir(root)
    return file_name


def get_PRF(word_num, word_standard_num, word_correct_num):
    p = word_correct_num / word_num
    r = word_correct_num / word_standard_num
    f = (2 * p * r) / (r + p)
    print("word_num:{0}\tword_standard_num:{1}\tword_correct_num:{2}\t\n".format(word_num, word_standard_num, word_correct_num))
    print("P:{0:.2%}\tR:{1:.2%}\tF:{2:.2%}\t\n".format(p, r, f))


def auto_split(root):
    fpath = root + '语料库/'
    dict_path = "E://Python/自然语言处理/实验二/wordlist.Dic"
    file_name = read_file(fpath)  # 读取并保存根目录下所有文件名
    word_num = 0  # 记录系统分词数
    word_standard_num = 0  # 记录标准答案分词数
    word_correct_num = 0  # 记录正确分词数
    jieba_dict(root, file_name, dict_path)
    dic = get_dict(dict_path)
    implement_FMM(root, file_name, dic, word_num, word_standard_num, word_correct_num)
    implement_BMM(root, file_name, dic, word_num, word_standard_num, word_correct_num)


def main():
    root = "E://Python/自然语言处理/实验二/"
    auto_split(root)


if __name__ == '__main__':
    main()
