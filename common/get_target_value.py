import json



#从一个json中获取某个键的值
def get_target_value(key, dic, tmp_list):
    """
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """

    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '

    if key in dic.keys() and dic[key]!=None:
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
    else:
        for value in dic.values():  # 传入数据不符合则对其value值进行遍历
            if isinstance(value, dict):
                get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(value, (list, tuple)):
                _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
    return tmp_list


def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)   # 传入数据的value值是列表或者元组，则调用自身

if __name__ == "__main__":
    content ={'handleDto': {}, 'responseCommonDto': {'resvNo': None, 'errorLevel': '0', 'invokerEndTime': 4938829387425979, 'lans': None, 'message': '000000', 'resultCode': '0', 'sessionKey': None, 'token': '6af80826-eba3-4e45-bb32-78b40541fef4', 'tracerId': None, 'userUid': None}, 'resultData': [{'acctNo': ['F0010160'], 'arrDt': None, 'breakFlg': None, 'dptDt': None, 'errorFlg': '0', 'errorRoomNums': None, 'noShareRoomNums': None, 'resvNo': 'R0010134', 'shareAcctNos': None, 'shareFlg': None, 'shareRoomNums': None, 'shareSeq': 'S0010160'}]}

    # data = json.loads(content)
    # print(data)
    list1=[]
    print(get_target_value('resvNo',content,list1))

