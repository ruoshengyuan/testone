# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:26:12 2019
gongsiwangzhan 
@author: h
"""

#-*- coding-8 -*-

import requests
import lxml
import sys
from bs4 import BeautifulSoup
import xlwt
import time
import urllib
from openpyxl import Workbook
 
def Craw(url):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    re = url
    headers = {
            'Host':'www.cecxtal.com',
            'Connection': 'keep-alive',
            'Accept':r'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer': re,
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cookie':r'JSESSIONID',  #设置自己浏览器的cookie  chrome://settings/cookies
            }
 
    try:
        response = requests.get(url,headers = headers)
        if response.status_code != 200:
            response.encoding = 'utf-8'
            print(response.status_code)
            print('ERROR')    
        soup = BeautifulSoup(response.text,'lxml')
    except Exception:
        print('请求都不让，这企查查是想逆天吗？？？')
    result=[]
    try:
        xinghao = str(soup.select('table')[0].select('td')[3].text)
        xiazai = str((soup.select('table')[0].select('tr')[1].select('td')[2].select('a')[0].attrs)['href'])
#        tags= com_all_info_array[0].select('td')[2].select('.search-tags')[0].text     #获取公司标签
#        faren = com_all_info_array[0].select('td')[2].select('p')[0].a.text    #获取法人名
#        zhuceziben = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[0].text.strip('注册资本：')    #获取注册资本
#        riqi = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[1].text.strip('成立日期：')    #获取公司注册时间
#        email = com_all_info_array[0].select('td')[2].select('p')[1].text.split('\n')[1].strip().strip('邮箱：')    #获取法人Email
#        phone = com_all_info_array[0].select('td')[2].select('p')[1].select('.m-l')[0].text.strip('电话：')    #获取法人手机号
#        addr = com_all_info_array[0].select('td')[2].select('p')[2].text.strip().strip('地址：')    #获取公司地址
#        state = com_all_info_array[0].select('td')[3].select('.nstatus.text-success-lt.m-l-xs')[0].text.strip()  #获取公司状态
#        
#        wangzhi = com_all_info_array[0].select('td')[2].a #wangzhi
        
        result = [xinghao,xiazai]                                 
    except Exception:
        print('未获取数据...'+url)        
    return(result)

if __name__=="__main__":

    wb = Workbook()
    ws = wb.active
    ws.append(('xinghao','xiazaidizhi','url'))
    for i in range(150,400):
        url=r'http://www.cecxtal.com/queryItemById.html?itemId={}'.format(i)
        shuchu=Craw(url)
        print(shuchu)
        if shuchu :
            shuchu.append(url)
            ws.append(shuchu)
        sleep_time = 3   #检索间隔时间
        time.sleep(sleep_time)
        
    wb.save('shishikan.xlsx')
    
    
    
    