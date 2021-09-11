import math
import logging

import pandas as pd


from data.daily_data import DataAPI

logger = logging.getLogger(__name__)


class Strategy:

    def __init__(self, account, data_api):
        self.account = account
        self.data_api = data_api

    def strategy_get_account(self):
        return self.account.get_holding_stock()

    def ma20_strategy(self):
        # self.data_api.get_df_data_from_cvs()

        df_last_row = self.data_api.get_data_tail(1)
        y_open = df_last_row.at[0, 'open']
        y_close = df_last_row.at[0, 'close']
        y_ma20 = df_last_row.at[0, 'ma30']

        for row in self.data_api.get_stock_data_except_last_row():
            ts_code = str(row['ts_code'])
            trade_date = str(row['trade_date'])
            today_open = row['open']
            today_close = row['close']
            today_ma20 = row['ma30']

            # 未持仓01
            if max(y_open, y_close) <= y_ma20 or y_close < y_ma20 < y_open:
                if today_close > today_ma20:
                    available_asset = self.account.get_available_asset()
                    max_buy_number = math.floor((available_asset / today_close) / 100) * 100
                    self.account.buy(stock_code=ts_code, stock_name="LDGF", buy_number=max_buy_number, buy_price=today_close, buy_date=trade_date)
                    print(f'Buy on day {trade_date}')
                    df_current_stock_info = self.strategy_get_account()
                    print(df_current_stock_info.to_string())
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
                        self.account.sale(stock_code=ts_code, stock_name="LDGF", sale_number=stock_available,
                                          sale_price=today_close, sale_date=trade_date)
                        print(f'--Sale on day {trade_date}')
                        logger.info('Sale in 未持仓011')

                        df_current_stock_info = self.strategy_get_account()
                        print(df_current_stock_info.to_string())

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


