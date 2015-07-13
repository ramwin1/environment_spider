# !usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2,time
from bs4 import BeautifulSoup
import re
import MySQLdb

global updateDict
updateDict={}

class cityTemperature():
    def __init__(self,province, city,country,updateTime,result):
        self.province = province
        self.city=city
        self.country = country
        self.updateTime=updateTime
        self.result=result
    def save(self):
        db = MySQLdb.connect("localhost","root",'','bigdata',charset='utf8')
        cu = db.cursor()
        command = '''insert into weather values(%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (
                  'null',self.province,self.city,self.country,self.updateTime,self.result['od22'],self.result['od24'],
                   self.result['od25'],self.result['od26'],self.result['od27'])
        try:
            cu.execute(command)
            db.commit()
        except:
            print command,'失效'

def getdata(net):
    '''输入:一个网址;输出:网址下城市的数据文本'''
    temp=urllib2.urlopen(net,timeout=10).read()
    soup=BeautifulSoup(temp)
    temp2=soup.find(id='hour')
    temp3=temp2.script.text
    return temp3

def modifyForm(dataText):
    '''输入:城市对应的数据文本; 输出:城市,更新时间,过去24小时的数据列表'''
    temp1 = re.findall(r'{[\s\S]+}',dataText)[0]
    temp2 = eval(temp1)
    updateTime = temp2['od']['od0']
    city = temp2['od']['od1']
    result = temp2['od']['od2']
    return city, updateTime, result

def monitorTimeCalc(updateTime,interval):
    secTime = time.mktime(updateTime)
    secTime = secTime - interval * 3600
    st2 = time.localtime(secTime)
    return time.strftime('%Y-%m-%d %H:%M:%S',st2)

def getTotalCountry():
    file=open('totalCountryList','r')
    text=file.read()
    return eval(text)

def main():
    totalCountryList = getTotalCountry()
    a=time.time()
    for w in totalCountryList:
        province = w[0].encode('utf-8')
        city = w[1].encode('utf-8')
        country = w[2].encode('utf-8')
        net = w[3]
        print province,city,country
        try:
            dataText = getdata(net)       #获取网站文本数据
            country2, updateTime, result = modifyForm(dataText)             #转化成dict数据类型
        except:
            print province,city,country,'第一次抓取失败,时间在:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            for again in range(10):
                try:
                    time.sleep(60)
                    dataText = getdata(net)       #获取网站文本数据
                    country2, updateTime, result = modifyForm(dataText)             #转化成dict数据类型
                    province,city,country,'第%d次抓取成功,时间在:'%(again+2),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    break
                except:
                    province,city,country,'第%d次抓取失败,时间在:'%(again+2),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    country2 = ''
                break
        if country2:
            if country != country2:
                print city ,country2, '错误'
            updateTime = time.strptime(updateTime, '%Y%m%d%H%M%S')
            interval = 24
            for j in result[::-1]:
                monitorTime = monitorTimeCalc(updateTime,interval)
                id = province+city+country2
                if not id in updateDict.keys():
                    updateDict[id] = monitorTime
                    temp=cityTemperature(province,city,country2,monitorTime,j)
                    temp.save()
                else:
                    if updateDict[id]>=monitorTime:
                        print id,updateDict[id],'大于',monitorTime
                    else:
                        updateDict[id]=monitorTime
                        temp=cityTemperature(province,city,country2,monitorTime,j)
                        temp.save()
                interval = interval - 1
    end = time.time()
    print '总共用时%d秒'%(end-a)

if __name__ == '__main__':
    main()
    print 'done'
