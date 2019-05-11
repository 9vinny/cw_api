import datetime;
from classes.sql_conn import SqlConn
import logging

class Donor(object):
    """Donor class. Donors have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        username: app login username
        password: app login password
        monthly balance: A float tracking the current balance of the change accumulated self month.
        location: A string representing the customer's name.
    """

    def __init__(self,uid=""):
        """Return a Donor object """

        self.name = "Donor"
        self.uid=uid
        self.fav_causes =[]
        self.username=""
        self.password=""
        self.lifetime_donation=0
        self.monthly_collected=0
        self.causes=[]
        print("donor constructor")
        self.sync_from_db()

    def sync_from_db(self):
        """Fetches user profile details"""
        pass

    def sync_to_db(self):
        pass

    def set_profile(self, name, fav_causes):
        """Saves user profile details"""
        self.name =name
        self.last_logged_in = datetime.datetime.now()
        self.fav_causes =fav_causes

        try:
            db_obj=SqlConn()

        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()

    def get_profile(self, name, fav_causes):
        pass



    def get_id(self):
        """Fetches user id"""
        print("get_id",self.uid)
        return self.uid

    def get_user_totals(self):
        print("in user tots")
        try:
            db_obj=SqlConn()

            query="Select lifetime_donation, monthly_collected  from donor \
            where donor_id = %s"
            data = (int(self.uid),)
            result = db_obj.get_query(query,data)

            query="Select count(distinct drive_id), \
            count(distinct charity_id) from donor_drive \
             where donor_id = %s"

            result2 = db_obj.get_query(query,data)

            return {'user_id':self.uid,'month_total':result[0][1],'lifetime_total':result[0][0],'active_drives':result2[0][0],'active_charities':result2[0][1]}


        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()




    def set_access_token(self, item_id, access_token):
        #update in obj and save to db

        try:
            db_obj=SqlConn()
            query="Update donor set plaid_item_id= %s, plaid_access_token=%s, last_logged_in=%s,\
            donation_cycle_start_date=%s where donor_id = %s"
            data = (item_id,access_token, datetime.datetime.now(), datetime.datetime.now(),self.uid,)
            db_obj.set_query(query,data)
            self.plaid_item=item_id
            self.plaid_access_token=access_token
            return True

        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()

    def set_month_total(self):
        #update in obj and save to db
        try:
            db_obj=SqlConn()
            query1="Select donation_cycle_start_date from donor where \
            donor_id=%s"
            data1 = (self.uid,)
            result1=db_obj.get_query(query1,data1)
            # print(datetime.datetime(cycle_start[0]))
            # print(cycle_start[0],)
            cycle_start=result1[0][0]
            if cycle_start > datetime.datetime.now().replace(day=1):
                donation_start=(cycle_start+ datetime.timedelta(-1)).replace(hour=0,minute=0, second=0)
            else:
                donation_start=datetime.datetime.now().replace(day=1).replace(hour=0,minute=0, second=0)

            query2="Select sum(donation_amt) from plaid_transaction where \
            donor_id=%s and plaid_transaction_date between %s and %s"
            data2 = (self.uid,donation_start,datetime.datetime.now()+datetime.timedelta(-1),)
            month_total=db_obj.get_query(query2,data2)
            print(data2,month_total)

            if month_total is None:
                month_total=0.0

            query3="Update donor set monthly_collected = %s where \
            donor_id=%s"
            data3 = (month_total,self.uid,)
            db_obj.set_query(query3,data3)
            # return True

        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()


    def select_drive(self,drive_id,charity_id):
        print("sel drive")
        try:
            db_obj=SqlConn()
            query="Insert into donor_drive values(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE \
            status=IF(status, 0, 1)"
            data = (drive_id,self.uid,charity_id, datetime.datetime.now(),True,)
            db_obj.set_query(query,data)
            return "Drive Toggle Sel/Unsel successful"
        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()
