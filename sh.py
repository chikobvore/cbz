#this script does session management (Session Handler)
import dbh,api,errorlogs
import datetime

def session_status(sender,session_type,status):
    chat = dbh.db['Senders'].find_one({"Sender": sender})
    try:
        dbh.db['Senders'].update({"Sender": sender},
        {
            "Sender": sender,
            "Conversation_ID": chat['Conversation_ID'],
            "Timestamp": datetime.datetime.now(),
            "session_type": session_type,
            "Status": status,
        })
        return True
    except:
        message = "im sorry an error occured whilst trying to log our conversation"
        api.reply_message(sender,message)
        return errorlogs.exception_hander(sender)

def session_date(sender,data):
    dbh.db['session_data'].update({"Sender": sender},
    {
    "Sender": sender,
    "data": data,
    })