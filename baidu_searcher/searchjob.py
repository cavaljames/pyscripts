#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''
Created on 2016年12月22日
@author: sugar
@see: the class that obtain your crawl-configs for search in www.baidu.com.
'''
class Searchjob(object):
    def __init__(self, jobname='jobname', jobpage=1, jobword='baidu', jobcsv='./csv', jobfilters=[]):
        if jobname:
            self.jobname = jobname
            self.jobpage = jobpage
            self.jobword = jobword
            self.jobcsv = jobcsv
            self.jobfilters = jobfilters
        else:
            print '加载任务%s失败！'%jobname
