# -*- coding: utf-8 -*-
import requests
from scrapy import Request, FormRequest
from scrapy import Spider
from scrapy.shell import inspect_response
from snumatch.items import SnumatchItem


class SnumatchspiderSpider(Spider):
    name = "snumatchspider"
    allowed_domains = ["www.snumatch.com"]
    start_urls = ['http://www.snumatch.com/profile/18693/']
    login_page = 'http://www.snumatch.com/login/'
    profile_url = 'http://www.snumatch.com/profile/%d/'

    custom_settings = {
        'FEED_EXPORT_FIELDS' : ["id", "nick_name", "birthyear", "graduate", "location", "intro_text", "image_url",],
    }

    def start_requests(self):
        print "start_requests"
        return [FormRequest(
                url="http://www.snumatch.com/user/login/",
                formdata={"email" : "@myemail",
                          "pass" : "@mypass"},
                callback= self.tmp_callback)]

    def tmp_callback(self, response):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        user_num = int(response.url.split("/")[-2])

        if response.xpath("/html/body/p/text()").extract_first() == "error":

            print "user_num : %d" % user_num
            if user_num <= 39999:
                next_url = self.profile_url % (user_num + 1)
                yield Request(next_url, callback=self.parse, dont_filter=True)
        else:
            basic_info, profile = response.xpath("//div[@class='profile-list profile-item']")
            # inspect_response(response, self)

            basic_info_list = basic_info.xpath(".//div[@class='ui-grid-a profile-row']//p/text()").extract()
            basic_info_list.pop(0)
            if basic_info_list[0] != u'이메일':
                nick_name = basic_info_list.pop(0)
            else:
                nick_name = ''
            basic_info_list.pop(0)
            if basic_info_list[0] != u'성별':
                email = basic_info_list.pop(0)
            else:
                email = ''
            basic_info_list.pop(0)
            if basic_info_list[0] != u'출생년도':
                gender = basic_info_list.pop(0)
            else:
                gender = ''
            basic_info_list.pop(0)
            if basic_info_list[0] != u'학부':
                birthyear = basic_info_list.pop(0)
            else:
                birthyear = ''
            basic_info_list.pop(0)
            if basic_info_list[0] != u'지역':
                graduate = basic_info_list.pop(0)
            else:
                graduate = ''
            basic_info_list.pop(0)
            if basic_info_list[0] != u'연락처':
                location = basic_info_list.pop(0)
            else:
                location = ''
            basic_info_list.pop(0)
            if len(basic_info_list) != 0:
                phone_number = basic_info_list.pop(0)
            else:
                phone_number = ''

            if gender == u"여자":
                intro_text = profile.xpath("string(div[@class='profile-row ui-grid-a']/p)").extract_first()
                intro_text = intro_text.replace(',', '*')

                tmp = response.xpath("//div[@class='profile-picture-big circleBase']/@style").extract_first()
                image_url = tmp[tmp.find('(') + 1:tmp.find(')')]

                if image_url != "http://asset.snumatch.com/image/female.png?1":
                    self.download_image(image_url, user_num)

                yield SnumatchItem(
                    id = user_num,
                    nick_name = nick_name,
                    email = email,
                    gender = gender,
                    birthyear = birthyear,
                    graduate = graduate,
                    location = location,
                    phone_number = phone_number,
                    intro_text = intro_text,
                    image_url = image_url
                )
            print "user_num : %d" % user_num
            if user_num <= 39999:
                next_url = self.profile_url % (user_num + 1)
                yield Request(next_url, callback=self.parse, dont_filter=True)

    def download_image(self, image_url, user_num):
        img_data = requests.get(image_url).content
        with open('/home/dlstnry/PycharmProjects/snumatch_scraping/snumatch/images/%d.png'% user_num, 'wb+') as handler:
            handler.write(img_data)


