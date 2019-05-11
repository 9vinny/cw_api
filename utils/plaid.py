import plaid
from classes.donor import Donor
import datetime;
from classes.sql_conn import SqlConn
import logging
import json
from classes.plaid_transaction import PlaidTransaction

PLAID_CLIENT_ID = '5cb0ce482db15200120fb445'
PLAID_SECRET = '4c61d2dfdff1021b50b7cd146bcf9a'
PLAID_PUBLIC_KEY = '0cfea3b8cf3611b374aecb1a215a39'
PLAID_ENV =  'development'
PLAID_PRODUCTS = 'transactions,auth'


print(PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY, PLAID_ENV, PLAID_PRODUCTS)

client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                      public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV, api_version='2018-05-22')



def get_access_token(uid,public_token):
    """get access token from Plaid api and save to DB"""
    try:
        exchange_response = client.Item.public_token.exchange(public_token)
        access_token = exchange_response['access_token']
        item = exchange_response['item_id']
        current_user = Donor(uid)
        # current_user.set_access_token(item,access_token)
        return current_user.set_access_token(item,access_token)
        logging.info(e)
    except plaid.errors.PlaidError as e:
        logging.info(e)
        raise

def get_transactions_from_plaid():
    """pull daily transactions"""
    start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-1))
    end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now()+ datetime.timedelta(-1))
    try:
        db_obj=SqlConn()
        query="Select donor_id,plaid_access_token,plaid_item_id from donor where account_status = %s \
        and plaid_access_token is not NULL"
        data=(True,)
        result=db_obj.get_query(query,data)
        transactions={}
        if len(result)==0:
            return "no plaid linked users"
        for row in result:
            # user_id,access_token,item_id=result[0]:
            transactions_response = client.Transactions.get(row[1], start_date, end_date)
            # transactions.append((user_id,transactions_response["transactions"]))
            for transaction in transactions_response["transactions"]:
                pt_obj=PlaidTransaction(
                    row[0],
                    transaction["name"],
                    transaction["amount"],
                    transaction["date"],
                    transaction["location"]["city"],
                    transaction["transaction_id"],
                    transaction["transaction_type"],
                    transaction["account_id"],
                    transaction["account_owner"]
                )
                pt_obj.save_tran()
                transactions[row[0]]=transactions_response["transactions"]
                # print("whts that",transaction)
            for row in result:
                donor_obj=Donor(row[0])
                donor_obj.set_month_total()

        return transactions
                # return True,transactions_response
    except Exception as e:
        logging.info(e)
        raise
