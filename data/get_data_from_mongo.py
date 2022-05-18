from pymongo import MongoClient
import pandas as pd
import os
import logging

from util.setting_path import cache_path
from common.exception_handle import GetDateError


logger = logging.getLogger(__name__)


def _connection_db(host, port, username, pwd, db):
    if username and pwd:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, pwd, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, pwd=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connection_db(host=host, port=port, username=username, pwd=pwd, db=db)

    # Make a query to the specific DB and Collection, excluded the column _id
    cursor = db[collection].find(query, {'_id': 0})

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # Delete the _id
    # if no_id:
    #     del df["_id"]
    #
    return df


def get_stock_code_sse():
    """Get stock code from C:\\Users\\xxx\\.winrich\\cache if file exists, or query from mongodb"""
    stock_list_file = os.path.join(cache_path, 'stock_list.csv')
    if not os.path.exists(stock_list_file):
        df = read_mongo(db='quantaxis', collection='stock_list')
        df['code'] = df[['code', 'sse']].apply(lambda x: '.'.join(x), axis=1)

        df2 = df[['code', 'name', 'sse']]

        df2.to_csv(stock_list_file, encoding='utf-8-sig')
        print(f'File {stock_list_file} doest exist, query from mongodb and save to csv.')

    else:
        df = pd.read_csv(stock_list_file, encoding='utf-8-sig')
        print(f'File {stock_list_file} is existing. get code from it.')

    return df


def get_stock_xdxr(stock_code: str):
    """Get stock xdxr info from \\.winrich\\cache if file exists, or query from mongodb"""
    f_name = stock_code + '_xdxr.csv'
    full_xdxr_file = os.path.join(cache_path, f_name)
    if not os.path.exists(full_xdxr_file):
        query = dict()
        query.update({"code": stock_code})
        query.update({"songzhuangu": {r'$gt': 0}})

        df = read_mongo(db='quantaxis', collection='stock_xdxr', query=query)
        # df['code'] = df[['code', 'sse']].apply(lambda x: '.'.join(x), axis=1)
        #
        # df2 = df[['code', 'name', 'sse']]

        df.to_csv(full_xdxr_file, encoding='utf-8-sig')
        print(f'File {full_xdxr_file} doest exist, query from mongodb and save to csv.')

    else:
        df = pd.read_csv(full_xdxr_file, encoding='utf-8-sig')
        print(f'File {full_xdxr_file} is existing. get code from it.')

    return df


if __name__ == '__main__':
    df = get_stock_xdxr("002019")
    print(df)




