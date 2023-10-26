#this script does session management (Session Handler)
import dbh,api
import datetime

def session_status(sender,session_type,status):
    
    dbh.db['Senders'].update_one({"Sender": sender},
    {
        "$set":{
            "Sender": sender,
            "Timestamp": datetime.datetime.now(),
            "session_type": session_type,
            "Status": status
            }
    })
    return True

def session_date(sender,data):
    dbh.db['session_data'].update_one({"Sender": sender},
    {
        "$set":{
            "Sender": sender,
            "data": data,
        }

    })
    return True