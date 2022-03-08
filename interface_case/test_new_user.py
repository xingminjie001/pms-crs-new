# -*- coding: utf-8 -*-
#!usr/bin/python
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append("C:/Users/35789/AppData/Roaming/Python/Python36/site-packages")
import unittest,json,ddt
from common.logger import Logger
from common.confighttp import ConfigHttp
from common import base_api
from common.get_cookie import GetCookies
from common.request_update import Update_all
from common.check import JsonCompare
from common import myassert
from common import get_database



#申明类、公共参数

sheet_name='PMS-拉新'
logger =Logger(logger_name=sheet_name).getlog()
api_xls = base_api.get_xls('case.xlsx',sheet_name)
update_all = Update_all()
getCookies=GetCookies(sheet_name)
LocalConfigHttp=ConfigHttp(sheet_name)
database=get_database.ConnectMysql()

'''
PMS提供的拉新接口，包括：检查手机号是否是新会员、给手机号发送短信验证码、注册新用户3个接口
检查手机号是否是新会员：http://192.168.32.95:8960/api/RezenMember/CheckPhoneNo
入参：{"grpCd":"LC","htlCd":"lc01","pmsType":"1","param":{"phone":"13344432333","countryCode":"+86","groupCd":"lc"}}
返回：retcode：0   body：false or true  以此为断言

给手机号发送短信验证码：http://192.168.32.95:8960/api/RezenMember/sendSMSByElong
入参：{"grpCd":"LC","htlCd":"lc01","pmsType":"1","param":{"groupCd":"lc","countryCode":"","MobileNo":"15311801297","verificationType":"32","smsFillInfo":["325221"]}}
返回：retcode  0：成功   41：手机号非法   以此为断言

注册新用户：api/RezenMember/createMember
入参：{"grpCd":"LC","htlCd":"lc01","pmsType":"1","param":{"phone":"15819098976","countryCode":"+86","groupCd":"lc","staffCd":"9897","hotelCd":"lc01"}}
返回：retcode ：0   "body": {"resultCode": 1} 或者 "body": {"resultCode": 0}  以此为断言
'''


@ddt.ddt
class TestReverse(unittest.TestCase):
    '''参数化'''

    def setParameters(self,case_id,description,interface,method,data,associate_id,get_param,set_param,message,resultcode):
        self.case_id = str(case_id)
        self.description = str(description)
        self.interface = str(interface)
        self.method = str(method)
        self.data = str(data)
        self.associate_id = str(associate_id)
        self.get_param = str(get_param)
        self.set_param = str(set_param)
        self.message = str(message)
        self.resultcode = str(resultcode)


    @classmethod
    def setUpClass(self):
        global cookie
        cookie = getCookies.get_cookies()
    @classmethod
    def tearDownClass(self):
        pass


    def setUp(self):
        pass
    def tearDown(self):
        pass




    @ddt.data(*api_xls)
    @ddt.unpack
    def testReverse(self,id,description,interface,method,data,associate_id,get_param,set_param,message,resultcode):
        self.setParameters(id,description,interface,method,data,associate_id,get_param,set_param,message,resultcode)
        datas = json.loads(self.data)  #转json
        if self.associate_id != "":#判断是否需要修改入参
            datas = update_all.update_all(sheet_name,self.associate_id,self.data,self.get_param,self.set_param)
        api_url = self.interface  #获取url
        if 'http'in api_url:#判断url格式是否需要拼接
            LocalConfigHttp.set_url2(api_url)
        else:
            LocalConfigHttp.set_url(api_url)
        LocalConfigHttp.set_data(datas)#参数

        LocalConfigHttp.set_cookies(cookie)



        self.response = LocalConfigHttp.post()#调接口
        self.content = self.response.json()


        #日志
        logger.info("case_id" + str(self.case_id)+'请求时间为'+str(self.response.elapsed.microseconds))
        logger.info("case_id" + str(self.case_id) + "入参" + str(datas))
        logger.info("case_id" + str(self.case_id) + "出参" + str(self.content))
        self.checkResult()

    #断言，截取返回数据中的retcode
    def checkResult(self):
        self.assertEqual(self.content["retcode"],int(self.message.split(",")[0]))
        #print(self.case_id,"************retcode",self.content["retcode"],self.message.split(","))

        if len(self.message.split(",")) == 2 and self.message.split(",")[1] == "true":
            self.assertTrue(self.content["body"])
            #print(self.message.split(",")[1])
        elif len(self.message.split(",")) == 2 and self.message.split(",")[1] == "false":
            self.assertFalse(self.content["body"])
        else:
            pass
        if self.resultcode:
            self.assertEqual(self.content["body"]["resultCode"],int(self.resultcode))
        # try:
        #     self.assertEqual(self.content["body"],self.message.split(",")[1])
        #     print(self.case_id,"+++++++++++++body",self.content["body"],self.message.split(",")[1])
        #     try:
        #         self.assertEqual(self.content["body"]["resultCode"],str(self.resultcode))
        #         print(self.case_id,"************body[resultCode]",self.content["body"]["resultCode"],str(self.resultcode))
        #     except:
        #         pass
        # except:
        #     pass


            #断言整个返回
            # expected_result=myassert.get_log_content(self.case_id,sheet_name)#预期
            # check1 = JsonCompare(expected_result,self.content)
            # check2 = JsonCompare(self.content, expected_result)
            #
            # if check1.data_compare_result == [] and check2.data_compare_result == []:
            #     pass
            # else:
            #     raise Exception("接口返回值异常"+str(check1.data_compare_result) + str(check2.data_compare_result))





if __name__ == '__main__':
    unittest.main()