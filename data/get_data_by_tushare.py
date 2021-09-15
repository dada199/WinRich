from data.tushare_data import get_daily_data

import os

data_file_path = 'E:\\PycharmProjects\\Autotrading\\datafile'
st_code = '002230.sz'

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_files_folder = project_path + '\\data_files'


if __name__ == '__main__':

    full_path = os.path.join(data_files_folder, st_code.split('.')[0] + '.csv')
    get_daily_data(st_code=st_code, start_date='20100101', end_date='', ma_type=[20])


