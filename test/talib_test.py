import os

import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_files_folder = project_path + '\\data_files'
csv_file = '002230.csv'


def get_talib_ma(ma=20):
    full_path = os.path.join(data_files_folder, csv_file)
    df_stock_daily = pd.read_csv(full_path, encoding='utf-8')

    df_stock_daily['talib_ma20'] = talib.SMA(df_stock_daily['close'][::-1], timeperiod=ma)
    df_stock_daily['talib_ma20'][::-1].fillna(method="bfill", inplace=True)

    df_stock_daily.to_csv(os.path.join(data_files_folder, csv_file.split('.')[0]+'_talib.csv'))

def draw_ma_line(ma=20):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)

    full_path = os.path.join(data_files_folder, csv_file)
    df_stock_daily = pd.read_csv(full_path, encoding='utf-8')

    df_stock_daily['talib_ma5'] = talib.SMA(df_stock_daily['close'][::-1], timeperiod=ma-15)
    df_stock_daily['talib_ma5'][::-1].fillna(method="bfill", inplace=True)

    df_stock_daily['talib_ma20'] = talib.SMA(df_stock_daily['close'][::-1], timeperiod=ma)
    df_stock_daily['talib_ma20'][::-1].fillna(method="bfill", inplace=True)

    df_stock_daily['talib_ma60'] = talib.SMA(df_stock_daily['close'][::-1], timeperiod=ma + 40)
    df_stock_daily['talib_ma60'][::-1].fillna(method="bfill", inplace=True)

    ax.plot(np.arange(0, len(df_stock_daily)), df_stock_daily["talib_ma5"])
    ax.plot(np.arange(0, len(df_stock_daily)), df_stock_daily["talib_ma20"])
    ax.plot(np.arange(0, len(df_stock_daily)), df_stock_daily["talib_ma60"])

    def format_date(x, pos=None):
        if x < 0 or x > len(df_stock_daily['trade_date']) - 1:
            return ''
        return df_stock_daily['trade_date'][int(x)]

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.show()




if __name__ == '__main__':
    draw_ma_line(ma=20)
