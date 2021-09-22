from data.tushare_data import get_daily_data

import os

data_file_path = 'E:\\PycharmProjects\\Autotrading\\datafile'
st_code = '000651.sz'

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_files_folder = project_path + '\\data_files'


if __name__ == '__main__':

    full_path = os.path.join(data_files_folder, st_code.split('.')[0] + '.csv')
    get_daily_data(st_code=st_code, start_date='19961118', end_date='', adj='qfq', ma_type=[10,20,30,60])


