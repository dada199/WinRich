# -*- coding:utf-8 -*-

"""
 * @Author       : Forrest
 * @Date         : 2021-09-23
 * @Description  : config ini file
"""
import os
import logging
from configparser import ConfigParser as conf


logger = logging.getLogger(__name__)

util_path = os.path.dirname(os.path.abspath(__file__))
ini_file_path = util_path + '\\config_ini.ini'


def get_config_value():
    pass

def get_ini(sections="defaults", key):
    conf.read(ini_file_path)

