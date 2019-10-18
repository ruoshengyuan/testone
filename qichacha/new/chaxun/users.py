

# -*- coding: utf-8 -*-
import scrapy
from ..items import UserItem


class UsersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['shiyanlou.com']

    @property
    def start_urls(self):
        url_temp = 'https://www.shiyanlou.com/users/{}'
        return (url_temp.format(i) for i in range(525000, 524800, -10))

    def parse(self, response):
        item = UserItem(
            name = response.css('div.user-meta span::text').extract()[0].strip(),
            level = response.css('div.user-meta span::text').extract()[1].strip(),
            status = response.css('div.user-status span::text').extract_first(default='无').strip(),
            school_job = response.xpath('//div[@class="user-status"]/span[2]/text()').extract_first(default='无').strip(),
            join_date = response.css('span.user-join-date::text').extract_first().strip(),
            learn_courses_num = response.css('span.tab-item::text').re_first('\D+(\d+)\D+')
        )
        if len(response.css('div.user-avatar img').extract()) == 2:
            item['is_vip'] = True

        yield item