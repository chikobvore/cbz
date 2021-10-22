import pymongo
import datetime
import random
import main
import requests
import api
import dbh
import sh
import payments

def addname(sender,response):
    
    record = {
        "Sender": sender,
        "Complainant": response,
        "Address": "",
        "Query_catergory": "",
        "Query_type": "",
        "Query": " "
        }
    dbh.db['Queries'].insert_one(record)
    sh.session_status(sender,session_type='5',status = 'A')

    message =  "*Details successfully saved*\nPlease provide your physical aaddress as follows(stand number/account number(finance related queries),street name,location"
    api.reply_message(sender,message)
    return '', 200


def addaddress(sender,response):

    details = dbh.db['Queries'].find_one({"Sender": sender})

    dbh.db['Queries'].update({"Sender": sender},{
        "Sender": details['Sender'],
        "Complainant": details['Complainant'],
        "Address": response,
        "Query_catergory": "",
        "Query_type": "",
        "Query": " "
            })
    sh.session_status(sender,session_type='5',status = '1')

    message =  "*Query logging*\nPlease select one of the following options 👇\n*1*.Water Queries.\n*2*.Sewer Queries\n*3*.Account/Bill Queries\n*4*.Road Query\n*5*.Health Query\n*6*.Other/General Queries\n*7*.Parking Queries\n*0*.Return to main menu"
    api.reply_message(sender,message)
    return '', 200
