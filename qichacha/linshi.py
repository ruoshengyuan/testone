# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:08:53 2019

@author: h
"""
import requests
import lxml
import sys
from bs4 import BeautifulSoup
import xlwt
import time
import urllib
from ceshiqichacha import Craw,Craw_inside
from openpyxl import load_workbook
from openpyxl import Workbook

#打开表格，获取全部数据为rows列表，获取查询关键字列的数据，为data
wb = load_workbook('d:\\testone\\qichacha\\abc.xlsx')
ws=wb.active
rows=[]

for row in ws.iter_rows():
            rows.append(row)


wb2 = Workbook()
ws2 = wb2.active
ws2.append(['公司抬头','姓名','手机号','邮箱','座机','QQ','微信','职位','部门','行业类型','客户类型','名单来源',
'回访人','地址','是否注册','注册时间','注册账号','绑定手机','绑定邮箱','客服代表','经营范围',
'公司','标签','法人','注册资本','成立日期','邮件','电话','地址','公司状态',
'网站','实缴资本','企业类型','所属行业','参保人数','人员规模','经营范围','简介','风险'
])
   
for row in rows[50:100] :

    key_word = str(row[0].value)
    print(key_word)
    if  key_word:
        key_word2 = urllib.parse.quote(key_word)    
        url = r'https://www.qichacha.com/search?key='+key_word2
        result = Craw(url,key_word2)
        new_row =[]
        for m in range(len(row)):
            new_row.append(row[m].value)
        if  result :
            new_row.extend(result)
            ws2.append(new_row)
            
        else :
            print('无采集到任何数据，请检查'+key_word)
        

wb2.save('111.xlsx')
#akk =[]
#for row in rows[:2] :
#    for m in range(len(row)) :
#        akk.append(row[m].value)
#    print(akk)    
#print(mingcheng)
#    wb.save("e:\\sample.xlsx")
#data = []   
#for i in range(0,len(rows)) :
#    data.append(rows[i][0].value)
#for m in range(len(rows)):
#    for n in range(len(m)):
#        rows[m]
#print(rows[1][:].value)   #所有行
#print (rows[0]) #获取第一行
#print (rows[0][0]) #获取第一行第一列的单元格对象
#print (rows[0][0].value) #获取第一行第一列的单元格对象的值
# 
#print (rows[len(rows)-1]) #获取最后行 print rows[-1]
#print (rows[len(rows)-1][len(rows[0])-1]) #获取第后一行和最后一列的单元格对象
#print (rows[len(rows)-1][len(rows[0])-1].value) #获取第后一行和最后一列的单元格对象的值