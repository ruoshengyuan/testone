# -*- coding:utf-8 -*-
#import scrapy
#
#class ShiyanlouCoursesSpider(scrapy.Spider):
#    """ 
#    使用 scrapy 爬取页面数据需要编写一个爬虫类，该爬虫类要继承 scrapy.Spider 类。在爬虫类中定义要请求的网站和链接、如何从返回的网页提取数据等等。
#    在 scrapy 项目中可能会有多个爬虫，name 属性用于标识每个爬虫，各个爬虫类的 name 值不能相同
#    """
#    name = 'shiyanlou-courses'
#
#    # 注意此方法的方法名字是固定的，不可更改
#    def start_requests(self):
#        # 课程列表页面 URL ，注意此列表中的地址可能有变动，需手动打开页面复制最新地址
#        url_list = ['https://www.shiyanlou.com/courses/',
#                    'https://www.shiyanlou.com/courses/?page_size=20&cursor=bz0yMA%3D%3D',
#                    'https://www.shiyanlou.com/courses/?page_size=20&cursor=bz00MA%3D%3D']
#        # 返回一个生成器，生成 Request 对象，生成器是可迭代对象
#        for url in url_list:
#            yield scrapy.Request(url=url, callback=self.parse)
#
#    # 注意此方法的方法名字也是固定的，不可更改
#    def parse(self, response):
#        # 遍历每个课程的 div.col-md-3
#        for course in response.css('div.col-md-3'):
#            # 使用 css 语法对每个 course 提取数据
#            yield {
#                # 课程名称，注意这里使用 strip 方法去掉字符串前后的空白字符
#                # 所谓空白字符，指的是空格、换行符、制表符
#                # 下面获取 name 的写法还可以省略 h6 的类属性，思考一下为什么可以省略
#                'name': course.css('h6.course-name::text').extract_first().strip(),
#                # 课程描述
#                'description': course.css('div.course-description::text').extract_first().strip(),
#                # 课程类型
#                'type': course.css('span.course-type::text').extract_first().strip(),
#                # 学生人数
#                'students': course.css('span.students-count span::text').extract_first()
#            }

#scrapy runspider spider.py -o data.json
            
import scrapy


class ShiyanlouCoursesSpider(scrapy.Spider):

    name = 'shiyanlou-courses'

    @property
    def start_urls(self):
        """ start_urls  需要返回一个可迭代对象，所以，你可以把它写成一个列表、元组或者生成器，这里用的是列表
        """
        url_list = ['https://www.shiyanlou.com/courses/',
                    'https://www.shiyanlou.com/courses/?page_size=20&cursor=bz0yMA%3D%3D',
                    'https://www.shiyanlou.com/courses/?page_size=20&cursor=bz00MA%3D%3D']
        return url_list

    def parse(self, response):
        for course in response.css('div.col-md-3'):
            yield {
                'name': course.css('h6::text').extract_first().strip(),
                'description': course.css('div.course-description::text').extract_first().strip(),
                'type': course.css('span.course-type::text').extract_first().strip(),
                'students': course.css('span.students-count span::text').extract_first()
            }