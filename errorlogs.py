import pymongo
import requests
import api
import dbh,main

def invalid(sender,response):

    state = dbh.db['Senders'].find_one({"Sender": sender})
    dbh.db['Senders'].update({"Sender": sender},
    {
        "Sender": sender,
        "Timestamp": state['Timestamp'],
        "Session_type": 0,
        "Status": "0",
        })

    message = "Waiting List services,\nPlease select one of the following option 👇 \n *1*. Join Waiting List*📝. \n *2*.Renew waiting list 📝\n *3*. View Status \n *0*.Return to main menu\n *"
    api.reply_message(sender,message)
    return '', 200

def exception_hander(sender):
    message = "Im sorry 😔, an error occured whilst i was trying to log our conversation.lets start afresh our conversation."
    api.reply_message(sender,message)
    return '', 200
 