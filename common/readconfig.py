# -*- coding: utf-8 -*-

from configparser import ConfigParser
import os
from common.file_path import CONFIG_PATH

# logger = Logger(logger_name='readconfig').getlog()

class ReadConfig:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(os.path.join(CONFIG_PATH,'config.ini'))


    def get_config_section_dict(self,section):
        config_section_dict = {}
        conf_sections = self.config.items(section)
        for conf_section in conf_sections:
            config_section_dict[conf_section[0]] = conf_section[1]
        return config_section_dict

    def get_config_value(self,section,conf_value):
        conf_sections = self.config.get(section,conf_value)
        return conf_sections

if __name__ == '__main__':
    c = ReadConfig()
    print(c.get_config_section_dict('HEADERS'))
    # print(c.get_config_value('HEADERS','jw_uid'))