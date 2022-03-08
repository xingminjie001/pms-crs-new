# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from common.readconfig import ReadConfig
from sshtunnel import SSHTunnelForwarder
import pymssql,pymysql
import paramiko
import datetime
readconfig=ReadConfig()

class ConnectMysql(object):
    def __init__(self):
        self.sqlserver = readconfig.get_config_section_dict('sqlserver')
        self.mysql = readconfig.get_config_section_dict('mysql')
    #吃早餐
    def upadte_bkdt(self):
        con = pymssql.connect(self.sqlserver['ip'], self.sqlserver['username'], self.sqlserver['password'],
                              self.sqlserver['database'], autocommit=True)
        cur = con.cursor()
        date = str(datetime.date.today())
        sql1 = "update htldt set htl_dt = '{}',audit_dt = '{}' where htl_cd = 'lc01'".format(date,date)

        cur.execute(sql1)

        sql2 = "update breakfast set htl_dt = '{}' where htl_cd = 'lc01' and rm_num = 1129 and telephone = '18310429430'".format(date)
        cur.execute (sql2)
        con.commit()

        sql3 = "delete from bkrecord where rm_num = '1129' and acct_num = '2497334' and post_tm > '{}'".format(date)
        cur.execute (sql3)
        con.commit()

        cur.close()
        con.close()
    #优先选房-pms库
    def choose_room_pms(self):
        con = pymssql.connect(self.sqlserver['ip'], self.sqlserver['username'], self.sqlserver['password'],
                              self.sqlserver['database'], autocommit=True)
        cur = con.cursor()
        #修改酒店日期
        sql1 = "update htldt set htl_dt = '2020-04-02 00:00:00',audit_dt = '2020-04-02 00:00:00' where htl_cd = 'lc01'"
        cur.execute (sql1)
        #预订单2502066-93119房间
        sql2 = "update account set acct_stus = '1',rm_num = '',channel_cd = 'DLT1' where acct_num = '2502066'"
        cur.execute (sql2)
        # 在店单2502065-93118房间
        sql3 = "update account set acct_stus = '4',rm_num = '93118' where acct_num = '2502065'"
        cur.execute(sql3)
        # 关闭房1160 空房93119 在店房93118
        sql4 = "update rmstus set rm_stus = 'I' where rm_num = '1160' and htl_cd = 'lc01'"
        sql4 = "update rmstus set rm_stus = 'V' where rm_num = '93119' and htl_cd = 'lc01'"
        sql4 = "update rmstus set rm_stus = 'O' where rm_num = '93118' and htl_cd = 'lc01'"
        cur.execute(sql4)
        # 退房-需要修改在店状态
        sql5 = "update account set acct_stus = '4' where acct_num = '2502020'"
        cur.execute(sql5)
        con.commit()

        cur.close()
        con.close()
    #优先选房
    def choose_room(self):
        con = pymysql.connect(database=self.mysql['database'],user=self.mysql['username'],password=self.mysql['password'],host=self.mysql['ip'],port = 3306,charset='utf8')
        cur = con.cursor()
        sql1 = "update appointment_checkin set status = 0 where hotel_id = '100012' and room_no = '93030'"
        cur.execute(sql1)
        con.commit()

        cur.close()
        con.close()

if __name__ == '__main__':
    a=ConnectMysql()
    #a.upadte_bkdt()
    a.choose_room_pms()
    # a.choose_room()
    # a.LoginServerWithPkey()


