#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wangx'
import urllib2
from bs4 import BeautifulSoup
def main():
    '''获取城市，格式为字典，key为城市名，value为网址'''
    net='http://www.weather.com.cn/textFC/hb.shtml'
    temp=urllib2.urlopen(net).read()
    temp1=BeautifulSoup(temp)
    temp2=temp1.find(class_ = 'lqcontentBoxheader')
    temp3 = temp2.find_all('a')
    cityList={}
    for i in temp3:
        t = i.text
        link = 'http://www.weather.com.cn'+i.get('href')
        cityList[t]= link
    return cityList
