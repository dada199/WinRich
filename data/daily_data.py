import pandas as pd
import numpy as np
import time
import os
import logging

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_files_folder = project_path + '\\data_files'

logger = logging.getLogger(__name__)


class DataAPI:

    def __init__(self):
        # 股票交易信息 pandas DataFrame
        self._df_data = pd.DataFrame()

    def get_df_data_from_cvs(self, csv_file_name):
        """

        :param csv_file_name:
        :return: get daily trading data from cvs file.
        """
        full_path = os.path.join(data_files_folder, csv_file_name)
        if not os.path.exists(full_path):
            logger.error(f'There is no file {csv_file_name}')
            raise FileNotFoundError
        logger.info(f'Stock trading data file {csv_file_name}')

        try:
            self._df_data = pd.read_csv(full_path, encoding='utf-8')

        except IOError:
            logger.info(f'There is no file {csv_file_name}')

    def get_data_tail(self, n):
        """
        :param n: int
        :return: DataFrame
        获取交易数据的最后n行
        """
        if not self._df_data.empty:
            df_tail = self._df_data.tail(n)
            df_tail = df_tail.reset_index()
            return df_tail
        else:
            logger.error(f'Please call get_df_data_from_cvs() to get trading data from cvs.')
            raise ValueError

    def get_stock_data_except_last_row(self):
        """
        获取除了最后一行的日交易数据
        :return:
        """
        if not self._df_data.empty:
            # [:-1]舍弃df的最后一行
            df_except_last = self._df_data[:-1]
        else:
            logger.error(f'Please call get_df_data_from_cvs() to get trading data from cvs.')
            raise ValueError

        # [::-1]反序
        for index, values in df_except_last[::-1].iterrows():
            # print(values['trade_date'], type(str(values['trade_date'])), values['open'], type(values['open']))
            yield values
