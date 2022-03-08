class JsonCompare:
    def __init__(self, expect_data, real_data):
        self.expect_data = expect_data
        self.real_data = real_data
        self.data_compare_result = []  # 数据对比结果
        self.defaultroot = ''
        self.compare(expect_data, real_data, self.defaultroot)


    def compare(self, expect_data, real_data, path='/'):
        try:
            if not isinstance(expect_data, (list, tuple, dict)):
                # if isinstance(real_data,unicode):real_data=real_data.encode('utf-8')
                if not type(expect_data) == type(real_data):
                    msg = '数据类型异常:%s:预期类型:%s,实际类型:%s' % (path,type(expect_data), type(real_data))
                    self.data_compare_result.append(msg)
                # elif not expect_data == real_data:
                #     msg = '数值异常:%s:预期值:%s,实际值:%s' % (path, str(expect_data), str(real_data))
                #     self.data_compare_result.append(msg)
            elif isinstance(expect_data, (list, tuple)):  # list,tuple
                if not isinstance(real_data, (list, tuple)):
                    raise IndexError('实际数据不是list:%s' % path)  # 实际数据为非list/tuple类型
                for index, value in enumerate(expect_data):
                    try:
                        if index < len(real_data):
                            self.compare(value, real_data[index], '%s[%d]' % (path, index))
                        else:
                            raise IndexError('不存在的下标：%s[%d]' % (path, index))
                    except Exception as e:
                        if IndexError:
                            self.data_compare_result.append('结构异常or数据缺失:%s' % e.args)
                        else:
                            self.data_compare_result.append('未知异常:%s' % e.args)
            else:  # dict
                if not isinstance(real_data, dict):
                    raise IndexError('实际数据不是dict:%s' % path)  # 实际数据为非dict类型
                for key,value in expect_data.items():
                    try:
                        if key in real_data.keys():
                            self.compare(value, real_data[key], '%s[\'%s\']' % (path, str(key)))
                        else:
                            raise IndexError('不存在的键：%s[\'%s\']' % (path, str(key)))
                    except Exception as e:
                        if IndexError:
                            self.data_compare_result.append('结构异常or数据缺失:%s' % e.args)
                        else:
                            self.data_compare_result.append('未知异常:%s' % e.args)
        except Exception as e:
            self.data_compare_result.append('未知异常:%s' % e.args)


if __name__ == "__main__":
    except_json = {"handleDto":{},"responseCommonDto":{"asyncId":None,"errorLevel":"0","invokerEndTime":3740580612063308,"lans":None,"message":"000000","resultCode":"0","sessionKey":None,"token":"6cf431ad-c842-482b-8127-ad46b0055893","tracerId":None,"userUid":None}}
    real_json = {"handleDto":{},"responseCommonDto":{"asyncId":None,"errorLevel":"1","invokerEndTime":3740580612063307,"lans":None,"message":"000000","resultCode":"0","sessionKey":None,"token":"6cf431ad-c842-482b-8127-ad46b0055893","tracerId":None,"userUid":None}}
    result = JsonCompare(except_json,real_json)
    print(result.data_compare_result)
