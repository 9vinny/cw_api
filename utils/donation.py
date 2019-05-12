from classes.sql_conn import SqlConn
import logging

def calculate_donor_month_total():
    """calculate and save donor's accumulated change amount"""
    pass


def make_donations():
    """make donations for users who have selected drives"""
    #get user_id and amts for active donors
    #make donation entry
    #reset donation cycle date as curr date, update accumulated amount zer, update ltd amount
    pass



    # charities=[]
    # try:
    #     db_obj=SqlConn()
    #     if uid==0:
    #         #get all charities
    #         print("all")
    #         query="Select * from charity"
    #         data=None
    #     else:
    #         query="Select * from charity where charity_id \
    #         in (Select distinct charity_id from donor_drive \
    #         where donor_id=%s and status = %s)"
    #         data = (uid,True,)
    #
    #     result=db_obj.get_query(query,data)
    #     if len(result)>0:
    #         print("db queried")
    #         for record in result:
    #             print(record)
    #             result2=db_obj.get_query(query,data)
    #             r={'charity_id':record[0],'charityName':record[1],
    #             'charityAbout': record[2],
    #             'charityImageURL':record[3],
    #             'charityAddress':record[4],
    #             'charityCity':record[5],
    #             'charityState':record[6],
    #             'charityActiveDrives':record[11],
    #             'charityCauses':record[12].split(",")
    #             }
    #             charities.append(r)
    #     else:
    #         raise Exception("No charities found")
    #     return charities
    # except Exception as e:
    #     logging.info(e)
    #     raise
    # finally:
    #     db_obj.close_conn()
