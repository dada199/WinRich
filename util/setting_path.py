# -*- coding:utf-8 -*-

import os
import platform as plf


from common import contants as ct

"""创建本地文件夹
1. setting_path ==> 用于存放配置文件 setting.cfg
2. cache_path ==> 用于存放临时文件
3. log_path ==> 用于存放储存的log
4. download_path ==> 下载的数据/财务文件
5. strategy_path ==> 存放策略模板
6. bin_path ==> 存放一些交易的sdk/bin文件等
"""

if plf.system() == 'Windows':
    winrich_path = ct.WINRICH_BASE_PATH
else:
    winrich_path = os.path.expanduser('~')

base_path = '{}{}{}'.format(winrich_path, os.sep, '.winrich')


def generate_path(name):
    return '{}{}{}'.format(base_path, os.sep, name)


def make_dir(path_name, is_exist=True):
    return os.makedirs(path_name, exist_ok=is_exist)


setting_path = generate_path('setting')
cache_path = generate_path('cache')
log_path = generate_path('log')
download_path = generate_path('download')
strategy_path = generate_path('strategy')
bin_path = generate_path('bin')
datafiles_path = generate_path('datafiles')

make_dir(setting_path, is_exist=True)
make_dir(cache_path, is_exist=True)
make_dir(log_path, is_exist=True)
make_dir(download_path, is_exist=True)
make_dir(strategy_path, is_exist=True)
make_dir(bin_path, is_exist=True)
make_dir(datafiles_path, is_exist=True)
