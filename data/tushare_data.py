from tushare.pro.data_pro import pro_bar
from util.setting_path import datafiles_path
import os


def get_daily_data(st_code, start_date='20100101', end_date='', adj=None, ma_type=[20]):
    # pro = ts.set_token('01ab08c0c3788996ec77657694c4a47feafe456ab5d33a3e8db868d5')
    try:
        file_name = st_code.split('.')[0] + '.csv'
        if os.path.exists(os.path.join(datafiles_path, file_name)):
            os.remove(os.path.join(datafiles_path, file_name))

        # pro = ts.pro_api()
        df01 = pro_bar(ts_code=st_code, start_date=start_date, end_date=end_date, asset='E', adj=adj, freq='D',ma=ma_type)
        if not df01.empty:
            print(df01)
            df01.dropna(inplace=True)
            df01.to_csv(os.path.join(datafiles_path, file_name), encoding='utf-8')
            print('Save to csv file successfully.')
        else:
            print('get data failed')

    except Exception as e:
        print(e)





