import MetaTrader5 as mt5
from datetime import datetime
import time
import json
from pymongo import MongoClient
from bson import ObjectId


def connect_to_mongodb():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["stocks"]
    collection = db["stocks_trade"]
    return collection


def read_from_mongodb(account, timestamp=None, type='read', limit=10):
    collection = connect_to_mongodb()
    query = {}
    if account:
        query['account'] = account
    sort_key = 'timestamp'
    if type == 'read':
        if timestamp:
            query['timestamp'] = {'$gte': timestamp.replace(second=0, microsecond=0).timestamp()}

        documents = collection.find(query).limit(limit)
    elif type == 'poll':
        if timestamp:
            query['timestamp'] = timestamp.replace(second=0, microsecond=0).timestamp()

        documents = collection.find(query).limit(limit)
    return documents


def write_to_mongodb(data):
    collection = connect_to_mongodb()
    collection.insert_one(data)

def get_data(account, password,server):
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    
    # connect to the trade account specifying a password and a server
    # login=mt5.login(5015083861, password="slzlug4k",server="MetaQuotes-Demo")
    login=mt5.login(login=account, password=password,server=server)
    if login:
        account_info=mt5.account_info()
        if account_info!=None:
            # print(account_info)
            data={
                'timestamp':datetime.now().replace(second=0, microsecond=0).timestamp(),
                'account':account_info.login,
                'balance':account_info.balance,
                'equity':account_info.equity,
                'profit':account_info.profit                
            }
            return data
    else:
        print(f"failed to connect to trade account {account}",mt5.last_error())
    
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()

if __name__ == "__main__":  
    while True: 
        data=get_data(account=5015389644, password="8nnhjwyi",server="MetaQuotes-Demo")
# data=get_data(account=5015083861, password="slzlug4k",server="MetaQuotes-Demo")
        # print('data:',data)
        write_to_mongodb(data)
        time.sleep(30)
        