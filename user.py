import os
import random

userdir = 'user/'
storedir = 'user/store/'


def newuid():
    file_names = [f for f in os.listdir(userdir) if f.endswith('.txt')]
    return len(file_names) + 10000


"""
设计用户的label，类似于目前的大数据给每个用户做一个用户画像
理想情况下需要很多个标签，需要一个大数据支持，这里简化处理，人工设置10个标签
如下面user类的label，代表的就是用户的标签，标签的值代表这个用户在这个标签上的重要程度，例如标签为原神，那么数值就是它的原批浓度（这样应该比较通俗）
设计10个标签如下，因为考虑到爬的网页都是游戏界和科技数码界的资讯新闻，因此设计如下：
1：二次元
2：育碧
3：数码pc爱好者
4：米哈游
5：英雄联盟
6：暴雪
7：数码pe爱好者
8：单机游戏爱好者
9：联机对战游戏爱好者
10：cos美女帅哥爱好者
设计标签的含有关键词如下：
1：原神 崩坏 星穹铁道 碧蓝航线 明日方舟 重返1999
2：刺客信条 孤岛惊魂 全境封锁 看门狗 汤姆克兰西
3：显卡 英伟达 英特尔 AMD CPU 主板 内存条 三星 华硕 七彩虹 光刻机 芯片
4：原神 崩坏 星穹铁道 阮梅 那维莱特 八重神子 卡芙卡
5：lpl faker GENG WBG LNG LCK theshy 盲僧 剑魔
6：守望先锋 炉石传说 暴雪 使命召唤 魔兽世界 星际争霸
7：小米 魅族 红米 iphone apple 华为 麒麟 天玑 联发科 鸿蒙
8：steam epic 生化危机 RPG xbox
9：lol 英雄联盟 cf csgo cs2 彩虹六号 王者荣耀 和平精英 PUBG
10：我被美女包围了 cos 互动
"""

# 使用嵌套列表创建二维数组
label_array = [['原神', '崩坏', '星穹铁道', '碧蓝航线', '明日方舟', '重返1999'],
               ['刺客信条', '孤岛惊魂', '全境封锁', '看门狗', '汤姆克兰西'],
               ['显卡', '英伟达', '英特尔', 'AMD', 'CPU', '主板', '内存条', '三星', '华硕', '七彩虹', '光刻机', '芯片'],
               ['原神', '崩坏', '星穹铁道', '阮梅', '那维莱特', '八重神子', '卡芙卡'],
               ['lpl', 'faker', 'GENG', 'WBG', 'LNG', 'LCK', 'theshy', '盲僧', '剑魔'],
               ['守望先锋', '炉石传说', '暴雪', '使命召唤', '魔兽世界', '星际争霸'],
               ['小米', '魅族', '红米', 'iphone', 'apple', '华为', '麒麟', '天玑', '联发科', '鸿蒙'],
               ['steam', 'epic', '生化危机', 'RPG', 'xbox'],
               ['lol', '英雄联盟', 'cf', 'csgo', 'cs2', '彩虹六号', '王者荣耀', '和平精英', 'PUBG'],
               ['我被美女包围了', 'cos', '互动']]


def has_str(source, target):
    len_target = len(target)
    len_source = len(source)
    # 遍历字符串 source 中的字符
    for i in range(len_source - len_target + 1):
        # 如果当前位置开始的子字符串与目标相同
        if source[i:i + len_target] == target:
            return True  # 找到了
    return False  # 未找到


class userbody:
    uid = 0
    username = ''
    password = ''
    age = 0
    sex = 'm'
    label = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.uid = 10000 + 0

    def myinit(self, username, password):
        self.username = username
        self.password = password
        self.uid = newuid()

    def saveuser(self):
        doc_context = open(os.path.join(userdir + str(self.uid) + '.txt'), 'w', encoding='utf-8')
        doc_context.write(str(self.uid) + '\n')
        doc_context.write(self.username + '\n')
        doc_context.write(self.password + '\n')
        doc_context.write(str(self.age) + '\n')
        doc_context.write(self.sex + '\n')
        for i in range(0, 10):
            doc_context.write(str(self.label[i]) + '\n')
        doc_context.close()


def initlogin():
    if not os.path.exists(userdir):
        os.mkdir(userdir)
    if not os.path.exists(storedir):
        os.mkdir(storedir)


def getuid(username, password):
    file_names = [f for f in os.listdir(userdir) if f.endswith('.txt')]
    for file_name in file_names:
        file_path = os.path.join(userdir, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            usname = file.readline()
            usname = file.readline()
            if str(usname.strip()) == str(username):
                result = file_name.split('.')[0]
                return int(result)
    user = userbody()
    user.myinit(username, password)
    user.saveuser()
    return user.uid


def store(uid, toid):
    iswr = False
    file_names = [f for f in os.listdir(storedir) if f.endswith('.txt')]
    for file_name in file_names:
        result = file_name.split('.')[0]
        file_path = os.path.join(storedir, file_name)
        if int(result) == int(uid):
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(str(toid) + '\n')
                iswr = True
    if iswr == False:
        newuser = open(os.path.join(storedir + str(uid) + '.txt'), 'w', encoding='utf-8')
        newuser.write(str(toid) + '\n')


def tolabel(uid, ti):
    file_names = [f for f in os.listdir(userdir) if f.endswith('.txt')]
    for file_name in file_names:
        result = file_name.split('.')[0]
        file_path = os.path.join(userdir, file_name)
        if int(result) == int(uid):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines[5 + ti] = str(int(lines[5 + ti].strip()) + 1) + '\n'
                with open(file_path, 'w', encoding='utf-8') as tfile:
                    tfile.writelines(lines)


def addlabel(uid, keyword):
    file_names = [f for f in os.listdir(userdir) if f.endswith('.txt')]
    for file_name in file_names:
        result = file_name.split('.')[0]
        file_path = os.path.join(userdir, file_name)
        if int(result) == int(uid):
            with open(file_path, 'r', encoding='utf-8') as file:
                for i in range(0, 10):
                    row = label_array[i]
                    for j in range(0, len(row)):
                        if has_str(keyword, row[j]):
                            # 第i个标签含有关键词
                            tolabel(uid, i)


def getrandomlabel(uid):
    ptr1 = 0
    ptr2 = 0
    file_names = [f for f in os.listdir(userdir) if f.endswith('.txt')]
    for file_name in file_names:
        result = file_name.split('.')[0]
        file_path = os.path.join(userdir, file_name)
        if int(result) == int(uid):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i in range(0, 10):
                    if int(lines[5 + i].strip()) > int(lines[5 + ptr1].strip()):
                        ptr1 = i
                    if int(lines[5 + ptr2].strip()) < int(lines[5 + i].strip()) <= int(lines[5 + ptr1].strip()):
                        ptr2 = i
    str11 = random.choice(label_array[ptr1])
    str22 = random.choice(label_array[ptr2])
    mystr = [str11, str22]
    return mystr


if __name__ == '__main__':
    initlogin()
