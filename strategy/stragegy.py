import math
import logging

import pandas as pd


from data.daily_data import DataAPI

logger = logging.getLogger(__name__)


class Strategy:

    def __init__(self, account, data_api):
        self.account = account
        self.data_api = data_api

        # 买卖股票佣金
        self.commission_rate = 0.0002
        # 最小买卖佣金
        self.commission_min = 5.0
        # 印花税 - 目前只有卖出股票算印花税

    def strategy_get_account(self):
        return self.account.get_holding_stock()

    def strategy_get_total_asset(self):
        return self.account.get_total_asset()

    def ma20_strategy(self):
        # self.data_api.get_df_data_from_cvs()

        # 最后一行第一次读进来没用，直接当成昨天数据
        df_last_row = self.data_api.get_data_tail(1)
        y_open = df_last_row.at[0, 'open']
        y_close = df_last_row.at[0, 'close']
        y_ma20 = df_last_row.at[0, 'ma20']

        for row in self.data_api.get_stock_data_except_last_row():
            ts_code = str(row['ts_code'])
            trade_date = str(row['trade_date'])
            today_open = row['open']
            today_close = row['close']
            today_ma20 = row['ma20']

            # 未持仓01
            if max(y_open, y_close) <= y_ma20 or y_close < y_ma20 < y_open:
                if today_close > today_ma20:
                    available_asset = self.account.get_available_asset()
                    max_buy_number = math.floor((available_asset / today_close) / 100) * 100
                    buy_price = today_ma20
                    # 计算佣金, 如果实际佣金金额小于5，那么佣金=5
                    temp_commission = buy_price * max_buy_number * self.commission_rate
                    buy_commission = 5 if temp_commission < 5 else temp_commission
                    # 如果总花费(+佣金)的金额大于可用资金，那就少买100股
                    if buy_price * max_buy_number + buy_commission > available_asset:
                        max_buy_number = max_buy_number - 100

                    self.account.buy(stock_code=ts_code, stock_name="LDGF", buy_number=max_buy_number, buy_price=buy_price, buy_date=trade_date)

                    df_current_stock_info = self.strategy_get_account()
                    print(f'Buy info: Buy on day {trade_date}, buy stock number {max_buy_number},  buy price {buy_price}')
                    print('---' * 10 + ' Current holding stock info ' + '---' * 10)
                    print(df_current_stock_info.to_string())
                    print('---' * 30)
                    logger.info('Buy in 未持仓01')

                y_open = today_open
                y_close = today_close
                y_ma20 = today_ma20

                continue

            # 持仓011
            if min(y_open, y_close) >= y_ma20 or y_open < y_ma20 < y_close:
                if today_close < today_ma20:
                    temp_holding_stock = self.account.get_holding_stock()
                    if not temp_holding_stock.empty:
                        stock_available = temp_holding_stock[(temp_holding_stock['StockCode'] == ts_code)][
                            'StockAvailable'].sum()
                        self.account.sale(stock_code=ts_code, stock_name="LDGF", sale_number=stock_available, sale_price=today_ma20, sale_date=trade_date)
                        print(f'--Sale on day {trade_date}, sale stock number {stock_available}, sale stock price {today_ma20}')
                        logger.info('Sale in 未持仓011')

                        current_total_asset = self.strategy_get_total_asset()
                        print(f'--Current total asset is ({current_total_asset})')
                        print('===' * 30)

                y_close = today_close
                y_open = today_open
                y_ma20 = today_ma20

                continue

            # # 未持仓02
            # if y_close < y_ma20 < y_open:
            #     if today_close > 20:
            #         available_asset = self.account.get_available_asset()
            #         max_buy_number = math.floor((available_asset / today_close) / 100) * 100
            #         self.account.buy(stock_code=ts_code, stock_name="LDGF", buy_number=max_buy_number, buy_price=today_close, buy_date=trade_date)
            #         logger.info('Buy in 未持仓02')
            #     y_close = today_close
            #     y_open = today_open
            #
            #     continue
            #
            # # 持仓22
            # if y_open < y_ma20 < y_close:
            #     if today_close < 20:
            #         temp_holding_stock = self.account.get_holding_stock()
            #         stock_available = temp_holding_stock[(temp_holding_stock['StockCode'] == ts_code)]['StockAvailable'].sum()
            #         self.account.sale(stock_code=ts_code, stock_name="LDGF", sale_number=stock_available, sale_price=today_close, sale_date=trade_date)
            #         logger.info('Sale in 未持仓022')
            #     y_close = today_close
            #     y_open = today_open
            #
            #     continue


