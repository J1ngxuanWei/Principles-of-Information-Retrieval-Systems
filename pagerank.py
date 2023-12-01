import pickle
import networkx

def get_pagerank():
    """
    计算网页权重
    """
    # 打开url跳转字典
    url_jump_dic = dict()
    with open("dataset/url_jump_dic.pkl", "rb") as tf:
        url_jump_dic = pickle.load(tf)
    # url对应的id
    url_find_id_dic = dict()
    with open("dataset/id_url_dic.pkl", "rb") as tf1:
        url_find_id_dic = pickle.load(tf1)
    # 构造一个图
    graph = networkx.DiGraph()
    # 遍历字典中的所有url keys()
    for i in range(0, len(url_jump_dic)):
        for j in url_jump_dic[i]:
            if j in url_find_id_dic.keys():
                # 构造从 i 到 j 的边
                graph.add_edge(i, url_find_id_dic[j])
    # 计算 page rank
    my_page_rank = networkx.pagerank(graph)
    # 把这个字典写到本地文件中
    with open("dataset/id_pagerank_dic.pkl", "wb") as tf2:
        pickle.dump(my_page_rank, tf2)
    tf.close()
    tf1.close()
    tf2.close()

if __name__ == '__main__':
    get_pagerank()
