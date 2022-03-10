import networkx as nx
import matplotlib.pyplot as plt
import heapq

import numpy as np
import pandas as pd

'''
制图思路：从csv文件表中读取数据，选取十条评分最高的数据，进行构图，
'''


def draw(file):
    G = {}
    data = pd.read_csv(file)
    data = np.array(data)
    data = data.T
    for i in range(0, len(data)):  #len(data)为21
        datas = data[i].tolist()
        max_number = heapq.nlargest(11, datas)  #最大的前10个值

        # 最大的2个数对应的，如果用nsmallest则是求最小的数及其索引
        max_index = map(datas.index, heapq.nlargest(11, datas))
        # max_index 直接输出来不是数，使用list()或者set()均可输出
        # print(list(set(max_index)))
        index = list(max_index)   #index[1]~idnex[10]代表政策编号

        # 序号3 索引 index 值 max_number
        # 画图
        del (index[0])  # 节点
        del (max_number[0])  # 权重
        G[i] = nx.DiGraph()
        for j in range(0, len(max_number)):
            G[i].add_node(index[j])
            G[i].add_weighted_edges_from([(i, index[j], int(max_number[j] * 100))])
        pos = nx.spring_layout(G[i])
        # node_labels = nx.get_node_attributes(G, 'name')  # 获取节点的name属性
        # nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)  # 将name属性，显示在节点上
        edge_labels = nx.get_edge_attributes(G[i], 'weight')  # 获取边的name属性，
        nx.draw_networkx_edge_labels(G[i], pos, edge_labels=edge_labels)  # 将weight属性，显示在边上
        # print(G[i].edges.data())

        nx.draw_networkx(G[i], edge_color='green', node_size=800, width=2.5, node_shape=',')
        path = '../picture/' + str(i) + '.png'
        plt.savefig(path)
        # plt.show()
        G[i].clear()
        plt.close()




draw('D:\科研/recom_system/recom/recom/工作簿1.csv')




