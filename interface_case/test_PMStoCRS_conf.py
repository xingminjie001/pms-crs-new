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

sheet_name='PMS-CRS配置同步'
logger =Logger(logger_name=sheet_name).getlog()
api_xls = base_api.get_xls('case.xlsx',sheet_name)
update_all = Update_all()
getCookies=GetCookies(sheet_name)
LocalConfigHttp=ConfigHttp(sheet_name)
database=get_database.ConnectMysql()

'''
PMS配置同步给CRS的接口
getGroupConfInformation接口，集团没有POS_NAME和POS_TYPE
getHotelConfInformation接口，单店没有ACCOUNT_TYPE SOURCE_CODE  MARKET_CODE   EXPENSE_TYPE PAYMENT_TYPE

入参示例：
{"htlcd":"lc01","GrpCd":"lc", "confTypList":["ACCOUNT_TYPE","POS_TYPE","POS_NAME"]}
{"htlcd":"lc01","GrpCd":"lc", "confTypList":["ACCOUNT_TYPE","SOURCE_CODE","MARKET_CODE","EXPENSE_TYPE","TRANSACTION_CODE","ROOM_TYPE","PAYMENT_TYPE","POS_NAME","POS_TYPE","POS_NAME","RATE_CODE"]}
'''


@ddt.ddt
class TestReverse(unittest.TestCase):
    '''参数化'''

    def setParameters(self,case_id,description,interface,method,data,associate_id,get_param,set_param,message):
        self.case_id = str(case_id)
        self.description = str(description)
        self.interface = str(interface)
        self.method = str(method)
        self.data = str(data)
        self.associate_id = str(associate_id)
        self.get_param = str(get_param)
        self.set_param = str(set_param)
        self.message = str(message)


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
    def testReverse(self,id,description,interface,method,data,associate_id,get_param,set_param,message):
        self.setParameters(id,description,interface,method,data,associate_id,get_param,set_param,message)
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

    #断言，截取返回数据中的confItemList，当len(confItemList)>1说明配置取到了，len(confItemList)=0说明没有此配置
    def checkResult(self):
        if int(self.message) == 1:
            self.assertGreater(len(self.content['confItemList']),int(self.message))
        else:
            self.assertEqual(len(self.content['confItemList']),int(self.message))



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