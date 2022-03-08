# -*- coding: utf-8 -*-
import requests,json
from common.readconfig import ReadConfig


config = ReadConfig()


class GetCookies:
    def __init__(self,sheet_name):
        self.timeout = config.get_config_value('apiDomain', 'timeout')
        self.interface = '/api/account/login'
        self.url = config.get_config_value('apiDomain', 'ip') + self.interface
        self.headers = {"content-type": "application/json;charset=UTF-8"}
        if 'CRS' not in sheet_name:
            self.data = config.get_config_value('LoginData', 'PMS_login')
        else:
            self.data=config.get_config_value('LoginData','CRS_login')



    def get_cookies(self):
        self.response = requests.post(self.url,headers = self.headers,json = json.loads(self.data))
        self.content = self.response.json()
        self.cookie = self.response.cookies
        return self.cookie
if __name__ == '__main__':
    sessionkey = GetCookies('PMS').get_cookies()
    print(sessionkey)