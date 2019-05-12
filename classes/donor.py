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

    def set_name(self, name, fav_causes):
        """Saves user profile details"""
        self.name=name
        try:
            db_obj=SqlConn()

        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()

    def get_name(self, name, fav_causes):
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

            query2="Select count(distinct drive_id), \
            count(distinct charity_id) from donor_drive \
             where donor_id = %s and status=%s"
            data2 = (int(self.uid),True,)
            result2 = db_obj.get_query(query2,data2)

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
            query="Update donor set plaid_item_id= %s, plaid_access_token=%s, \
            donation_cycle_start_date=%s where donor_id = %s"
            data = (item_id,access_token, datetime.datetime.now(), self.uid,)
            db_obj.set_query(query,data)
            self.plaid_item=item_id
            self.plaid_access_token=access_token
            return True

        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()

    def set_causes(self, causes):
        #update in obj and save to db
        try:
            db_obj=SqlConn()
            query="Update donor set fav_causes= %s where donor_id = %s"
            data = (','.join([str(x) for x in causes]),self.uid,)
            print(data)
            db_obj.set_query(query,data)
            self.fav_causes=causes
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

    def make_donation(self,amount=0):
        try:
            db_obj=SqlConn()
            if amount == 0:
                query="Select monthly_collected from donor where donor_id = %s"
                data=(self.uid,)
                result1=db_obj.get_query(query,data)

                query2= "Select distinct drive_id,charity_id from donor_drive where donor_id=%s and status=%s"
                data2=(self.uid,True,)
                result2=db_obj.get_query(query2,data2)

                print(result1[0][0])
                print(result2, len(result2))

                if len(result2)>0:

                    donation_amt_per_drive = result1[0][0]/len(result2)

                    for drive in result2:
                        query3= "Insert into donation (donor_id, drive_id,charity_id, donation_date, donation_amt, donation_type)\
                         values(%s,%s,%s,%s,%s,%s)"
                        data3=(self.uid,drive[0],drive[1],datetime.datetime.now(),donation_amt_per_drive,"OTD",)
                        print(query3, data3)
                        db_obj.set_query(query3,data3)

                    query4= "Update donor set monthly_collected = %s, donation_cycle_start_date =%s, \
                     lifetime_donation=lifetime_donation+%s where donor_id=%s"
                    data4=(0,datetime.datetime.now(),result1[0][0],self.uid,)
                    db_obj.set_query(query4,data4)
                    print(query4, data4)
                    return True, "Donation Successfull"
                else:
                    return False, "No selected drive"

            else:
                # return False, "Donation amount needs to be greater than 0"
                query2= "Select distinct drive_id,charity_id from donor_drive where donor_id=%s and status=%s"
                data2=(self.uid,True,)
                result2=db_obj.get_query(query2,data2)

                print("why",query2,data2)
                print("Drive ids",result2, len(result2))

                if len(result2)>0:

                    donation_amt_per_drive = float(amount)/len(result2)

                    for drive in result2:
                        query3= "Insert into donation (donor_id, drive_id,charity_id, donation_date, donation_amt, donation_type)\
                         values(%s,%s,%s,%s,%s,%s)"
                        data3=(self.uid,drive[0],drive[1],datetime.datetime.now(),donation_amt_per_drive,"OTD",)
                        print(query3, data3)
                        db_obj.set_query(query3,data3)

                    query4= "Update donor set monthly_collected = %s, donation_cycle_start_date =%s, \
                     lifetime_donation=lifetime_donation+%s where donor_id=%s"
                    data4=(0,datetime.datetime.now(),float(amount),self.uid,)
                    db_obj.set_query(query4,data4)
                    print(query4, data4)
                    return True, "Donation Successfull"
                else:
                    return False, "No selected drive"

        except Exception as e:
            logging.info(e)
            raise
        finally:
            db_obj.close_conn()
