'''
尽可能的考虑使用打开一个excel，在后面添加相应的结果？
搜索的关键词，直接读取相关的内容，一个公司检索下去，应该会有很多结果，
只考虑第一个就好了，所以不要那么多结果，没意义，也顾不过来，
搜索次数1次就可以了，这个是做什么用的
延时最好在5s到10s，随机延时。

获取数据的
基本与原来方案一致，增加一个文本文档存储备注信息产品和经营范围信息，便于分析
需要购买1天会员，进行查询
另外，进入到详细页面，获取相应的数据（上市和不上市有什么区别？）

'''


#-*- coding-8 -*-

import requests
import lxml
import sys
from bs4 import BeautifulSoup
import xlwt
import time
import urllib
 
def Craw(url,key_word):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
#    if x == 0:
#        re = 'http://www.qichacha.com/search?key='+key_word
#    else:
#        re = 'https://www.qichacha.com/search?key={}#p:{}&'.format(key_word,x-1)
    re = r'https://www.qichacha.com/search?key='+key_word
    headers = {
            'Host':'www.qichacha.com',
            'Connection': 'keep-alive',
            'Accept':r'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer': re,
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cookie':r'519542629-1560237892-https%253A%252F%252Fwww.so.com%252F%7C1571293316',  #设置自己浏览器的cookie  chrome://settings/cookies
            #Hm_lvt_3456bee468c83cc63fb5147f119f1075
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
        com_all_info = soup.find_all(class_='m_srchList')[0].tbody
        com_all_info_array = com_all_info.select('tr')
        gongsi = com_all_info_array[0].select('td')[2].select('.ma_h1')[0].text    #获取公司名
        tags= com_all_info_array[0].select('td')[2].select('.search-tags')[0].text     #获取公司标签
        faren = com_all_info_array[0].select('td')[2].select('p')[0].a.text    #获取法人名
        zhuceziben = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[0].text.strip('注册资本：')    #获取注册资本
        riqi = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[1].text.strip('成立日期：')    #获取公司注册时间
        email = com_all_info_array[0].select('td')[2].select('p')[1].text.split('\n')[1].strip().strip('邮箱：')    #获取法人Email
        phone = com_all_info_array[0].select('td')[2].select('p')[1].select('.m-l')[0].text.strip('电话：')    #获取法人手机号
        addr = com_all_info_array[0].select('td')[2].select('p')[2].text.strip().strip('地址：')    #获取公司地址
        state = com_all_info_array[0].select('td')[3].select('.nstatus.text-success-lt.m-l-xs')[0].text.strip()  #获取公司状态
        
#        wangzhi = com_all_info_array[0].select('td')[2].a #wangzhi
        
        result = [gongsi,tags,faren,zhuceziben,riqi,email,phone,addr,state]                                 

    except Exception:
        print('好像被拒绝访问了呢...请稍后再试叭...'+key_word)
    
     
    return(result)

 



#    workbook = xlwt.Workbook()  select('href')
#    #创建sheet对象，新建sheet
#    sheet1 = workbook.add_sheet('企查查数据', cell_overwrite_ok=True)
#    #---设置excel样式---
#    #初始化样式
#    style = xlwt.XFStyle()
#    #创建字体样式
#    font = xlwt.Font()
#    font.name = '仿宋'
##    font.bold = True #加粗
#    #设置字体
#    style.font = font
#    #使用样式写入数据
#    print('正在存储数据，请勿打开excel')
#    #向sheet中写入数据
#    name_list = ['公司名字','公司标签','法定法人','注册资本','成立日期','法人邮箱','法人电话','公司地址','公司状态']
#    for cc in range(0,len(name_list)):
#        sheet1.write(0,cc,name_list[cc],style)
#    for i in range(0,len(g_name_list)):
#        print(g_name_list[i])
#        sheet1.write(i+1,0,g_name_list[i],style)#公司名字
#        sheet1.write(i+1,1,g_tag_list[i],style)#公司标签
#        sheet1.write(i+1,2,r_name_list[i],style)#法定法人
#        sheet1.write(i+1,3,g_money_list[i],style)#注册资本
#        sheet1.write(i+1,4,g_date_list[i],style)#成立日期
#        sheet1.write(i+1,5,r_email_list[i],style)#法人邮箱
#        sheet1.write(i+1,6,r_phone_list[i],style)#法人电话
#        sheet1.write(i+1,7,g_addr_list[i],style)#公司地址
#        sheet1.write(i+1,8,g_state_list[i],style)#公司状态
#    #保存excel文件，有同名的直接覆盖
#    workbook.save(r"D:\wyy-qcc-"+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +".xls")
#    print('保存完毕~')
#
