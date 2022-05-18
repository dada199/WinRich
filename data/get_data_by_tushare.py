from concurrent.futures import ThreadPoolExecutor
from data.tushare_data import get_daily_data
from data.get_data_from_mongo import get_stock_code_sse
from common import contants as ct
import time



st_code = '002903.sz'


def for_threading_get_daily_data(stock_code):
    get_daily_data(st_code=stock_code, start_date=ct.DEFAULT_START_DATE, end_date='', adj='nofq', ma_type=[10, 20, 30])


if __name__ == '__main__':
    time_start = time.time()

    # get_daily_data(st_code=st_code, start_date=ct.DEFAULT_START_DATE, end_date='', adj='nofq', ma_type=[10,20,30])
    code_sse = get_stock_code_sse()
    # ---------- mul-threading to get data via tushare -----------
    with ThreadPoolExecutor(max_workers=5) as pool:
        for value in code_sse['code'][3239:3240]:
            print(value)
            pool.submit(for_threading_get_daily_data, value)


    # ---------- get data via tushare -----------
    # for value in code_sse['code'][500:550]:
    #     print(value)
    #     get_daily_data(st_code=value, start_date=ct.DEFAULT_START_DATE, end_date='', adj='nofq', ma_type=[10, 20, 30])

    time_end = time.time()
    time_sum = time_end - time_start
    print("Get data time %s" % time_sum)



