import numpy as np
import jieba
from sklearn.cluster import KMeans

#对分布均匀的类别进行聚类后重新分配类别名称，缩减类别数量
class ClassKMeans():
    stopwords_f = 'stop_words.txt'
    stopwords = list()
    wordspace = set()

    def __init__(self, stopword=None):
        if stopword is not None:
            self.stopwords_f = stopword
        for line in open(self.stopwords_f, 'r', encoding='utf-8'):
            self.stopwords.append(line.strip('\n'))

    #对单句切词并删除停用词
    def _cut_stop(self, line):
        rt = list()
        for word in jieba.cut(line):
            if word not in self.stopwords:
                rt.append(word)
        return rt

    #构建词袋空间
    def _wordspace(self, docs):
        for doc in docs:
            doc_set = set(self._cut_stop(doc))
            self.wordspace |= doc_set

    #对单句进行词向量转换
    def _to_vector(self, line):
        doc_list = self._cut_stop(line)
        doc_vector = np.zeros(len(self.wordspace))
        for index, value in enumerate(self.wordspace):
            if value in doc_list:
                doc_vector[index] += 1.0
        return doc_vector

    #整体列表转换为词向量矩阵
    def _to_vector_matrix(self, docs):
        self._wordspace(docs)
        return np.array([self._to_vector(x) for x in docs])

    #KMeans模型训练，返回新类别列表
    def newClass(self, docs, k=10):
        clf = KMeans(n_clusters=k)
        mod = clf.fit(self._to_vector_matrix(docs))
        labels = clf.labels_
        dict_f = dict()
        new_docs = list()
        for index, value in enumerate(labels):
            if value not in dict_f.keys():
                dict_f[value] = docs[index]
            new_docs.append(dict_f[value])
        return new_docs

