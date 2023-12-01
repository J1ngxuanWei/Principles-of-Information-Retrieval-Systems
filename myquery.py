import os
import pickle

from whoosh import query
from whoosh import qparser
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh import scoring, fields, index
from whoosh.query import Phrase

from user import getrandomlabel

indexdir = 'indexdir/'
indexnanp = 'wjx1'
ixnp = open_dir(indexdir, indexnanp)
indexnawp = 'wjx2'
ixwp = open_dir(indexdir, indexnawp)
storedir = 'user/store/'

def getrank(ptr):
    # id对应的url
    with open("dataset/id_pagerank_dic.pkl", "rb") as tf1:
        url_id_dic = pickle.load(tf1)
    score = url_id_dic[int(ptr)]
    tf1.close()
    return score

def initpa(title,text,tourl):
    for i in range(0,6):
        title[i]='没有搜索结果'
        text[i]='没有搜索结果'
        tourl[i]=''

def gettitle(id):
    with open("dataset/title_id_dic.pkl", "rb") as tf1:
        title_id_dic = pickle.load(tf1)
    title = title_id_dic[int(id)]
    tf1.close()
    return title

# 自定义评分器
class CustomScorer(scoring.BM25F):
    def __init__(self, id_weight=1.0, **kwargs):
        super().__init__(**kwargs)
        self.id_weight = id_weight

    def score(self, searcher, docnum, text, weight):
        bm25f_score = super().score(searcher, docnum, text, weight)
        doc = searcher.stored_fields(docnum)
        id_score = doc.get("id", 0)  # 获取文档的 ID 值，如果不存在，则默认为0
        return bm25f_score * (self.id_weight * getrank(id_score))


# 获取自定义评分器
custom_scorer = CustomScorer(id_weight=1.0, fieldnum=0, content_B=0.75, content_K1=1.5)


def commonsearch(keyword,title,text,tourl):
    """
    没有任何限制的查询,普通查询
    """
    initpa(title,text,tourl)
    with ixnp.searcher(weighting=custom_scorer) as searcher:
        query = QueryParser("content", ixnp.schema).parse(keyword)
        results = searcher.search(query)
        for i in range(0,min(6,len(results))):
            temp_result = results[i]
            for field_name, field_value in temp_result.items():
                if field_name=='content':
                    text[i]=field_value[:150]
                if field_name=='url':
                    tourl[i] = field_value
                if field_name=='id':
                    title[i] = gettitle(field_value)

#0是text,1是id,2是url

def instasearch(keyword, url,title,text,tourl):
    """
    站内查询
    本质上就是查询这个站的url与正文，是通配查询的一部分
    """
    initpa(title, text, tourl)
    with ixnp.searcher(weighting=custom_scorer) as searcher:
        # 创建查询解析器
        parser = qparser.MultifieldParser(["content", "url"], ixnp.schema)
        # 构建查询
        query = parser.parse(f'content:{keyword} AND url:{url}*')
        results = searcher.search(query)
        for i in range(0, min(6, len(results))):
            temp_result = results[i]
            for field_name, field_value in temp_result.items():
                if field_name == 'content':
                    text[i]=field_value[:150]
                if field_name == 'url':
                    tourl[i] = field_value
                if field_name == 'id':
                    title[i] = gettitle(field_value)


def phrasesearch(keyword,title,text,tourl):
    """
    短语查询
    """
    initpa(title, text, tourl)
    with ixwp.searcher(weighting=custom_scorer) as searcher:
        query_parser = QueryParser("content", ixwp.schema)
        query = query_parser.parse(keyword)
        results = searcher.search(query)
        for i in range(0, min(6, len(results))):
            temp_result = results[i]
            for field_name, field_value in temp_result.items():
                if field_name == 'content':
                    text[i]=field_value[:150]
                if field_name == 'url':
                    tourl[i] = field_value
                if field_name == 'id':
                    title[i] = gettitle(field_value)

def wildcardsearch(keyword,title,text,tourl):
    """
    通配查询
    """
    initpa(title, text, tourl)
    with ixnp.searcher(weighting=custom_scorer) as searcher:
        query_parser = QueryParser("content", ixnp.schema)
        query = query_parser.parse(keyword)
        results = searcher.search(query)
        for i in range(0, min(6, len(results))):
            temp_result = results[i]
            for field_name, field_value in temp_result.items():
                if field_name == 'content':
                    text[i]=field_value[:150]
                if field_name == 'url':
                    tourl[i] = field_value
                if field_name == 'id':
                    title[i] = gettitle(field_value)


def likesearch(uid,title1,text1,tourl1,title2,text2,tourl2):
    """
    推荐查询，根据用户的标签来检索推荐内容
    1是最大的label
    2是次大的label
    """
    initpa(title1, text1, tourl1)
    initpa(title2, text2, tourl2)
    if uid == 0:
        return 1
    str=getrandomlabel(uid)
    keyword1=str[0]
    keyword2=str[1]
    commonsearch(keyword1,title1,text1,tourl1)
    commonsearch(keyword2,title2,text2,tourl2)
    while title1[0]=='没有搜索结果' or title2[0]=='没有搜索结果':
        str = getrandomlabel(uid)
        keyword1 = str[0]
        keyword2 = str[1]
        commonsearch(keyword1, title1, text1, tourl1)
        commonsearch(keyword2, title2, text2, tourl2)

def rise(title,text,tourl,ptr):
    temp1 = title[ptr]
    temp2 = text[ptr]
    temp3 = tourl[ptr]
    title[ptr]=title[0]
    text[ptr]=text[0]
    tourl[ptr]=tourl[0]
    title[0]=temp1
    text[0]=temp2
    tourl[0]=temp3



def resort(uid,title,text,tourl,title1, text1, tourl1, title2, text2, tourl2):
    """
    个性化查询，根据用户的标签来重排序搜索结果
    分两个优先级，先通过用户画像重排序，再通过用户的赞排序
    """
    for i in range(0,len(title)):
        if title[i]=='没有搜索结果':
            continue
        if title[i] in title1 or title[i] in title2:
            rise(title,text,tourl,i)
    file_names = [f for f in os.listdir(storedir) if f.endswith('.txt')]
    for i in range(0,len(tourl)):
        if tourl[i]=='':
            continue
        with open("dataset/id_url_dic.pkl", "rb") as tf1:
            id_url_dic = pickle.load(tf1)
        myid = id_url_dic[tourl[i]]
        tf1.close()
        for file_name in file_names:
            result = file_name.split('.')[0]
            file_path = os.path.join(storedir, file_name)
            if int(result) == int(uid):
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        toid = int(line.strip())
                        if toid==myid:
                            rise(title,text,tourl,i)



if __name__ == '__main__':
    title = dict()
    text = dict()
    tourl = dict()
    wildcardsearch('的*',title,text,tourl)
    #instasearch('原神', 'https://www.ali213.net/news/html/2023-11')
    #phrasesearch('不平')
