#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''
Created on 2016年12月22日
@author: sugar
@see: a crawler for searching in www.baidu.com.
'''
import urllib2,os,urllib
from bs4 import BeautifulSoup
from searchjob import Searchjob

def filter_checked(title,jobfilters):
    checked = True
    for ft in jobfilters:
        if (title in ft) or (ft in title):
            checked = False
            break
    return checked
    
def do_crawl(url):
    req_headers = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2243.0 Safari/537.36'
               }
    req = urllib2.Request(url,headers=req_headers)
    page_str = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page_str,'html.parser')
    content = soup.select('#content_left h3.t a')
    while not len(content)>0:
        page_str = urllib2.urlopen(url)
        soup = BeautifulSoup(page_str,'html.parser')
        content = soup.select('#content_left h3.t a')
    return content

if __name__ == '__main__':
    #===========================================================================
    # 配置参数
    param_fname = './param'
    # param_fname = sys.argv[1]
    if not os.path.exists(param_fname):
        param_fname += '.xml'
    param_f = open(param_fname)
    param_str = param_f.read()
    param_soup = BeautifulSoup(param_str,'html.parser')
    search_job_list = []
    for p in param_soup.select('param-list param'):
        job_name = p.get('name')
        job_word = p.get('word')
        job_csv = p.get('csv')
        job_page = int(p.get('page'))
        job_filters = []
        for jf in p.select('jobfilter-list filter'):
            job_filter = jf.get_text()
            job_filters.append(job_filter)
          
        s_job = Searchjob(jobname=job_name,
                          jobword=job_word,
                          jobpage=job_page,
                          jobcsv=job_csv,
                          jobfilters=job_filters)
        search_job_list.append(s_job)
    #===========================================================================
       
    #===========================================================================
    # 开始任务
    for s_job in search_job_list:
        for page_num in range(0,s_job.jobpage):
            j_name_str = s_job.jobname.encode('utf8')
            j_csv_str = s_job.jobcsv.encode('utf8')
            file_str = ''
            url = 'https://www.baidu.com/s?wd=%s&pn=%s0'%(urllib.quote(s_job.jobword.encode('utf8'),'gbk'),page_num)
            content = do_crawl(url)
            for anc in content:
                title = anc.get_text()
                href = anc.get('href')
                if filter_checked(title,s_job.jobfilters):
                    j_title_str = title.encode('utf8')
                    j_href = href.encode('utf8')
                    try:
                        req = urllib2.Request(j_href)
                        res = urllib2.urlopen(req)
                        j_href_str = res.url
                        file_str += '\"%s\",\"%s\",\"%s\"\n'%(j_name_str,j_title_str,j_href_str)
                        print j_title_str
                    except Exception,ex:
                        print 'error with %s:%s'%(j_name_str,j_href)
                        pass
            f2w = open(j_csv_str,'a')
            f2w.write(file_str)
            f2w.close()
    #===========================================================================
    