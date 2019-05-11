from classes.donor import Donor
import logging
from classes.sql_conn import SqlConn
import datetime

class Auth(object):
    """Class for authentication of user:

    Attributes:
        status
        login token
    """


    def __init__(self):
        """Returns an auth object used to save a new user, validate and sign in an existing one or sign out"""
        self.status=False


    def signup_user(self, username, password):
        """Creates new user, returns user object with valid id."""
        # call db to save user - for now list
        # Have to handle the exsiting user scenarios
        try:
            db_obj=SqlConn()
            query="Select * from donor where username = %s"
            data = (username,)
            result=db_obj.get_query(query,data)
            if len(result)>0:
                raise Exception("The username has already been registered, pick another username or try Logging In, instead.")
            else:
                query="Insert into donor (username, password, name, activation_date, account_status) values(%s,%s,%s,%s,%s)"
                data = (username,password,"Donor",datetime.datetime.now(),True,)
                db_obj.set_query(query,data)
                result= db_obj.get_query("Select donor_id from donor where username = %s",(username,))
                uid=result[0][0]
                user = Donor(uid)
                return user, True

        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()




    def signin_user(self, username,password):
        """Login for existing user, returns user object with valid id."""

        try:
            db_obj=SqlConn()
            query="Select * from donor where username = %s and password= %s"
            data = (username,password,)
            result=db_obj.get_query(query,data)
            print(result)
            uid=0
            user=None
            if len(result)>0 and result[0][-3]==1 :
                uid=result[0][0]
                user=Donor(uid)
                print (uid,user)
                self.status=True
            return user, self.status
        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()

    def update_password(self, username,password,new_password):
        """Change credentials for existing user, returns user object with valid id."""
        pass
        # try:
        #     db_obj=SqlConn()
        #     uid, validation_flag=db_obj.check_user(username,password)
        #     if validation_flag:
        #         user=Donor(uid)
        #         self.status=user.set_password(new_password)
        #     return self.status
        # except Exception as e:
        #     logging.info(e)
        #     raise
        # finally:
        #     db_obj.close_conn()

    def reset_password(self, username):
        """Change credentials for existing user, returns user object with valid id."""

        try:
            db_obj=SqlConn()
            query="Select * from donor where username = %s"
            data = (username,)
            result=db_obj.get_query(query,data)
            if len(result)>0:
                #update pwd in db
                #send pwd in mail
                return True
            else:
                raise Exception("Username does not exist")
        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()
