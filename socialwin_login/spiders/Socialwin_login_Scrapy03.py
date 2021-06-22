import scrapy
import requests

from scrapy.http import FormRequest, Request
from scrapy.utils.response import open_in_browser

from copy import deepcopy
from scrapy.http import Headers

class Headers2(Headers):

    def __init__(self, seq=None, encoding='utf-8'):

        Headers.__init__(self, seq, encoding)

    def normkey(self, key):
        """Method to normalize dictionary key access"""
        return key.lower()


class LoginSpiderSocialwin(scrapy.Spider):
    name = "loginToScrapeSocialwin"
    start_urls = ["https://www.socialwin.be/nl/user/login"]
    handle_httpstatus_list = [307, 400] # 302

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self,response):
        print(f"Request headers used:\n{response.request.headers}")
        if response.status == 307 and "dbs.larciergroup.com" in response.headers.getlist('Location')[0].decode("utf-8"):
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            }
            requests.get(f'{response.headers.getlist("Location")[0].decode("utf-8")}',
                            headers=headers,
                            allow_redirects=False)
            yield Request("https://www.socialwin.be/nl/user/login?redirect_counter=1")
        elif response.status == 400:
            pass
        else:
            request = FormRequest.from_response(
                response,
                formdata={"login[username]":"glenn.van.oevelen@acerta.be", "login[password]":"_______"},
                callback=self.after_login,
                meta={'dont_redirect': False}
            )
            print(f"Body of request:\n{request.body}")
            yield request


    def after_login(self,response):
        with open("login_output.html","w") as file:
            file.write(response.body.decode())
        # if response.status == 302:
        #     print(f"Response headers:\n{response.headers}")
        #     cookies = [cookie.decode("utf-8") for cookie in response.headers.getlist("Set-Cookie")]
        #     cookies = [cookie.split('; ') for cookie in cookies][-1:]
        #     cookies = [{'name': cookie[0].split('=')[0], 'value': '='.join(cookie[0].split('=')[1:]) if '=' in cookie[0] else '', 'domain': 'socialwin.be', 'path':'/'} for cookie in cookies]
        #     cookies = {cookies[0]['name']: cookies[0]['value']}
        #     print(f"Cookies to include:\n{cookies}")
        #     request = Request(
        #         f'{response.headers.getlist("Location")[0].decode("utf-8")}',
        #         cookies=cookies,
        #         callback=self.after_login,
        #         meta={'dont_merge_cookies': True}
        #     )
        #     yield request

        print(f"Request headers used:\n{response.request.headers}")
        open_in_browser(response)

    
