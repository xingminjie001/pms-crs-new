import json


#更新一个json
#target_value为None，删除目标key：value；不为空，则修改
def update_target_value(keys, dic, target_value):
    """
    :param key: 目标key值
    :param dic: JSON数据
    :param target_value: 用于更新的数据
    """
    if not isinstance(dic, dict):  # 对传入数据进行格式校验
        return 'argv[1] not an dict '
    for key in dic.keys():
        if key==keys:
        #有的关联接口的出参与这里的入参格式可能不同，需要判断
            if isinstance(dic[keys], list) and not isinstance(target_value,list):
                dic[keys] = [target_value]
            elif not isinstance(dic[keys], list) and isinstance(target_value,list):
                dic[keys] = target_value[0]
            else:
                dic[keys] = target_value  # 更新数据
        else:
            for value in dic.values():  # 传入数据不符合则对其value值进行遍历
                # print(dic)
                if isinstance(value, dict):
                    update_target_value(keys, value, target_value)  # 传入数据的value值是字典，则直接调用自身
                elif isinstance(value, (list, tuple)):
                    for val in value:
                        # print(val)
                        update_target_value(keys, val, target_value)
    # print(dic)
    return target_value






# def _update_value(key, val,target_value):
#     for val_ in val:
#         if isinstance(val_, dict):
#             update_target_value(key, val_,target_value)  # 传入数据的value值是字典，则调用update_target_value
#         elif isinstance(val_, (list, tuple)):
#             _update_value(key, val_, target_value)   # 传入数据的value值是列表或者元组，则调用自身

if __name__ == "__main__":
    content ={'submitData': [{'accountDto': {'acctNo': 'a', 'cancelrsnId': '10096'}}]}


    # del_data(key,content)
    # data = json.loads(content)
    update_target_value('acctNo',content,['F0010190'])
    print(content)