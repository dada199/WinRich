import pandas as pd
from data.daily_data import DataAPI
from account.account_info import Account
from strategy.stragegy import Strategy

csv_file = '600999.csv'



if __name__ == '__main__':
    data_api = DataAPI()
    data_api.get_df_data_from_cvs(csv_file)

    account = Account()
    account.transfer = 100000.00

    strategy = Strategy(account, data_api)

    strategy.ma20_strategy()

    df_holding_stock_info = strategy.strategy_get_account()

    print(df_holding_stock_info.to_string())

    print(account.get_available_asset())
    print(account.get_total_asset())
    print(account.get_profit_and_loss())




