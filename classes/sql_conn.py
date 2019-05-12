import MySQLdb
import datetime


class SqlConn(object):
    """Class to connect with MYSQL db"""

    def __init__(self):
        """Class to connect with MYSQL db"""

        # self.db = MySQLdb.connect("charitywallet.ckjkftdengvx.us-west-1.rds.amazonaws.com", "root", "capstone", "charity_wallet")
        self.db = MySQLdb.connect("localhost", "root", "capstone", "charity_wallet")
        self.cursor = self.db.cursor()


    def close_conn(self):
        """Closes DB connection"""
        self.db.close()

    def set_query(self,query,data):
        """Saves user profile details"""
        self.cursor.execute(query,data)
        self.db.commit()


    def get_query(self,query,data):
        """Saves user profile details"""
        if data is not None:
            self.cursor.execute(query,data)
            result = self.cursor.fetchall()
        else:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        return result

    # def user_exists(self,username):
    #     query="Select * from donor where username = %s"
    #     data = (username,)
    #     result=self.get_query(query,data)
    #     if len(result)>0:
    #         return True
    #     return False

    # def create_user(self,username,password):
    #     query="Insert into donor (username, password, name, activation_date, account_status) values(%s,%s,%s,%s,%s)"
    #     data = (username,password,"Donor",datetime.datetime.now(),True,)
    #     self.set_query(query,data)
    #     result= self.get_query("Select donor_id from donor where username = %s",(username,))
    #
    #     return result[0][0]

    # def check_user(self,username,password):
    #     query="Select * from donor where username = %s and password= %s"
    #     data = (username,password,)
    #     result=self.get_query(query,data)
    #     uid=0
    #     print(result)
    #     if len(result)>0 and result[0][-1]==1 :
    #         uid=result[0][0]
    #         return uid,True
    #     return uid, False


# +---[RSA 2048]----+
# | o*Bo.  .        |
# | +*==.+o o       |
# |..+ooB+.+.       |
# |+o .+++++        |
# |+o. +o.=S        |
# |E. ... +.        |
# |.      o+.       |
# |      . ...      |
# |         .o.     |
# +----[SHA256]-----+
