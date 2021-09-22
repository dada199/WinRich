# -*- coding:utf-8 -*-
import pandas as pd
import logging

logger = logging.getLogger(__name__)

stock_info_columns = ['StockCode', 'StockName', 'StockValue', 'StockNumber', 'StockAvailable',
                      'StockCurrentPrice', 'StockCost', 'StockProfitAndLost']


class Account:
    """
    帐户基本信息
    account_id:帐户ID
    _transfer:转账金额
    total_asset: 人民币总资产
    stock_value:持仓市值
    profit_and_loss:持仓盈亏金额
    profit_percentage:盈亏百分比
    available:可用金额
    holding_share_info:持有股票相信信息 pandas Dataframe
    """

    def __init__(self):
        # 账户id
        self._account_id = ""
        # 转账金额
        self._transfer = 0.0
        # 人民币总资产
        self._total_asset = 0.0
        # 持仓市值
        self._stock_value = 0.0
        # 持仓盈亏金额
        self._profit_and_loss = 0.0
        # 盈亏百分比
        self._profit_percentage = 0.0
        # 可用金额
        self._available = 0.0
        # 冻结资金
        self._frozen = 0.0
        # 买卖股票佣金
        self.commission_rate = 0.0002
        # 最小买卖佣金
        self.commission_min = 5.0
        # 印花税率 - 目前只有卖出股票算印花税
        self.stamp_duty_rate = 0.001
        # 每次购买购票的值
        self._new_buy_stock_value = 0.0

        # 持仓股票信息 pandas DataFrame
        self._df_share_info = pd.DataFrame(data=None, columns=stock_info_columns, dtype=object)

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, accountid):
        self._account_id = accountid

    @property
    def transfer(self):
        return self._transfer

    @transfer.setter
    def transfer(self, transfer_balance):
        if not isinstance(transfer_balance, float):
            raise ValueError('Initial balance must be float!')
        # 可用金额
        self._available += transfer_balance
        # 总资产
        self._total_asset += transfer_balance
        if self._total_asset < 0:
            raise ValueError(f'No enough money {transfer_balance} to withdraw.')

        self._transfer = transfer_balance

    def get_total_asset(self):
        # self._total_asset = self.get_stock_value() + self.get_available_asset()
        return round(self._total_asset, 2)

    # 持仓市值
    def get_stock_value(self):
        if not self._df_share_info.empty:
            # self._stock_value = (self.df_share_info['StockNumber'].mul(self.df_share_info['CurrentPrice'])).sum()
            return self._df_share_info['StockValue'].sum()
        return 0

    # 可用资金
    def get_available_asset(self):
        # available = self._available - self._new_buy_stock_value - self._frozen
        return round(self._available, 2)

    def get_profit_and_loss(self):
        if not self._df_share_info.empty:
            self._profit_and_loss = self._df_share_info['StockProfitAndLost'].sum()
            return round(self._profit_and_loss, 2)
        return 0

    def get_holding_stock(self):
        return self._df_share_info

    def buy(self, stock_code, stock_name, buy_number, buy_price, buy_date, trade_flag='B'):

        self._new_buy_stock_value = round(buy_price * buy_number, 2)
        temp_commission = round(self._new_buy_stock_value * self.commission_rate, 2)

        # 计算佣金, 如果实际佣金金额小于5，那么佣金=5
        buy_commission = self.commission_min if temp_commission < 5 else temp_commission

        if self._new_buy_stock_value + buy_commission > self._available:
            print(f'No enough money to buy {buy_number} number of stock')
            logger.info(f'No enough money to buy {buy_number} number of stock')
            return

        # 计算可用金额
        self._available = self._available - self._new_buy_stock_value - buy_commission

        buy_stock_data = [{
            'StockCode': stock_code,
            'StockName': stock_name,
            'StockValue': self._new_buy_stock_value,
            'StockNumber': buy_number,
            'StockAvailable': buy_number,
            'StockCurrentPrice': buy_price,
            # 'StockCost': buy_price,
            'StockCost': (self._new_buy_stock_value + buy_commission) / buy_number,
            'StockProfitAndLost': 0
        }]

        # 新买股票数据， 放在一个dataframe里面，index设置为-1
        df_new_line = pd.DataFrame(buy_stock_data, columns=stock_info_columns, index=[-1])

        # print(df_new_line)
        if stock_code in self._df_share_info['StockCode'].values:
            # 与现买股票相同的 持股中的index，因为每个股票只能有一条持股信息，所有取list[0]
            stock_index = self._df_share_info[self._df_share_info['StockCode'] == stock_code].index.tolist()[0]

            # 合并前股票值(已有)
            holding_share_value = self._df_share_info.at[stock_index, 'StockValue']
            # 合并前股票盈亏(已有)
            holding_share_profit = self._df_share_info.at[stock_index, 'StockProfitAndLost']

            # 合并后的持股信息
            # 合并后股数=新买股数+已有股数
            self._df_share_info.at[stock_index, 'StockNumber'] += buy_number
            # 合并后的持股市值 = 当前价(新购买股价) * 总股数
            self._df_share_info.at[stock_index, 'StockValue'] = buy_price * self._df_share_info.at[
                stock_index, 'StockNumber']
            # 可用股数=新买股数+已有股数
            self._df_share_info.at[stock_index, 'StockAvailable'] += buy_number
            # 合并后当前股价 = 新购买股价
            self._df_share_info.at[stock_index, 'StockCurrentPrice'] = buy_price
            # 合并后成本 = （合并前股票值(已有) + 新买股票值）/ 合并后股数
            self._df_share_info.at[stock_index, 'StockCost'] = (holding_share_value + self._new_buy_stock_value) / \
                                                               self._df_share_info.at[stock_index, 'StockNumber']
            # 本次买入盈亏 = （当前股价 - 合并后成本）* 合并后股数
            buy_profit_this_time = (buy_price - self._df_share_info.at[stock_index, 'StockCost']) * \
                                   self._df_share_info.at[stock_index, 'StockNumber']
            # 合并后盈亏 = 合并前股票盈亏(已有) + 本次买入盈亏
            self._df_share_info.at[stock_index, 'StockProfitAndLost'] = holding_share_profit + buy_profit_this_time

        else:
            logger.info(msg="Buy share is not in holding share.  Now add to holding share.")
            self._df_share_info = self._df_share_info.append(df_new_line, ignore_index=True)
            self._df_share_info.reset_index()

        # 计算 持仓市值
        self._stock_value = self.get_stock_value()
        # 计算 总资产
        self._total_asset = self._stock_value + self._available

        info = str(buy_date) + ' 买入 ' + stock_code + ' ' + str(int(buy_number)) + '股，股价：' + str(buy_price) + \
               ', 花费：' + str(self._new_buy_stock_value) + ',手续费：' \
               + str(buy_commission) + '，剩余可用现金：' + str(round(self._available, 2)) + \
               ', 目前持仓市值：' + str(self._stock_value)
        print(info)
        logger.info(info)

    def sale(self, stock_code, stock_name, sale_number, sale_price, sale_date, trade_flag='S'):

        # 本次卖出股票值
        value_this_time = sale_price * sale_number
        # 计算佣金, 如果实际佣金金额小于5，那么佣金=5
        temp_commission = round(value_this_time * self.commission_rate, 2)
        sale_commission = self.commission_min if temp_commission < 5 else temp_commission
        stamp_duty = round(value_this_time * self.stamp_duty_rate, 2)

        if stock_code in self._df_share_info['StockCode'].values:
            # 持股中的index，因为每个股票只能有一条持股信息，所有取list[0]
            stock_index = self._df_share_info[self._df_share_info['StockCode'] == stock_code].index.tolist()[0]
            holding_share_value = self._df_share_info.at[stock_index, 'StockValue']
            holding_share_number = self._df_share_info.at[stock_index, 'StockNumber']
            holding_share_profit = self._df_share_info.at[stock_index, 'StockProfitAndLost']
            holding_share_cost = self._df_share_info.at[stock_index, 'StockCost']

            # 卖出股份>持有股份
            if sale_number > holding_share_number:
                logger.error("Sale share number is larger than holding share number.  Operation failed.")
                return
            elif sale_number == holding_share_number:  # 卖出股份==持有股份
                logging.info(msg=f'Sale all share {stock_code}')
                self._df_share_info.drop(index=[stock_index], inplace=True)
                self._df_share_info.reset_index()

                # 计算 持仓市值
                self._stock_value = self.get_stock_value()
                # 计算可用金额
                self._available = self._available + value_this_time - sale_commission - stamp_duty
                # 计算 总资产
                self._total_asset = self._stock_value + self._available

            # 卖出股份<持有股份
            else:
                # 合并后股数 = 已有股数 - 卖出股数
                self._df_share_info.at[stock_index, 'StockNumber'] -= sale_number
                # 合并后的持股市值 = 当前价(卖出股价) * 总股数
                self._df_share_info.at[stock_index, 'StockValue'] = sale_price * self._df_share_info.at[
                    stock_index, 'StockNumber']
                # 可用股数= 已有股数 - 卖出股数
                self._df_share_info.at[stock_index, 'StockAvailable'] -= sale_number
                # 合并后当前股价 = 卖出股价
                self._df_share_info.at[stock_index, 'StockCurrentPrice'] = sale_price
                # 合并前股票总本 = 合并前股票值 - 合并前盈亏
                holding_value_cost = holding_share_value - holding_share_profit
                # 卖出后剩下的总本 = 合并前股票总本 - 这次卖出值
                after_sale_value_cost = holding_value_cost - value_this_time - sale_commission - stamp_duty
                # 合并后成本 = 卖出后剩下的总本/ 合并后股数
                self._df_share_info.at[stock_index, 'StockCost'] = after_sale_value_cost / self._df_share_info.at[
                    stock_index, 'StockNumber']
                # 合并后盈亏 = 合并后的持股市值 - 合并前股票总本
                self._df_share_info.at[stock_index, 'StockProfitAndLost'] = self._df_share_info.at[stock_index, 'StockValue'] - after_sale_value_cost

                # 计算 持仓市值
                self._stock_value = self.get_stock_value()
                # 计算可用金额
                self._available = self._available + value_this_time - sale_commission - stamp_duty
                # 计算 总资产
                self._total_asset = self._stock_value + self._available

            info = str(sale_date) + ' 卖出 ' + stock_code + ' ' + str(int(sale_number)) + '股，股价：' + str(sale_price) + \
                   ', 卖出市值：' + str(value_this_time) + ', 佣金：' + str(sale_commission) + \
                   ', 印花税：' + str(stamp_duty) + '，剩余可用现金：' + str(round(self._available, 2)) + \
                   ', 目前持仓市值：' + str(self._stock_value)
            print(info)
            logger.info(info)

        else:
            logger.error("Sale share is not in holding share.  Operation failed.")
            return
