import pymongo
import datetime
import random
import main
import requests
import api
import dbh,sh
import sys

def menu(sender,response):

    state = dbh.db['Senders'].find_one({"Sender": sender})
    sh.session_status(sender,session_type=response,status='0')

    message = "*Account services*\nPlease select one of the following option 👇\n*1*.Inquire balance.\n*2*.Mini-statement\n*3*.Verify account details\n*0*.Return to main menu\n"

    api.reply_message(sender,message)
    return '', 200

def balance(sender,response):

    try:
        existance = dbh.db['account_balances'].find_one({"account_no": response})

        if existance:
            account = existance

            message = "Dear "+ account['account_name'] + ", Your account balance is zwl $" + str(account['balance'])+" ,Please ensure your pay your balances on time to avoid any inconviniences"
            api.reply_message(sender,message)
            return main.feedback(sender)

        else:
            #dbh.db['Senders'].find_one_and_delete({"Sender": sender})  
            message = "The account *"+ response + "* doesnt not exist, please verify your account number before trying again"
            api.reply_message(sender,message)
            return '', 200
    except:
        message = "An error occured whilst trying to retrieve your record, please try again"
        api.reply_message(sender,message)
        return '', 200

def verify_account(sender,response):
    state = dbh.db['Senders'].find_one({"Sender": sender})

    existance = dbh.db['account_balances'].count_documents({"account_no": response})

    if existance > 0:
        record = {
            "Sender": sender,
            "account_no": response 
            }
        dbh.db['temp_account'].insert_one(record)

        account = dbh.db['account_balances'].find_one({"account_no": response})

        message = "Account name: *"+ account['account_name'] + "*,\nAccount number: *" +response+"* \n\nPlease confirm your account details before proceeding\n\n'Yes'.Above mentioned details are a true record of my account details\n'No'.I dont know the stated account details"
        api.reply_message(sender,message)
        return '', 200


    else:
        #dbh.db['Senders'].find_one_and_delete({"Sender": sender})  
        message = "The account *"+ response + "* doesnt not exist\nPlease verify your account number before trying again"
        api.reply_message(sender,message)
        return '', 200

def addemail(sender,response):

    if main.validateemail(email=response):
        try:
            state = dbh.db['Senders'].find_one({"Sender": sender})
            myaccount = dbh.db['temp_account'].find_one({"Sender": sender})
            record = {
                "Sender": sender,
                "account_no": myaccount['account_no'],
                "email": response
                }
            dbh.db['account_updates'].insert_one(record)
 
                
            dbh.db['Senders'].update({"Sender": sender},
            {
                "Sender": sender,
                "Timestamp": state['Timestamp'],
                "session_type": state['session_type'],
                "Status": "2E"
                })

            message = "*Account details successfully saved* ✅,\nPlease provide your *phone number* for communications purposes"
            api.reply_message(sender,message)
            return '', 200

        except:
            message = "An error occured whilst trying to log your message please retry"
            api.reply_message(sender,message)
            return '', 200
    else:
        message = "Please enter a valid email address"
        api.reply_message(sender,message)
        return '', 200

def addphone(sender,response):

    if main.validatephone(phone_number=response):
        try:
            myaccount = dbh.db['account_updates'].find_one({"Sender": sender})
            dbh.db['account_updates'].update({"Sender": sender},
            {
                "Sender": sender,
                "account_no": myaccount['account_no'],
                "email": myaccount['email'],
                "phone": response,
            })


            message = "*Account details successfully saved* ✅,\nGood Bye"
            api.reply_message(sender,message)
            sh.session_status(sender,session_type='0',status='0')
            return '', 200

        except:
            message = "An error occured whilst trying to log your message please retry"
            api.reply_message(sender,message)
            return '', 200
    else:
        message = "Please enter a valid phone number"
        api.reply_message(sender,message)
        return '', 200










