import logging.config
import time

from data.daily_data import DataAPI
from account.account_info import Account
from strategy.stragegy import Strategy
from visualization.date_profit_pyplot import draw_date_profit_plot
from util.setting_path import download_path, datafiles_path
from util.files_helper import list_files
from util.count_time import time_it
from common import contants as ct


# 读取日志配置文件内容
logging.config.fileConfig(ct.LOGGING_CONF_PATH)

# 创建一个日志器logger
logger = logging.getLogger('stock_strategy')

# csv_file = '002024.csv'


def back_test(csv_file):
    data_api = DataAPI()
    data_api.get_df_data_from_cvs(csv_file)

    account = Account()
    account.transfer = ct.START_CAPITAL

    strategy = Strategy(account, data_api)

    strategy.ma20_strategy()

    df_holding_stock_info = strategy.strategy_get_account()

    print(df_holding_stock_info.to_string())

    print("当前可用资产： " + str(account.get_available_asset()))
    print("当前总资产： " + str(account.get_total_asset()))
    print("盈利情况： " + str(account.get_total_profit()))

    logger.info("当前可用资产： " + str(account.get_available_asset()))
    logger.info("当前总资产： " + str(account.get_total_asset()))
    logger.info("盈利情况： " + str(account.get_total_profit()))

    save_pic_name = download_path + '\\' + csv_file.split('.')[0]
    draw_date_profit_plot(strategy.strategy_get_sale_trading_date_list(), strategy.strategy_get_current_profit_list(),
                          pic_name=save_pic_name)


@time_it
def run_all_back_test():
    csv_files = list_files(datafiles_path, '.csv')
    print('Total csv file: ' + str(len(csv_files)))

    for csv_file in csv_files:
        back_test(csv_file)


@time_it
def run_pool():
    from multiprocessing import Pool

    cup_work_num = 5

    csv_files = list_files(datafiles_path, '.csv')
    print('Total csv file: ' + str(len(csv_files)))

    with Pool(cup_work_num) as pool:
        pool.map(back_test, csv_files)


if __name__ == '__main__':

    # run_all_back_test()

    run_pool()




