import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import pickle


def geturl(ptr):
    # id对应的url
    with open("dataset/url_id_dic.pkl", "rb") as tf1:
        url_id_dic = pickle.load(tf1)
    url = url_id_dic[int(ptr)]
    return url


def makeindexnotpar():
    """
    创建索引，不记录term的位置，不支持邻近的短语查询
    """
    analyzer = ChineseAnalyzer()
    schema = Schema(url=ID(stored=True, analyzer=analyzer),
                    content=TEXT(stored=True, phrase=False, analyzer=analyzer),
                    id=ID(stored=True, analyzer=analyzer))

    indexdir = 'indexdir/'
    indexna = 'wjx1'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema, indexna)

    # 获取目录中文件列表并计算数量
    datadir = 'dataset/web_data/'
    # 定义正则表达式来匹配文件名中的开头数字部分
    pattern = re.compile(r'^(\d+)_')
    file_names = [f for f in os.listdir(datadir) if f.endswith('.txt')]

    writer = ix.writer()
    for file_name in file_names:
        file_path = os.path.join(datadir, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用正则表达式匹配文件名中的开头数字部分
            match = pattern.match(file_name)
            if match:
                first_number = match.group(1)
            else:
                first_number = None
            mycontent = file.read()
            writer.add_document(url=geturl(first_number), content=mycontent, id=first_number)
    writer.commit()


def makeindexwithpar():
    """
    创建索引，记录term的位置，支持邻近的短语查询
    """
    analyzer = ChineseAnalyzer()
    schema = Schema(url=ID(stored=True, analyzer=analyzer),
                    content=TEXT(stored=True, phrase=True, analyzer=analyzer),
                    id=ID(stored=True, analyzer=analyzer))

    indexdir = 'indexdir/'
    indexna = 'wjx2'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema, indexna)

    # 获取目录中文件列表并计算数量
    datadir = 'dataset/web_data/'
    # 定义正则表达式来匹配文件名中的开头数字部分
    pattern = re.compile(r'^(\d+)_')
    file_names = [f for f in os.listdir(datadir) if f.endswith('.txt')]

    writer = ix.writer()
    for file_name in file_names:
        file_path = os.path.join(datadir, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用正则表达式匹配文件名中的开头数字部分
            match = pattern.match(file_name)
            if match:
                first_number = match.group(1)
            else:
                first_number = None
            mycontent = file.read()
            writer.add_document(url=geturl(first_number), content=mycontent, id=first_number)
    writer.commit()


def initindex():
    makeindexnotpar()
    makeindexwithpar()

if __name__ == '__main__':
    makeindexnotpar()
    makeindexwithpar()
