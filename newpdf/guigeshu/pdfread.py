# -*- coding: utf-8 -*-
from urllib.request import Request
from urllib.request import quote
from urllib.request import urlopen

import pandas as pd
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

headers = {'content-type': 'application/json',
                    'Accept-Encoding': 'gzip, deflate',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}

baseurl = "http://"


def parse(docucode, txtcode):
        try:

                # 打开在线PDF文档
                #_path = baseurl + quote(docucode) + "?random=0.3006649122149502"
                #_path = baseurl + quote(docucode)
                #request = Request(url=_path, headers=headers)  # 随机从user_agent列表中抽取一个元素
                #fp = urlopen(request,timeout=500)    #timeout设置超时的时间,防止出现访问超时问题
                # 读取本地文件
                path = '1.pdf'
                fp = open(path, 'rb')
                # 用文件对象来创建一个pdf文档分析器
                praser_pdf = PDFParser(fp)
                # 创建一个PDF文档
                doc = PDFDocument()
                # 连接分析器 与文档对象
                praser_pdf.set_document(doc)
                doc.set_parser(praser_pdf)
                # 提供初始化密码doc.initialize("123456")
                # 如果没有密码 就创建一个空的字符串
                doc.initialize()
                # 检测文档是否提供txt转换，不提供就忽略
                if not doc.is_extractable:
                        raise PDFTextExtractionNotAllowed
                else:
                        # 创建PDf资源管理器 来管理共享资源
                        rsrcmgr = PDFResourceManager()
                        # 创建一个PDF参数分析器
                        laparams = LAParams()
                        # 创建聚合器
                        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                        # 创建一个PDF页面解释器对象
                        interpreter = PDFPageInterpreter(rsrcmgr, device)
                        
                        
                        # 循环遍历列表，每次处理一页的内容
                        # doc.get_pages() 获取page列表
                        for page in doc.get_pages():
                                # 使用页面解释器来读取
                                interpreter.process_page(page)
                                # 使用聚合器获取内容
                                layout = device.get_result()
                                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox,
                                # LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                                for out in layout:
                                        # 判断是否含有get_text()方法，图片之类的就没有
                                        # if ``hasattr(out,"get_text"):
                                        docname = str(txtcode).split('.')[0]+'.txt'
                                        with open(docname, 'a') as f:
                                                if isinstance(out, LTTextBoxHorizontal):
                                                        results = out.get_text()
                                                        #print(results)
                                                        f.write(results)
        except Exception as e:      #抛出超时异常
                        print("a", str(e))

pdfurl = 'www.sse.com.cn/disclosure/credibility/supervision/inquiries/opinion/c/8135857143683813.pdf'
txtname = 'ceshi'
parse(pdfurl, txtname)
