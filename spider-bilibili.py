#! -*- coding:utf-8 -*-

"""
Author:Jasper.Z

2018.1.26
"""
import re
import requests
import logger
import codecs
from bs4 import BeautifulSoup
import jieba
import jieba.analyse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'}


def getAv():
    try:
        # av = input("请输入Av号:")
        av = "18618251"
        url = "https://www.bilibili.com/video/av" + str(av) + "/"
        getHTMLText(url, av)
    except:
        print("输入错误.")


def getHTMLText(url, av):
    u = requests.get(url=url, headers=headers)
    html = u.text
    cid = re.findall(r'cid=(.*?)&aid=', html)[0]
    getDanmu(cid, av)


def getDanmu(cid, av):
    dmurl = "https://comment.bilibili.com/" + str(cid) + ".xml"
    dmhtml = requests.get(url=dmurl, headers=headers).text
    soup = BeautifulSoup(dmhtml,from_encoding="utf-8")
    dmlist = soup.find_all('d')
    printDanmu(dmlist, av)


def printDanmu(dmlist, av):
    filename = "av" + str(av) + ".txt"
    print("Loading...\n")
    try:
        with codecs.open(filename, 'w', "utf-8") as t:
            for dm in dmlist:
                t.write(dm.string + '\n')
        analyse(filename, av)
    except Exception, e:
        logger.error('Failed to upload to ftp: ' + str(e))


def analyse(filename, av):
    content = open(filename, 'rb').read()
    tags = jieba.analyse.extract_tags(content, topK=60, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    with codecs.open(av+"-result.json", 'w', "utf-8") as t:
        for tag in tags:
            # json.dump("{\n  name: '%s',\n  value:%f\n}" % (tag[0], tag[1]), t)
            t.write("{\n  name: '%s',\n  value:%f\n},\n" % (tag[0], tag[1])+'\n')
            print("%s: %f" % (tag[0], tag[1]))


if __name__ == "__main__":
    getAv()
    print("Done!!!\n")


