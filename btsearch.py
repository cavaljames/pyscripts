#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2,urllib,sys,codecs
from bs4 import BeautifulSoup
'''
Created on 2016年11月9日
@author: sugar
@see: a simple searcher to get downlinks from http://btdigg.pw , you can search whatever you like :-)
'''

def do_post(url, data): 
    post_headers = {
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding':'deflate',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'Cache-Control':'max-age=0',
               'Connection':'keep-alive',
               'Content-Type':'application/x-www-form-urlencoded',
               'Host':'btdigg.pw',
               'Origin':'http://btdigg.pw',
               'Referer':'http://btdigg.pw/search/c2dhMDQ5/1/0/0.html',
               'Upgrade-Insecure-Requests':'1',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    } 
    req = urllib2.Request(url,headers=post_headers)  
    data = urllib.urlencode(data)  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    try:
        d = opener.open(req, data ,timeout=5).read()
    except:
        return None
    return d  

def do_get(url): 
    get_headers = {
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding':'deflate, sdch',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'Cache-Control':'max-age=0',
               'Connection':'keep-alive',
               'Content-Type':'application/x-www-form-urlencoded',
               'Host':'btdigg.pw',
               'Upgrade-Insecure-Requests':'1',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    } 
    req = urllib2.Request(url,headers=get_headers)  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    try:
        d = opener.open(req ,timeout=5).read()
    except:
        return None
    return d
  

if __name__ == '__main__':
    code_path = './codes'
    if len(sys.argv) > 1:
        code_path = sys.argv[1]
    code_file = open(code_path)
    codes = code_file.readlines()
    fname = codes[0].replace('\r','').replace('\n','').decode('utf8').encode('gbk')
    for code in codes[1:]:
        code = code.replace('\r','').replace('\n','')
        posturl = 'http://btdigg.pw/'
        data = {'keyword':code}
        f_page = do_post(posturl, data)
        if f_page:
            f_soup = BeautifulSoup(f_page,'html.parser')
            f_list = f_soup.select('div.list-box div.list dl')
            for dl in f_list:
                a_href = dl.select_one('dt > a')
                attrs = dl.select('dd.attr span')
                flist = dl.select_one('dd.flist > p span.filename')
                filename = flist.get_text()
                time = attrs[0].select_one('b').get_text()
                size = attrs[1].select_one('b').get_text()
                fils = attrs[2].select_one('b').get_text()
                hots = attrs[4].select_one('b').get_text()
                 
                f_href = a_href['href']
                s_page = do_get(f_href)
                if s_page:
                    s_soup = BeautifulSoup(s_page,'html.parser')
                    thunder_href = s_soup.select('div.torrent dl.detail dd.down > span')[1].select_one('a')['href']
                    file_write = codecs.open('./%s.csv'%fname,'a','utf8')
                    file_write.write('\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n'%(filename,time,size,fils,hots,code,thunder_href))
                    file_write.close()
                    print thunder_href
                    
    data = open('./%s.csv'%fname).read()
    if not (data[:3] == codecs.BOM_UTF8):
        data = '%s%s'%(codecs.BOM_UTF8,data)
    result = codecs.open('./%s.csv'%fname,'w','utf8')
    result.write(data.decode('utf8'))
    result.close()
    
    
    
    
    
