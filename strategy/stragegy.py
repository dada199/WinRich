import math
import logging.config

from common import contants as ct

# 读取日志配置文件内容
logging.config.fileConfig(ct.LOGGING_CONF_PATH)

# 创建一个日志器logger
logger = logging.getLogger('stock_strategy')


class Strategy:

    def __init__(self, account, data_api):
        self.account = account
        self.data_api = data_api

        self._sale_stock_day_list = []
        self._current_profit_list = []

        # 买卖股票佣金
        # self.commission_rate = 0.0002
        # 最小买卖佣金
        # self.commission_min = 5.0
        # 印花税 - 目前只有卖出股票算印花税

    def strategy_get_account(self):
        return self.account.get_holding_stock()

    def strategy_get_total_asset(self):
        return self.account.get_total_asset()

    def strategy_get_sale_trading_date_list(self):
        return self._sale_stock_day_list

    def strategy_get_current_profit_list(self):
        return self._current_profit_list

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

            # 未持仓01, 如果 收盘价= ma， 持仓
            if max(y_open, y_close) < y_ma20 or y_close < y_ma20 < y_open or y_close < y_ma20 == y_open:
                if today_close >= today_ma20:
                    available_asset = self.account.get_available_asset()
                    # 计算买入的价格是关键因素
                    # buy_price = round((today_close + today_ma20)/2 + ct.SLIPPAGE, 2)
                    buy_price = round(today_ma20 + ct.SLIPPAGE, 2)
                    # 最大买入数量
                    max_buy_number = math.floor((available_asset / buy_price) / 100) * 100
                    # 计算佣金, 如果实际佣金金额小于5，那么佣金=5
                    temp_commission = buy_price * max_buy_number * ct.COMMISSION_RATE
                    buy_commission = 5.0 if temp_commission < 5.0 else temp_commission
                    # 如果总花费(+佣金)的金额大于可用资金，那就少买100股
                    if buy_price * max_buy_number + buy_commission > available_asset:
                        max_buy_number = max_buy_number - 100

                    self.account.buy(stock_code=ts_code, stock_name="LDGF", buy_number=max_buy_number, buy_price=buy_price, buy_date=trade_date)

                    df_current_stock_info = self.strategy_get_account()
                    print(f'Buy info: Buy on day {trade_date}, buy stock number {max_buy_number},  buy price {buy_price}')
                    print('---' * 10 + ' Current holding stock info ' + '---' * 10)
                    print(df_current_stock_info.to_string())
                    print('---' * 30 + '\n')

                    logger.info(f'Buy info: Buy on day {trade_date}, buy stock number {max_buy_number},  buy price {buy_price}')
                    logger.info('---' * 10 + ' Current holding stock info ' + '---' * 10)
                    logger.info(df_current_stock_info.to_string())
                    logger.info('---' * 30 + '\n')

                y_open = today_open
                y_close = today_close
                y_ma20 = today_ma20
                continue

            # 持仓011
            if min(y_open, y_close) >= y_ma20 or y_open < y_ma20 <= y_close:
                if today_close < today_ma20:
                    temp_holding_stock = self.account.get_holding_stock()
                    if not temp_holding_stock.empty:
                        stock_available = temp_holding_stock[(temp_holding_stock['StockCode'] == ts_code)][
                            'StockAvailable'].sum()
                        # 计算卖出的价格是关键因素
                        # sale_out_price = round((today_close + today_ma20)/2 - ct.SLIPPAGE, 2)
                        sale_out_price = round(today_ma20 - ct.SLIPPAGE, 2)
                        self.account.sale(stock_code=ts_code, stock_name="LDGF", sale_number=stock_available, sale_price=sale_out_price, sale_date=trade_date)

                        print(f'--Sale on day {trade_date}, sale stock number {stock_available}, sale stock price {sale_out_price} \n')
                        logger.info(f'--Sale on day {trade_date}, sale stock number {stock_available}, sale stock price {sale_out_price} \n')

                        current_total_asset = self.strategy_get_total_asset()
                        current_profit = round(self.account.get_total_profit(), 2)

                        # Put sale trading date to list for plot
                        self._sale_stock_day_list.append(trade_date)
                        # Put current total profit to list for plot
                        self._current_profit_list.append(current_profit)

                        print(f'*** Current total asset is ({current_total_asset}), profit: ({current_profit}))')
                        print('===' * 30 + '\n\n')
                        logger.info(f'*** Current total asset is ({current_total_asset}), profit: ({current_profit}))')
                        logger.info('===' * 30 + '\n\n')

                y_close = today_close
                y_open = today_open
                y_ma20 = today_ma20
                continue

