#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wangx'
import urllib2
from bs4 import BeautifulSoup
import getProvinceList

provinceList = getProvinceList.main()

global coun
coun=[]
def get(net):
    result = []
    try:
        html = urllib2.urlopen(net,timeout=10).read()
    except:
        html=''
        while not html:
            html = urllib2.urlopen(net,timeout=10).read()
        
    soup = BeautifulSoup(html)
    temp = soup.body.find(class_='lqcontentBoxH').find(class_='contentboxTab').find(class_='contentboxTab1').find(class_='conMidtab').find_all(class_='conMidtab3')
    print len(temp)
    for i in temp:
        city = i.td.text
        j = i.find_all('tr')
        for k in j:
            result.append((city,k.a.text,k.a.get('href')))
            coun.append(k.a.text)
    return result

def gettotal():
    totalCountryList = []
    for i in provinceList.keys():
        net = provinceList[i]
        temp = get(net)
        for j in temp:
            row = (i,)+j
            totalCountryList.append(row)
    file = open('totalCountryList','w')
    text=''
    text = str(totalCountryList)
    file.write(text)
    file.close()

def test():
    test=[]
    for i in provinces:
        if i in test:
            print i

        test.append(i)

