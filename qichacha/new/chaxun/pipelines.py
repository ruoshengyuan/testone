# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:50:23 2019

@author: h
"""

from datetime import datetime
#from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, User, engine
from shiyanlou.items import CourseItem, UserItem


class ShiyanlouPipeline(object):

    def process_item(self, item, spider):
        """ 对不同的 item 使用不同的处理函数
        """
        if isinstance(item, CourseItem):
            self._process_course_item(item)
        else:
            self._process_user_item(item)
        return item

    def _process_course_item(self, item):
        item['students'] = int(item['students'])
        self.session.add(Course(**item))

    def _process_user_item(self, item):
        # 抓取到的数据类似 'L100'，需要去掉 'L' 然后转化为 int
        item['level'] = int(item['level'][1:])
        # 抓取到的数据类似 '2017-01-01 加入实验楼'，把其中的日期字符串转换为 date 对象
        item['join_date'] = datetime.strptime(item['join_date'].split()[0], '%Y-%m-%d')
        # 学习课程数目转化为 int
        item['learn_courses_num'] = int(item['learn_courses_num'])
        # 添加到 session
        self.session.add(User(**item))

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
