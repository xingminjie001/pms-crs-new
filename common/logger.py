import logging
import time,os
from common.file_path import LOG_PATH

class Logger:
    def __init__(self,logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        date_time = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        log_file_pathname = os.path.join(LOG_PATH,logger_name+date_time+'.log')

        if not self.logger.handlers:
            fh = logging.FileHandler(log_file_pathname,encoding='utf-8')  # 创建一个handler，用于写入日志文件
            fh.setLevel(logging.INFO)

            console_sh = logging.StreamHandler()  # 再创建一个handler，用于输出到控制台
            console_sh.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            fh.setFormatter(formatter)
            console_sh.setFormatter(formatter)

            self.logger.addHandler(fh)#输出日志文件
            # self.logger.addHandler(console_sh)#输出系统日志

    def getlog(self):
        return self.logger