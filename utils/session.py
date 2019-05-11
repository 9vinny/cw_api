user_session={}
import datetime


def start_session(uid,timestamp):
    """starts session"""
    global user_session
    print("ss",uid,timestamp)
    user_session[uid]={"start":timestamp, "active":True,"end":""}
    print(user_session)


def check_session(uid):
    """check active session"""
    global user_session
    # if (datetime.datetime.now()- user_session[uid]["start"])> 30:
    if uid in user_session.keys():
        duration=datetime.datetime.now()- user_session[uid]["start"]
        duration_in_min=divmod(duration.total_seconds(), 60)[0]
        if duration_in_min>30:
            end_session(uid,datetime.datetime.now())
            return False
        else:
            start_session(uid,datetime.datetime.now())
            return True
    else:
        return False



def end_session(uid,timestamp):
    """end active session"""
    global user_session
    user_session[uid]["active"]=False
    user_session[uid]["end"]=timestamp
    print(user_session)
