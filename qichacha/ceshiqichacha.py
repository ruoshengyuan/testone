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
import re
 
def Craw(url,key_word):
    sleep_time = 10   #检索间隔时间
    time.sleep(sleep_time)
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    re = url
    headers = {
            'Host':'www.qichacha.com',
            'Connection': 'keep-alive',
            'Accept':r'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer': re,
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cookie':r'acw_tc=3cdfd94715712944734741510edf5221430510901350e464f5752d1fce; QCCSESSID=kjlo9oiui1r8kc80gamujlfhl0; zg_did=%7B%22did%22%3A%20%2216dd8729700877-0e764955705a46-43450521-1fa400-16dd8729701242%22%7D; _uab_collina=157129445153216988852851; UM_distinctid=16dd8729829179-0f61ae064054c-43450521-1fa400-16dd872982a541; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1571294452; hasShow=1; CNZZDATA1254842228=519542629-1560237892-https%253A%252F%252Fwww.so.com%252F%7C1571703717; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1571704705; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201571703708193%2C%22updated%22%3A%201571704808210%2C%22info%22%3A%201571294451475%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22d2ccb117cf68f3409ccdd36485180ac1%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D',  #设置自己浏览器的cookie  chrome://settings/cookies
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
    
    gongsi=''
    tags=''
    faren=''
    zhuceziben=''
    riqi=''
    email=''
    phone=''
    addr=''
    state=''
    wangzhi=''
    new_array=[]



    try:
        com_all_info = soup.find_all(class_='m_srchList')[0].tbody
        com_all_info_array = com_all_info.select('tr')
        gongsi = com_all_info_array[0].select('td')[2].select('.ma_h1')[0].text
    except Exception:
        gongsi='估计限制登录了'
        print('    打不开了，估计限制登录了。。。')        
    try:
        tags= com_all_info_array[0].select('td')[2].select('.search-tags')[0].text     #获取公司标签
    except Exception:
        tags=''
    try:
        faren = com_all_info_array[0].select('td')[2].select('p')[0].a.text    #获取法人名
    except Exception:
        faren=''
    try:
        zhuceziben = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[0].text.strip('注册资本：')
    except Exception:
        zhuceziben=''
    try:
        riqi = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[1].text.strip('成立日期：') 
    except Exception:
        riqi=''
    try:
        email = com_all_info_array[0].select('td')[2].select('p')[1].text.split('\n')[1].strip().strip('邮箱：').replace(' ', '').replace('\n', '')    
    except Exception:
        email=''
    try:
        phone = com_all_info_array[0].select('td')[2].select('p')[1].select('.m-l')[0].text.strip().strip('\n').strip('电话：').replace(' ', '').replace('\n', '')
    except Exception:
        phone=''
    try:
        addr = com_all_info_array[0].select('td')[2].select('p')[2].text.strip().strip('地址：')    #获取公司地址
    except Exception:
        addr=''
    try:
        state = com_all_info_array[0].select('td')[3].select('.nstatus.text-success-lt.m-l-xs')[0].text.strip()  #获取公司状态
    except Exception:
        state=''
        
#    gongsi = com_all_info_array[0].select('td')[2].select('.ma_h1')[0].text    #获取公司名
#    tags= com_all_info_array[0].select('td')[2].select('.search-tags')[0].text     #获取公司标签
#    faren = com_all_info_array[0].select('td')[2].select('p')[0].a.text    #获取法人名
#    zhuceziben = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[0].text.strip('注册资本：')    #获取注册资本
#    riqi = com_all_info_array[0].select('td')[2].select('p')[0].select('span')[1].text.strip('成立日期：')    #获取公司注册时间
#    email = com_all_info_array[0].select('td')[2].select('p')[1].text.split('\n')[1].strip().strip('邮箱：')    #获取法人Email
#    phone = com_all_info_array[0].select('td')[2].select('p')[1].select('.m-l')[0].text.strip().strip('\n').strip('电话：')    #获取法人手机号
#    addr = com_all_info_array[0].select('td')[2].select('p')[2].text.strip().strip('地址：')    #获取公司地址
#    state = com_all_info_array[0].select('td')[3].select('.nstatus.text-success-lt.m-l-xs')[0].text.strip()  #获取公司状态
     
    try :  
        wangzhi = 'https://www.qichacha.com'+str((com_all_info_array[0].select('td')[2].select('.ma_h1')[0].attrs)['href'])+'#base'#wangzhi
        new_array = Craw_inside(wangzhi)
    except Exception:
        print('    不能获取跳转链接地址')
        new_array =[]
        
    result = [gongsi,tags,faren,zhuceziben,riqi,email,phone,addr,state]  
    result.extend(new_array)     
    return(result)

def Craw_inside(url):
    sleep_time = 10   #检索间隔时间
    time.sleep(sleep_time)
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' #详情页
    headers = {
            'Host':'www.qichacha.com',
            'Connection': 'keep-alive',
            'Accept':r'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer': url,
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cookie':r'acw_tc=3cdfd94715712944734741510edf5221430510901350e464f5752d1fce; QCCSESSID=kjlo9oiui1r8kc80gamujlfhl0; zg_did=%7B%22did%22%3A%20%2216dd8729700877-0e764955705a46-43450521-1fa400-16dd8729701242%22%7D; _uab_collina=157129445153216988852851; UM_distinctid=16dd8729829179-0f61ae064054c-43450521-1fa400-16dd872982a541; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1571294452; hasShow=1; CNZZDATA1254842228=519542629-1560237892-https%253A%252F%252Fwww.so.com%252F%7C1571703717; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1571704705; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201571703708193%2C%22updated%22%3A%201571704808210%2C%22info%22%3A%201571294451475%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22d2ccb117cf68f3409ccdd36485180ac1%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D',  #设置自己浏览器的cookie  chrome://settings/cookies
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
        print('    详情页：请求都不让，这企查查是想逆天吗？？？')
    result=[]
    
    mingcheng = ''
    
    dianhua = ''
    gengduo = ''
    youxiang = ''
    wangzhan='' #you

    faren = ''
    zhuce = ''
    shijiao=''  #you
    zhuangtai = ''
    shijian = '' #you
    leixing='' #you
    hangye=''
    jiguan=''
    quyu=''    
    canbao='' #you
    renshu=''#you
    fanwei='' #you
    
    jianjie=''    #you
    fengxian='' #you
       
    
         #每一个都分开来try，避免漏采数据，重点是详情页页面信息，公司名称，电话，更多电话，邮箱，网站，地址，简介，
#        法定代表人，注册资本，实缴资本，经营状态，成立日期，企业类型，所属行业，登记机关，所属地区，参保人数，人员规模，经营范围
         

        
    try:    
        b=str(soup.find_all(id='Cominfo'))        
        faren=re.findall('<h2 class="seo font-20">(.*?)</h2>',b)[0].strip(' ')
    except Exception:
        faren =''

    try:        
        zhuce=re.findall('注册资本 </td> <td width="30%"> (.*?) </td>',b)[0].strip(' ')
    except Exception:
        zhuce =''

    try:        
        shijiao=re.findall('实缴资本 </td> <td width="30%"> (.*?) </td>',b)[0].strip(' ')
    except Exception:
        shijiao =''
        
    try:        
        zhuangtai=re.findall('经营状态</td> <td class="">\n(.*?)</td>',b)[0].strip()
    except Exception:
        zhuangtai =''

    try:        
        shijian=re.findall('成立日期</td> <td class="">\n(.*)',b)[0].strip()
    except Exception:
        shijian =''
        
    try:        
        leixing=re.findall('</td> </tr> <tr> <td class="tb">企业类型</td> <td class="">\n(.*)',b)[0].strip()  
    except Exception:
        leixing =''

    try:        
        hangye=re.findall('<td class="tb">所属行业</td> <td class="">\n(.*)',b)[0].strip()
    except Exception:
        hangye =''
        
    try:        
        jiguan=re.findall('登记机关</td> <td class="">\n(.*)',b)[0].strip()
    except Exception:
        jiguan =''

    try:        
        quyu=re.findall('<td class="tb">所属地区</td> <td class="" style="max-width:301px;">\n(.*)',b)[0].strip()
    except Exception:
        quyu =''

    try:        
        canbao=re.findall('参保人数\n.*\n(.*)',b)[0].strip(' ')
    except Exception:
        canbao =''
        
    try:        
        renshu=re.findall('人员规模\n.*\n(.*)',b)[0].strip(' ')
    except Exception:
        renshu =''

    try:        
        fanwei=re.findall('经营范围</td> <td class="" colspan="3">\n(.*)</td>',b)[0].strip(' ')
    except Exception:
        fanwei =''

        
#        zhuce=re.findall('注册资本 </td> <td width="30%"> (.*?) </td>',b)[0].strip(' ')
#        shijiao=re.findall('实缴资本 </td> <td width="30%"> (.*?) </td>',b)[0].strip(' ')
#        zhuangtai=re.findall('经营状态</td> <td class="">\n(.*?)</td>',b)[0].strip()
#        shijian=re.findall('成立日期</td> <td class="">\n(.*)',b)[0].strip()
#        leixing=re.findall('</td> </tr> <tr> <td class="tb">企业类型</td> <td class="">\n(.*)',b)[0].strip()      
#        hangye=re.findall('<td class="tb">所属行业</td> <td class="">\n(.*)',b)[0].strip()
#        jiguan=re.findall('登记机关</td> <td class="">\n(.*)',b)[0].strip()
#        quyu=re.findall('<td class="tb">所属地区</td> <td class="" style="max-width:301px;">\n(.*)',b)[0].strip()
#        canbao=re.findall('参保人数\n.*\n(.*)',b)[0].strip(' ')
#        renshu=re.findall('人员规模\n.*\n(.*)',b)[0].strip(' ')
#        fanwei=re.findall('经营范围</td> <td class="" colspan="3">\n(.*)</td>',b)[0].strip(' ')




    try:    #每一个都分开来try，避免漏采数据
        n=str(soup.find_all(class_='dcontent')[0])  #获取网址信息
        wangzhan=re.findall('进入官网">(.*?)</a>',n)[0].strip()
    except Exception:
        wangzhan =''
        
    try:    #每一个都分开来try，避免漏采数据
        n=str(soup.find_all(class_='dcontent')[0])  #获取网址信息
        youxiang = re.findall('title="发送邮件">(.*?)</a>',n)[0].strip().replace(' ', '').replace('\n', '')
    except Exception:
        youxiang =''
        
    try:    #每一个都分开来try，避免漏采数据        
        jianjie=soup.find_all(class_='m-t-sm m-b-sm')[0].text
    except Exception:
        jianjie =''
        
    try:    #每一个都分开来try，避免漏采数据        
        fengxian=soup.find_all(class_='risk-panel b-a')[0].text.replace(' ', '').replace('\n', '')
    except Exception:
        fengxian =''
        
    try:    #每一个都分开来try，避免漏采数据        
        mingcheng = soup.find_all(class_='content')[0].h1.text
    except Exception:
        mingcheng =''

    try:    #每一个都分开来try，避免漏采数据        
        dianhua = re.findall('电话：</span><span class="cvlu"> <span style="color: #000;">(.*?)</span>',n)[0].strip()
    except Exception:
        dianhua =''

    try:    #每一个都分开来try，避免漏采数据         
        n=len(soup.find_all(class_='clearfix font-15 m-b-sm'))
        gengduo =[]
        for i in range(0,n):
            gengduo.append(soup.find_all(class_='clearfix font-15 m-b-sm')[i].text.replace(' ', '').replace('\n', ','))
        gengduo=str(gengduo)
    except Exception:
        gengduo =''

       


    result = [mingcheng,dianhua,gengduo,wangzhan,youxiang,faren,zhuce,shijiao,zhuangtai,shijian,leixing,hangye,jiguan,quyu,canbao,renshu,fanwei,jianjie,fengxian]    
    return(result)





