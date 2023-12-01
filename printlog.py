import os
from datetime import datetime

searchlogdir = 'searchlog/'

def initsearlog():
    if not os.path.exists(searchlogdir):
        os.mkdir(searchlogdir)

def getfilesear(uid):
    file_names = [f for f in os.listdir(searchlogdir) if f.endswith('.log')]
    for file_name in file_names:
        result = file_name.split('.')[0]
        if int(result)==uid:
            return file_name
    doc_context = open(os.path.join(searchlogdir + str(uid) + '.log'), 'w', encoding='utf-8')
    doc_context.close()
    return (str(uid)+'.log')



def seartolog(uid,iscom,ispar,iswild,isinst,keyword,url):
    filename=getfilesear(uid)
    logt = open(os.path.join(searchlogdir + filename), 'a', encoding='utf-8')
    now = datetime.now()
    time = now.strftime("%Y-%m-%d | %H:%M:%S")
    if iscom:
        logt.write("[" + time + "] " + "Search_mode: Common_search " + " Keyword: " + keyword + "\n")
    elif ispar:
        logt.write("[" + time + "] " + "Search_mode: Phrase_search " + " Keyword: " + keyword + "\n")
    elif iswild:
        logt.write("[" + time + "] " + "Search_mode: Wildcard_search " + " Keyword: " + keyword + "\n")
    elif isinst:
        logt.write("[" + time + "] " + "Search_mode: Onsite_search " + " Keyword: " + keyword + " Url: " + url + "\n")
    logt.close()











if __name__ == '__main__':
    initsearlog()



