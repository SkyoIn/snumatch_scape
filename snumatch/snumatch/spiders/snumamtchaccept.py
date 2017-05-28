# -*- coding: utf-8 -*-
import requests
from scrapy import Request, FormRequest
from scrapy import Spider
from scrapy.shell import inspect_response
import pandas

class SnumatchsacceptSpider(Spider):
    name = "snumatchaccept"
    allowed_domains = ["www.snumatch.com"]
    start_urls = ['http://www.snumatch.com/match/accept/']
    login_page = 'http://www.snumatch.com/login/'


    def start_requests(self):
        print "start_requests"
        return [FormRequest(
                url="http://www.snumatch.com/user/login/",
                formdata={"email" : "@myemail",
                          "pass" : "@mypass"},
                callback= self.tmp_callback)]

    def tmp_callback(self, response):
        # for url in self.start_urls:
        # result = pandas.read_csv('/home/dlstnry/PycharmProjects/snumatch_scraping/snumatch/snumatch_only_woman_18693.csv')
        # under_1989 = result["birthyear"] >= "1989"
        # result_under_1989 = result[under_1989]
        # for url in result_under_1989["id"].tolist():
            yield FormRequest(
                url="http://www.snumatch.com/match/dash/",
                formdata={"to" : str(18210)},
                callback= self.parse)

    def parse(self, response):
        print response.body


