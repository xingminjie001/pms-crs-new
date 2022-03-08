import sys
from common.request_update import Update_all
update_all=Update_all()
sys.setrecursionlimit(10000)


def get_log_content(id,log_name):#获取log文件出参
    content=update_all.get_content(id,log_name,'出参','对比')
    return content

if __name__ == '__main__':
    pass



