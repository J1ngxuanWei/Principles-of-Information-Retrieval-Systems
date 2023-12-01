import os
import pickle

from flask import Flask, request, render_template, redirect, url_for

from myquery import commonsearch
from myquery import instasearch
from myquery import phrasesearch
from myquery import wildcardsearch
from myquery import likesearch
from myquery import resort
from user import getuid
from user import store
from user import addlabel
from printlog import seartolog

from spider import mainspider
from getindex import initindex
from pagerank import get_pagerank
from printlog import initsearlog
from user import initlogin

app = Flask(__name__)

stateurl = 'empty'
ispar = False
iswild = False
globaluid = 00000


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST' and request.form.get('keyword'):
        keyword = request.form['keyword']
        return redirect(url_for('searchto', keyword=keyword))
    title1 = dict()
    text1 = dict()
    tourl1 = dict()
    title2 = dict()
    text2 = dict()
    tourl2 = dict()
    likesearch(globaluid,title1,text1,tourl1,title2,text2,tourl2)
    return render_template("index.html", uid=globaluid,
                           l1t=title1[0], l1c=text1[0], l1u=tourl1[0],
                           l2t=title2[0], l2c=text2[0], l2u=tourl2[0])


@app.route('/shouye', methods=['POST', 'GET'])
def shouye():  # put application's code here
    if request.method == 'POST' and request.form.get('keyword'):
        keyword = request.form['keyword']
        return redirect(url_for('searchto', keyword=keyword))
    title1 = dict()
    text1 = dict()
    tourl1 = dict()
    title2 = dict()
    text2 = dict()
    tourl2 = dict()
    likesearch(globaluid, title1, text1, tourl1, title2, text2, tourl2)
    return render_template("index.html", uid=globaluid,
                           l1t=title1[0], l1c=text1[0], l1u=tourl1[0],
                           l2t=title2[0], l2c=text2[0], l2u=tourl2[0])


@app.route('/login', methods=['POST', 'GET'])
def login():  # put application's code here
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('loginto', username=username, password=password))
    return render_template("login.html", uid=globaluid)


@app.route('/loginto/<username>&<password>', methods=['POST', 'GET'])
def loginto(username, password):  # put application's code here
    global globaluid
    globaluid = getuid(username, password)
    return redirect(url_for('shouye'))


@app.route('/search_set', methods=['POST', 'GET'])
def search_set():  # put application's code here
    if request.method == 'POST':
        global stateurl
        global ispar
        global iswild
        if request.form['surl'] != '0':
            stateurl = request.form['surl']
        else:
            stateurl = 'empty'
        if request.form['par'] != '0':
            ispar = True
        else:
            ispar = False
        if request.form['wild'] != '0':
            iswild = True
        else:
            iswild = False
    return render_template("search_set.html", uid=globaluid)



@app.route('/searchto/<keyword>', methods=['POST', 'GET'])
def searchto(keyword):  # put application's code here
    if ispar:
        seartolog(globaluid, False, True, False, False, keyword, stateurl)
        addlabel(globaluid,keyword)
        return redirect(url_for('parse', keyword=keyword))
    elif iswild:
        seartolog(globaluid, False, False, True, False, keyword, stateurl)
        addlabel(globaluid, keyword)
        return redirect(url_for('wildse', keyword=keyword))
    elif stateurl != 'empty':
        seartolog(globaluid, False, False, False, True, keyword, stateurl)
        addlabel(globaluid, keyword)
        return redirect(url_for('instse', keyword=keyword))
    seartolog(globaluid, True, False, False, False, keyword, stateurl)
    addlabel(globaluid, keyword)
    return redirect(url_for('commonse', keyword=keyword))


@app.route('/commonse/<keyword>', methods=['POST', 'GET'])
def commonse(keyword):
    title = dict()
    text = dict()
    tourl = dict()
    commonsearch(keyword, title, text, tourl)
    title1 = dict()
    text1 = dict()
    tourl1 = dict()
    title2 = dict()
    text2 = dict()
    tourl2 = dict()
    likesearch(globaluid, title1, text1, tourl1, title2, text2, tourl2)
    resort(globaluid,title,text,tourl,title1,text1,tourl1,title2,text2,tourl2)
    return render_template("result.html", r0t=title[0], r0c=text[0], r0u=tourl[0],
                           r1t=title[1], r1c=text[1], r1u=tourl[1],
                           r2t=title[2], r2c=text[2], r2u=tourl[2],
                           r3t=title[3], r3c=text[3], r3u=tourl[3],
                           r4t=title[4], r4c=text[4], r4u=tourl[4],
                           r5t=title[5], r5c=text[5], r5u=tourl[5],
                           l1t=title1[0], l1c=text1[0], l1u=tourl1[0],
                           l2t=title2[0], l2c=text2[0], l2u=tourl2[0])


@app.route('/parse/<keyword>', methods=['POST', 'GET'])
def parse(keyword):
    title = dict()
    text = dict()
    tourl = dict()
    phrasesearch(keyword, title, text, tourl)
    title1 = dict()
    text1 = dict()
    tourl1 = dict()
    title2 = dict()
    text2 = dict()
    tourl2 = dict()
    likesearch(globaluid, title1, text1, tourl1, title2, text2, tourl2)
    resort(globaluid, title, text, tourl, title1, text1, tourl1, title2, text2, tourl2)
    return render_template("result.html", r0t=title[0], r0c=text[0], r0u=tourl[0],
                           r1t=title[1], r1c=text[1], r1u=tourl[1],
                           r2t=title[2], r2c=text[2], r2u=tourl[2],
                           r3t=title[3], r3c=text[3], r3u=tourl[3],
                           r4t=title[4], r4c=text[4], r4u=tourl[4],
                           r5t=title[5], r5c=text[5], r5u=tourl[5],
                           l1t = title1[0], l1c = text1[0], l1u = tourl1[0],
                           l2t = title2[0], l2c = text2[0], l2u = tourl2[0])


@app.route('/wildse/<keyword>', methods=['POST', 'GET'])
def wildse(keyword):
    title = dict()
    text = dict()
    tourl = dict()
    wildcardsearch(keyword, title, text, tourl)
    title1 = dict()
    text1 = dict()
    tourl1 = dict()
    title2 = dict()
    text2 = dict()
    tourl2 = dict()
    likesearch(globaluid, title1, text1, tourl1, title2, text2, tourl2)
    resort(globaluid, title, text, tourl, title1, text1, tourl1, title2, text2, tourl2)
    return render_template("result.html", r0t=title[0], r0c=text[0], r0u=tourl[0],
                           r1t=title[1], r1c=text[1], r1u=tourl[1],
                           r2t=title[2], r2c=text[2], r2u=tourl[2],
                           r3t=title[3], r3c=text[3], r3u=tourl[3],
                           r4t=title[4], r4c=text[4], r4u=tourl[4],
                           r5t=title[5], r5c=text[5], r5u=tourl[5],
                           l1t=title1[0], l1c=text1[0], l1u=tourl1[0],
                           l2t=title2[0], l2c=text2[0], l2u=tourl2[0])



@app.route('/instse/<keyword>', methods=['POST', 'GET'])
def instse(keyword):
    title = dict()
    text = dict()
    tourl = dict()
    instasearch(keyword, stateurl, title, text, tourl)
    title1 = dict()
    text1 = dict()
    tourl1 = dict()
    title2 = dict()
    text2 = dict()
    tourl2 = dict()
    likesearch(globaluid, title1, text1, tourl1, title2, text2, tourl2)
    resort(globaluid, title, text, tourl, title1, text1, tourl1, title2, text2, tourl2)
    return render_template("result.html", r0t=title[0], r0c=text[0], r0u=tourl[0],
                           r1t=title[1], r1c=text[1], r1u=tourl[1],
                           r2t=title[2], r2c=text[2], r2u=tourl[2],
                           r3t=title[3], r3c=text[3], r3u=tourl[3],
                           r4t=title[4], r4c=text[4], r4u=tourl[4],
                           r5t=title[5], r5c=text[5], r5u=tourl[5],
                           l1t=title1[0], l1c=text1[0], l1u=tourl1[0],
                           l2t=title2[0], l2c=text2[0], l2u=tourl2[0])



@app.route('/getcache', methods=['POST', 'GET'])
def getcache():  # put application's code here
    tourl = request.args.get('tourl')
    webcachedir = "WebCache/"
    cachepath = "not_found.html"
    # 打开url跳转字典
    id_url_dic = dict()
    with open("dataset/id_url_dic.pkl", "rb") as tf:
        id_url_dic = pickle.load(tf)
    toid = id_url_dic[tourl]
    tf.close()
    file_names = [f for f in os.listdir(webcachedir) if f.endswith('.html')]
    for file_name in file_names:
        result = file_name.split('.')[0]
        if int(result) == int(toid):
            cachepath = webcachedir + file_name
            return render_template(cachepath)
    return render_template(cachepath)


@app.route('/shouca', methods=['POST', 'GET'])
def shouca():  # put application's code here
    tourl = request.args.get('tourl')
    # 打开url跳转字典
    id_url_dic = dict()
    with open("dataset/id_url_dic.pkl", "rb") as tf:
        id_url_dic = pickle.load(tf)
    toid = id_url_dic[tourl]
    tf.close()
    store(globaluid, toid)
    return '', 204  # 返回一个空响应，表示成功但没有内容


if __name__ == '__main__':
    print("开始初始化搜索引擎！")
    print("开始爬取更新网页数据库！")
    #mainspider()
    print("网页数据更新完毕！")
    print("开始构建索引！")
    initindex()
    print("索引构建完毕！")
    print("开始进行链接分析，评估网页权重！")
    get_pagerank()
    print("评估网页权重完毕！")
    print("开始初始化其他所需数据集！")
    initsearlog()
    initlogin()
    print("初始化其他所需数据集完毕！")
    print("初始化完成，准备启动搜索引擎！")
    app.run()
