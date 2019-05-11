from classes.donor import Donor
import logging
from classes.sql_conn import SqlConn
import datetime
import math

class PlaidTransaction(object):
    """Class for authentication of user:

    Attributes:
        status
        login token
    """


    def __init__(self,uid, name, amount, date, city, transaction_id, transaction_type, account_id, account_owner):
        """Returns a plaid transaction obj"""
        self.transaction_id=0
        self.donor_id=uid
        self.name=name,
        self.amount=amount,
        self.date=date,
        self.city=city,
        self.transaction_id=transaction_id,
        self.transaction_type=transaction_type,
        self.account_id=account_id,
        self.account_owner=account_owner


    def save_tran(self):
        """Creates new user, returns user object with valid id."""
        # call db to save user - for now list
        # Have to handle the exsiting user scenarios
        try:
            db_obj=SqlConn()
            query="Insert into plaid_transaction (donor_id,plaid_transaction_name,entry_date, \
            plaid_transaction_amt,plaid_transaction_date,plaid_transaction_city,\
            plaid_transaction_id, plaid_transaction_type,plaid_account_id,plaid_account_owner,\
            donation_amt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (self.donor_id,self.name,datetime.datetime.now(),
            self.amount, self.date, self.city, self.transaction_id,
            self.transaction_type, self.account_id, self.account_owner,self.calc_change(),)
            db_obj.set_query(query,data)
            # return True;
        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()

    def calc_change(self):
        print(self.amount[0])
        change_amt=math.ceil(self.amount[0])-self.amount[0]
        if change_amt<0.5:
            return change_amt
        else:
            return self.amount[0]-math.floor(self.amount[0])





    # def signin_user(self, username,password):
    #     """Login for existing user, returns user object with valid id."""
    #
    #     try:
    #         db_obj=SqlConn()
    #         query="Select * from donor where username = %s and password= %s"
    #         data = (username,password,)
    #         result=db_obj.get_query(query,data)
    #         print(result)
    #         uid=0
    #         user=None
    #         if len(result)>0 and result[0][-3]==1 :
    #             uid=result[0][0]
    #             user=Donor(uid)
    #             print (uid,user)
    #             self.status=True
    #         return user, self.status
    #     except Exception as e:
    #         logging.info(e)
    #         raise
    #     finally:
    #         db_obj.close_conn()



    # def reset_password(self, username):
    #     """Change credentials for existing user, returns user object with valid id."""
    #
    #     try:
    #         db_obj=SqlConn()
    #         query="Select * from donor where username = %s"
    #         data = (username,)
    #         result=db_obj.get_query(query,data)
    #         if len(result)>0:
    #             #update pwd in db
    #             #send pwd in mail
    #             return True
    #         else:
    #             raise Exception("Username does not exist")
    #     except Exception as e:
    #         logging.info(e)
    #         raise
    #     finally:
    #         db_obj.close_conn()
