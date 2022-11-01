import numpy as np
import pandas as pd
import json


# 序列化与反序列树字典
class TreeHandler(object):
    def __init__(self):
        self.tree = None

    def save(self, tree):
        self.tree = tree
        with open("tree.txt", mode="w", encoding="utf-8") as f:
            tree = json.dumps(tree, indent="  ", ensure_ascii=False)
            f.write(tree)

    def load(self, file):
        with open(file, mode="r", encoding="utf-8") as f:
            tree = f.read()
            self.tree = json.loads(tree)
        return self.tree


#
class ID3Tree(TreeHandler):
    """主要的数据结构是pandas对象"""
    __count = 0

    def __init__(self):
        super().__init__()
        """认定最后一列是标签列"""
        self.gain = {}

    def _entropy(self, dataSet):
        """计算给定数据集的熵"""
        labels = list(dataSet.columns)
        level_count = dataSet[labels[-1]].value_counts().to_dict()  # 统计分类标签不同水平的值
        entropy = 0.0
        for key, value in level_count.items():
            prob = float(value) / dataSet.shape[0]
            entropy += -prob * np.log2(prob)
        return entropy

    def _split_dataSet(self, dataSet, column, level):
        """根据给定的column和其level来获取子数据集"""
        subdata = dataSet[dataSet[column] == level]
        del subdata[column]  # 删除这个划分字段列
        return subdata.reset_index(drop=True)  # 重建索引

    def _best_split(self, dataSet):
        """计算每个分类标签的信息增益"""
        best_info_gain = 0.0  # 求最大信息增益
        best_label = None  # 求最大信息增益对应的标签(字段)
        labels = list(dataSet.columns)[: -1]  # 不包括最后一个靶标签
        init_entropy = self._entropy(dataSet)  # 先求靶标签的香农熵
        for _, label in enumerate(labels):
            # 根据该label(也即column字段)的唯一值(levels)来切割成不同子数据集，并求它们的香农熵
            levels = dataSet[label].unique().tolist()  # 获取该分类标签的不同level
            label_entropy = 0.0  # 用于累加各水平的信息熵；分类标签的信息熵等于该分类标签的各水平信息熵与其概率积的和。
            for level in levels:  # 循环计算不同水平的信息熵
                level_data = dataSet[dataSet[label] == level]  # 获取该水平的数据集
                prob = level_data.shape[0] / dataSet.shape[0]  # 计算该水平的数据集在总数据集的占比
                # 计算香农熵，并更新到label_entropy中
                label_entropy += prob * self._entropy(level_data)  # _entropy用于计算香农熵
            # 计算信息增益
            info_gain = init_entropy - label_entropy  # 代码至此，已经能够循环计算每个分类标签的信息增益
            print("++++++++++++++")
            print("label: {3}   Gain(D,a): {0}    Ent(D): {1}   Ent(Dv): {2}".format(info_gain, init_entropy,
                                                                                     label_entropy, label))
            print("--------------")
            # 用best_info_gain来取info_gain的最大值，并获取对应的分类标签
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_label = label
            # 这里保存一下每一次计算的信息增益，便于查看和检查错误
            self.gain.setdefault(self.__count, {})  # 建立本次函数调用时的字段，设其value为字典
            self.gain[self.__count][label] = info_gain  # 把本次函数调用时计算的各个标签数据存到字典里
        self.__count += 1
        return best_label

    def _top_amount_level(self, target_list):
        class_count = target_list.value_counts().to_dict()  # 计算靶标签的不同水平的样本量，并转化为字典
        # 字典的items方法可以将键值对转成[(), (), ...]，可以使用列表方法
        sorted_class_count = sorted(class_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_class_count[0][0]

    def mktree(self, dataSet):
        """创建决策树"""
        target_list = dataSet.iloc[:, -1]  # target_list 靶标签的那一列数据
        # 程序终止条件一: 靶标签(数据集的最后一列因变量)在该数据集上只有一个水平，返回该水平
        if target_list.unique().shape[0] <= 1:
            return target_list[0]  # ！！！
        # 程序终止条件二: 数据集只剩下把标签这一列数据；返回数量最多的水平
        if dataSet.shape[1] == 1:
            return self._top_amount_level(target_list)
        # 不满足终止条件时，做如下递归处理
        # 1.选择最佳分类标签
        best_label = self._best_split(dataSet)
        # 2.递归计算最佳分类标签的不同水平的子数据集的信息增益
        #   各个子数据集的最佳分类标签的不同水平...
        #   ...
        #   直至递归结束
        best_label_levels = dataSet[best_label].unique().tolist()
        tree = {best_label: {}}  # 生成字典，用于保存树状分类信息；这里不能用self.tree = {}存储
        for level in best_label_levels:
            level_subdata = self._split_dataSet(dataSet, best_label, level)  # 获取该水平的子数据集
            tree[best_label][level] = self.mktree(level_subdata)  # 返回结果
        return tree

    def predict(self, tree, labels, test_sample):
        """
        对单个样本进行分类
        tree: 训练的字典
        labels: 除去最后一列的其它字段
        test_sample: 需要分类的一行记录数据
        """
        classLabel = None
        firstStr = list(tree.keys())[0]  # tree字典里找到第一个用于分类键值对
        secondDict = tree[firstStr]
        featIndex = labels.index(firstStr)  # 找到第一个建(label)在给定label的索引
        for key in secondDict.keys():
            if test_sample[featIndex] == key:  # 找到test_sample在当前label下的值
                if secondDict[key].__class__.__name__ == "dict":
                    classLabel = self.predict(secondDict[key], labels, test_sample)
                else:
                    classLabel = secondDict[key]
        return classLabel

    def _unit_test(self):
        """用于测试_entropy函数"""
        data = [
            ['晴', '炎热', '高', '弱', '取消'],  # 1
            ['晴', '炎热', '高', '强', '取消'],  # 2
            ['阴', '炎热', '高', '弱', '进行'],  # 3
            ['雨', '适中', '高', '弱', '进行'],  # 4
            ['雨', '寒冷', '正常', '弱', '进行'],  # 5
            ['雨', '寒冷', '正常', '强', '取消'],  # 6
            ['阴', '寒冷', '正常', '强', '进行'],  # 7
            ['晴', '适中', '高', '弱', '取消'],  # 8

            ['晴', '寒冷', '正常', '弱', '进行'],  # 9
            ['雨', '适中', '正常', '弱', '进行'],  # 10
            ['晴', '适中', '正常', '强', '进行'],  # 11
            ['阴', '适中', '高', '强', '进行'],  # 12
            ['阴', '炎热', '正常', '弱', '进行'],  # 13
            ['雨', '适中', '高', '强', '取消'],  # 14
        ]
        data = pd.DataFrame(data=data, columns=['天气', '温度', '湿度', '风速', '活动'])
        # return data # 到此行，用于测试_entropy
        # return self._split_dataSet(data, "a", 1)  # 到此行，用于测试_split_dataSet
        # return self._best_split(data)  # 到此行，用于测试_best_split
        # return self.mktree(self.dataSet)  # 到此行，用于测试主程序mktree
        # 生成树
        self.tree = self.mktree(data)  # 到此行，用于测试主程序mktree
        # 打印树
        print(self.tree)
        # labels = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感']
        # 测试样本
        # test_sample = ['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑']
        # 预测结果
        # outcome = self.predict(self.tree, labels, test_sample)
        # print("The truth class is %s, The ID3Tree outcome is %s." % ("否", outcome))


model = ID3Tree()
model._unit_test()

# import matplotlib.pyplot as plt
# from pylab import *
#
# mpl.rcParams['font.sans-serif'] = ['SimHei']
# plt.figure(1, figsize=(8, 8))
# ax = plt.subplot(111)
#
#
# def drawNode(text, startX, startY, endX, endY, ann):
#     # 绘制带箭头的文本
#     ax.annotate(text,
#                 xy=(startX + 0.01, startY), xycoords='data',
#                 xytext=(endX, endY), textcoords='data',
#                 arrowprops=dict(arrowstyle="<-",
#                                 connectionstyle="arc3"),
#                 bbox=dict(boxstyle="square", fc="r")
#                 )
#     # 在箭头中间位置标记数字
#     ax.text((startX + endX) / 2, (startY + endY) / 2, str(ann))
#
#
# # 绘制树根
# bbox_props = dict(boxstyle="square,pad=0.3", fc="cyan", ec="b", lw=2)
# ax.text(0.5, 0.97, '纹理', bbox=bbox_props)
# # 绘制其他节点
# drawNode('根蒂', 0.5, 0.97, 0.25, 0.8, "清晰")
# drawNode('触感', 0.5, 0.97, 0.50, 0.8, "稍糊")
# drawNode('坏瓜', 0.5, 0.8, 0.4, 0.65, "硬滑")
# drawNode('好瓜', 0.5, 0.8, 0.6, 0.65, "硬滑")
# drawNode('坏瓜', 0.5, 0.97, 0.75, 0.8, "模糊")
# drawNode('好瓜', 0.25, 0.8, 0.1, 0.65, "蜷缩")
# drawNode('色泽', 0.25, 0.8, 0.2, 0.65, "稍蜷")
# drawNode('好瓜', 0.25, 0.8, 0.3, 0.65, "硬挺")
# drawNode('好瓜', 0.2, 0.65, 0.1, 0.5, "青绿")
# drawNode('触感', 0.2, 0.65, 0.25, 0.5, "乌黑")
# drawNode('好瓜', 0.25, 0.5, 0.1, 0.35, "硬滑")
# drawNode('坏瓜', 0.25, 0.5, 0.4, 0.35, "软粘")
# # 显示图形
# plt.show()
