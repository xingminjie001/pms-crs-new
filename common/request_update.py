import json
import os
import re
from common.update_json import update_target_value
from common.get_target_value import get_target_value
from common.file_path import LOG_PATH

class Update_all():
    def __init__(self):
        self.logs = os.listdir(LOG_PATH)



    def get_associate_id(self,api_xls, id):
        for list in api_xls:
            if str(list[0]) == id and str(list[5]) != "":
                return str(list[5])
        return ""

    def get_content(self,id,log_name,type,what):
        #筛选要比对的log文件
        log_list = []
        for name in self.logs:
            if log_name in name:
                log_list.append(name)
        if what=='修改':
            current_log=os.path.join(LOG_PATH, max(log_list))#获取最新log文件
        else:
            try:
                current_log=os.path.join(LOG_PATH, log_list[len(log_list)-1])#获取上次执行log文件
            except:
                return
        with open(current_log, 'rb') as f:
            while True:
                line = f.readline().decode("utf-8").strip()
                if "case_id" + id + type in line:
                    # print("case_id" + id + type)
                    content = line.split("case_id" + id + type)[1]
                    content = re.sub('\'', '^', content)
                    content = re.sub('\"', '\'', content)
                    content = re.sub('\^', '\"', content)
                    content = re.sub('None', 'null', content)
                    content = re.sub('False', 'false', content)
                    content = re.sub('True', 'true', content)
                    content=json.loads(content)
                    return content
                if not line:
                    return ""

    #更新当前被测接口的入参
    def update_all(self,log_name,id,data,get_param,set_param):
        get_param_list = get_param.split(',')
        set_param_list = set_param.split(',')
        id_list=id.split(',')
        if len(id_list)==1:    #判断依赖的用例个数
            content = self.get_content(id_list[0], log_name, "出参", "修改")
            for get_param, set_param in zip(get_param_list, set_param_list):
                    global value
                    result_list = []
                        # 如果关联接口的出参没有要获取的参数或者出参中获取的参数为none，从关联接口的入参找
                    try:
                        value = get_target_value(get_param, content, result_list)[0]   #获取修改的值
                        if str(value) == "None":
                            content1 = self.get_content(id,log_name, "入参","修改")    #获取入参
                            try:
                                value = get_target_value(get_param, content1, result_list)[0]
                            except:
                                pass

                    except:
                        content1 = self.get_content(id,log_name, "入参","修改")
                        try:
                            value = get_target_value(get_param, content1, result_list)[0]
                        except:
                            pass
                    if isinstance(data, dict):
                        update_target_value(set_param, data, value)
                    else:
                        data=json.loads(data)
                        update_target_value(set_param, data, value)
        else:
            for id,get_param, set_param in zip(id_list,get_param_list, set_param_list):
                content = self.get_content(id,log_name, "出参", "修改")
                result_list = []
                # global value
                try:
                    value = get_target_value(get_param, content, result_list)[0]  # 获取修改的值
                    if str(value) == "None":
                        content1 = self.get_content(id,log_name, "入参", "修改")  # 获取入参
                        try:
                            result_list = []
                            value = get_target_value(get_param, content1, result_list)[0]
                        except:
                            pass

                except:
                    content1 = self.get_content(id,log_name, "入参", "修改")
                    try:
                        value = get_target_value(get_param, content1, result_list)[0]
                    except:
                        pass
                if isinstance(data, dict):
                    update_target_value(set_param, data, value)
                else:
                    data = json.loads(data)
                    update_target_value(set_param, data, value)


        return data


