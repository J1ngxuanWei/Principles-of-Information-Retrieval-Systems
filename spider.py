import re
import os
import requests
from bs4 import BeautifulSoup
from string import punctuation
from time import sleep
import random
import pickle

webcachedir = "templates/WebCache/"
cache_max_files = 50  # 最大缓存文件数
save_probability = 10  # 保存概率（百分之10）


def get_url_data(base_url, count, url_id_dic, to_use_url_list, used_url_set, url_jump_dic, id_url_dic, title_id_dic):
    print("@ 开始爬取网页：", base_url)
    # 返回爬取到的网页
    html = requests.get(base_url, timeout=50)
    # 解决爬取网页乱码的问题
    html.encoding = 'utf-8'
    # 保存cache
    # 获取文件夹下所有文件
    file_list = os.listdir(webcachedir)
    # 以一定概率保存文件
    if random.randint(1, 100) <= save_probability:
        # 如果文件数达到上限，随机删除一个文件
        if len(file_list) >= cache_max_files:
            file_to_delete = random.choice(file_list)
            os.remove(os.path.join(webcachedir, file_to_delete))
        file_name = f"{count}.html"
        file_path = os.path.join(webcachedir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html.text)
    # 从网页抓取数据。
    soup = BeautifulSoup(html.text, 'html.parser')
    tmp = soup.find('title')
    if tmp is None:
        to_use_url_list.remove(base_url)
        used_url_set.add(base_url)
        print('title为空 没有内容 无法爬取该页面//$^$//')
        return count
    else:
        html_title = tmp.text  # str类型
    # 去掉标题中的空格、标点符号
    html_title = html_title.replace(' ', '')
    html_title = re.sub(r"[{}、，。！？·【】）》；;《“”（-：— \t \n \r]+".format(punctuation), '', html_title)
    if html_title == '404NotFound':
        print('>>>404 Not Found, return')
        used_url_set.add(base_url)
        return count

    # 保存内容和标题
    # 声明文件对象
    doc_context = open(os.path.join('dataset/web_data/' + str(count) + '_' + html_title + '.txt'), 'w',
                       encoding='utf-8')

    # 这个总链接（我爬虫的这个页面）的标题写进去
    data = soup.select('head')
    for item in data:
        # 变成一行
        text = re.sub('[\r \n\t]', '', item.get_text())
        if text is None or text == '':
            continue
        title_id_dic[count] = text

    # 这个链接的文字写进去
    data = soup.select('#Content')
    for item in data:
        text = re.sub('[\r \n\t]', '', item.get_text())
        # 替换\u3000字符为空格
        text = text.replace('\u3000', '')
        text.strip()
        if text is None or text == '':
            continue
        doc_context.write(text)
    doc_context.close()

    # 在html中，a表示超链接，例如<a href="https://www.ali213.net/news/html/2023-11/798423.html" title="互动电影游戏《琉璃烟火》上架Steam平台 明年Q1发售" target="_blank">互动电影游戏《琉璃烟火》上架Steam平台 明年Q1发售</a>
    # 找到所有有超链接的地方，返回的可以看作列表，能用[i]索引
    data = soup.select('a')

    # 遍历这些超链接
    # 字典，每个url对应一个列表，列表中记录这个url可以跳转的其他url，字符串类型['url1','url2']
    url_jump_dic[count] = []
    for item in data:
        # 获取文本
        text = re.sub("[\r \n\t]", '', item.get_text())
        # 如果text中没有内容,continue
        if text == None or text == '':
            continue
        # 找item中的href,链接， 它是https://www.ali213.net/news/html形式的
        url = item.get('href')

        if url is None or url == '' or re.search('java|void', url) != None:
            continue

        if url not in used_url_set and 'https://www.ali213.net/news/html' in url and url not in to_use_url_list:
            to_use_url_list.append(url)
            # 添加到url跳转列表
            url_jump_dic[count].append(url)

    # 将该 url 加入 url_id_dic
    url_id_dic[count] = base_url
    id_url_dic[base_url] = count
    to_use_url_list.remove(base_url)
    used_url_set.add(base_url)
    count = count + 1
    print("@ 爬取完毕：", base_url)
    return count


def spider():
    # 已经爬取过的网页，用集合
    used_url_set = set()
    # 将要爬取的网页，用列表保存，因为集合无序，无法遍历
    to_use_url_list = [
        'https://www.ali213.net/news/game/',
        'https://www.ali213.net/news/game/index_2.html',
        'https://www.ali213.net/news/game/index_3.html',
        'https://www.ali213.net/news/game/index_4.html',
        'https://www.ali213.net/news/game/index_5.html',
        'https://www.ali213.net/news/comic/',
        'https://www.ali213.net/news/comic/index_2.html',
        'https://www.ali213.net/news/comic/index_3.html',
        'https://www.ali213.net/news/comic/index_4.html',
        'https://www.ali213.net/news/comic/index_5.html',
        'https://www.ali213.net/news/movie/',
        'https://www.ali213.net/news/movie/index_2.html',
        'https://www.ali213.net/news/movie/index_3.html',
        'https://www.ali213.net/news/movie/index_4.html',
        'https://www.ali213.net/news/movie/index_5.html',
        'https://www.ali213.net/news/tech/',
        'https://www.ali213.net/news/tech/index_2.html',
        'https://www.ali213.net/news/tech/index_3.html',
        'https://www.ali213.net/news/tech/index_4.html',
        'https://www.ali213.net/news/tech/index_5.html',
        'https://www.ali213.net/news/esports/',
        'https://www.ali213.net/news/esports/index_2.html',
        'https://www.ali213.net/news/esports/index_3.html',
        'https://www.ali213.net/news/esports/index_4.html',
        'https://www.ali213.net/news/esports/index_5.html',
        'https://www.ali213.net/news/amuse/',
        'https://www.ali213.net/news/amuse/index_2.html',
        'https://www.ali213.net/news/amuse/index_3.html',
        'https://www.ali213.net/news/amuse/index_4.html',
        'https://www.ali213.net/news/amuse/index_5.html'
    ]
    # 字典，记录1号对应哪个url，2号对应哪个url
    url_id_dic = dict()
    # 字典，记录url对应的id
    id_url_dic = dict()
    # 字典 记录每个url页面可以跳转到的url们 用它们对应的数字id标识
    url_jump_dic = dict()
    # 字典 记录1号对应哪个标题，2号对应哪个标题
    title_id_dic = dict()
    mycount = 0
    for i in range(0, 5000):
        if len(to_use_url_list) != 0 and mycount < 4900:
            print("@ 爬取网页个数：", i, "  爬取成功个数：", mycount)
            tmp = to_use_url_list[0]
            mycount = get_url_data(tmp, mycount, url_id_dic, to_use_url_list, used_url_set, url_jump_dic, id_url_dic,
                                   title_id_dic)
            # 休息一下
            sleep(random.randint(0, 1))

    # 保存字典文件url_id_dic
    with open("dataset/url_id_dic.pkl", "wb") as tf:
        pickle.dump(url_id_dic, tf)
    tf.close()
    print('save url_id_dic end')
    # 保存字典文件id_url_dic
    with open("dataset/id_url_dic.pkl", "wb") as tf1:
        pickle.dump(id_url_dic, tf1)
    tf1.close()
    print('save id_url_dic end')
    # 保存url跳转到的url记录
    with open("dataset/url_jump_dic.pkl", "wb") as tf2:
        pickle.dump(url_jump_dic, tf2)
    tf2.close()
    print('save url_jump_dic end')
    # 保存id到title记录
    with open("dataset/title_id_dic.pkl", "wb") as tf3:
        pickle.dump(title_id_dic, tf3)
    tf3.close()


def initcache():
    webcachedir = "templates/WebCache//"
    if not os.path.exists(webcachedir):
        os.mkdir(webcachedir)

def mainspider():
    initcache()
    spider()

if __name__ == '__main__':
    initcache()
    spider()

