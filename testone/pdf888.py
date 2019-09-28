# -*- coding: utf-8 -*-
import re
import os
import pandas as pd
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

FENGZHUANG={'L':'3225','K':'3225','M':'DIP','D':'7050'}
DIANYA={'3':'3.3V','2.85':'2.85V','2.5':'2.5V','1.8':'1.8V','5':'5.0V'}
ZHANKONG={'5':'45%~55%','6':'40%~60%'}
SHUCHU={'D':'LVDS','P':'PECL/LVPECL','H':'HCSL'}
CRYSTAL=('K','KC','KD','N','C','D','HC','WB','J')
OSC=('L','R','OF','ON')
CFOSC=('LH','RH','OH')

def filelist():
    pdflist = []
    for files in os.walk("/home/shiyanlou/testone/testone/"):
        for name in files:
            for real in name :
                (realname,nametype) = os.path.splitext(real)
                if nametype==".pdf":
                    pdflist.append(real)
    return pdflist
def parse(filepath):
        try:
            fp = open(filepath, 'rb')
            praser_pdf = PDFParser(fp)
            doc = PDFDocument()
            praser_pdf.set_document(doc)
            doc.set_parser(praser_pdf)
            doc.initialize()
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
            else:
                rsrcmgr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                results = []
                page = next(doc.get_pages())
                interpreter.process_page(page)
                layout = device.get_result()
                for out in layout:
                    if isinstance(out, LTTextBoxHorizontal):
                        results.append(out.get_text().strip("\n"))
                return(results)

        except Exception as e:     
            print("a", str(e))
def infolist(allinfo):
    leibie = ()
    liaohao = ()
    kehu = ()
    guigeshu = ()
    riqi = ()
    bianxie = ()
    info = []
    for i in range(len(allinfo)) :
        if re.match('.*-.*-.*-.*-.*',allinfo[i],re.I|re.M):
            leibie = str(allinfo[i-1]).strip()
            liaohao = str(allinfo[i]).strip()
            kehu = str(allinfo[i+1]).strip()
        if re.match('\d\d\d\d-.*-.*',allinfo[i],re.I|re.M):
            guigeshu = str(allinfo[i-1]).strip()
            riqi = str(allinfo[i]).strip()
            bianxie = str(allinfo[i+1]).strip()
    info = [leibie,liaohao,kehu,guigeshu,riqi,bianxie]
    return info
def wuliao(liaohao):
    array = str(liaohao).split('-')
    result = []
    for i in CRYSTAL :
        if array[0] == i:
            sp = ''
            sp = array[4][0:1]
            wp = ''
            wp = array[4][2:3]
            result=[array[0],array[2],array[3],sp,wp]
    return result



if __name__ == "__main__":
    file_list = filelist()
    results = []

    for pdfway in file_list:
        linshi = []
        all_info = parse(pdfway)
        new_info = infolist(all_info)
        linshi.append(pdfway)
        linshi.extend(new_info)
        liaohao = new_info[1]
        wuliaoinfo = wuliao(liaohao)
        linshi.extend(wuliaoinfo)
        results.append(linshi)
    print(len(results))
    print(results)
