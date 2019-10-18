# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 09:46:44 2019

@author: h
"""

class UserItem(scrapy.Item):
    name = scrapy.Field()
    is_vip = scrapy.Field()
    status = scrapy.Field()
    school_job = scrapy.Field()
    level = scrapy.Field()
    join_date = scrapy.Field()
    learn_courses_num = scrapy.Field()