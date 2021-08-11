import pymongo
import datetime
import random
import main
import requests
import api
import dbh
import sh
import payments

def addfullname(response,sender):

    try:
        record = {
                "Sender": sender,
                "Full_name": response,
                "Gender": 'NULL',
                "Age": 'NULL',
                "Nationality": 'NULL'
                }
        dbh.db['budget_reviewers'].insert_one(record)

        sh.session_status(sender,session_type='8',status='1A')

        message = "*Details successfully saved*\nPlease provide us your gender as follows\n*M*.Male\n*F*.Female"
        api.reply_message(sender,message)
        return '', 200
    except:
            message = "*im sorry i didnt get that*Please provide your Full name"
            api.reply_message(sender,message)
            return '', 200

def addgender(response,sender):

    if response == 'M' or response =='m':

        details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
        dbh.db['budget_reviewers'].update({"Sender": sender},{
            "Sender": sender,
            "Full_name": details['Full_name'],
            "Gender": 'Male',
            "Age": 'NULL',
            "Nationality": 'NULL'
            })
        sh.session_status(sender,session_type='8',status='1B')
        message = "*Details successfully saved*\nPlease provide us your age"
        api.reply_message(sender,message)
        return '', 200

    elif response =='F' or response == 'f':

        details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
        dbh.db['budget_reviewers'].update({"Sender": sender},{
            "Sender": sender,
            "Full_name": details['Full_name'],
            "Gender": 'Female',
            "Age": 'NULL',
            "Nationality": 'NULL'
            })
        sh.session_status(sender,session_type='8',status='1B')
        message = "*Details successfully saved*\nPlease provide us your age"
        api.reply_message(sender,message)
        return '', 200

    else:
        message = "*im sorry i didnt get that*Please provide us your gender as follows\n*M*.Male\n*F*.Female"
        api.reply_message(sender,message)
        return '', 200

def addage(response,sender):

    details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
    dbh.db['budget_reviewers'].update({"Sender": sender},{
        "Sender": sender,
        "Full_name": details['Full_name'],
        "Gender": 'Female',
        "Age": response,
        "Nationality": 'NULL'
    })
    sh.session_status(sender,session_type='8',status='1C')
    message = "*Details successfully saved*\nPlease provide us your nationality/citizenship"
    api.reply_message(sender,message)
    return '', 200

def addnation(response,sender):
    details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
    dbh.db['budget_reviewers'].update({"Sender": sender},{
        "Sender": sender,
        "Full_name": details['Full_name'],
        "Gender": details['Gender'],
        "Age": details['Gender'],
        "Nationality": response
    })
    sh.session_status(sender,session_type='8',status='1D')
    message = "*Details successfully saved*\nWhich of the following options apply to you in reference to Mutare City\n*1*.Resident\n*2*.Formal Sector(Business owners,shops,restaurants and etc)\n*3*.Informal sector(Vendor,Hawkers and etc)\n*4*.Institutional(Churches,Schools,and other institutes)\n*5*.Industry(light industry,Heavy industry)"
    api.reply_message(sender,message)
    return '', 200
def addcategory(response,sender):

    try:

        if response == '1':
            category = 'Resident'
        elif response == '2':
            category = 'Formal Sector'
        elif response == '3':
            category = 'Informal Sector'
        elif response == '4':
            category = 'Institutional'
        elif response == '5':
            category = 'Industrial'
        else:
            message = "*I am sorry i didnt get that*\nWhich of the following options apply to you in reference to Mutare City\n*1*.Resident\n*2*.Formal Sector(Business owners,shops,restaurants and etc)\n*3*.Informal sector(Vendor,Hawkers and etc)\n*4*.Institutional(Churches,Schools,and other institutes)\n*5*.Industry(light industry,Heavy industry)"
            api.reply_message(sender,message)
            return '', 200

        details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
        dbh.db['budget_reviewers'].update({"Sender": sender},{
            "Sender": sender,
            "Full_name": details['Full_name'],
            "Gender": details['Gender'],
            "Age": details['Gender'],
            "Catergory": response
        })
        sh.session_status(sender,session_type='8',status='1E')

        message = "*Details successfully saved*\nPlease provide us your account number if it applies,if Not Applicable please respond with N/A"
        api.reply_message(sender,message)
        return '', 200

    except:

        message = "*I am sorry i didnt get that*\nWhich of the following options apply to you in reference to Mutare City\n*1*.Resident\n*2*.Formal Sector(Business owners,shops,restaurants and etc)\n*3*.Informal sector(Vendor,Hawkers and etc)\n*4*.Institutional(Churches,Schools,and other institutes)\n*5*.Industry(light industry,Heavy industry)"
        api.reply_message(sender,message)
        return '', 200

    return '', 200

def addaccount(response,sender):

    details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
    dbh.db['budget_reviewers'].update({"Sender": sender},{
        "Sender": sender,
        "Full_name": details['Full_name'],
        "Gender": details['Gender'],
        "Age": details['Gender'],
        "Catergory": details['Catergory'],
        "Account_no": response
    })
    sh.session_status(sender,session_type='8',status='1F')
    message = "*Details succesfully saved!!*,Please find attached documents"
    api.reply_message(sender,message)
    return senddocuments(sender)

def senddocuments(sender):
    caption = "1.*Performance Report*,\nComments from council about performace report comes here"
    attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20Tarrif%20Schedule.pdf'
    api.send_attachment(sender,attachment_url,caption)

    caption = "2.*Tarrif Schedule*,\nComments from council about *tarrif schedule* comes here"
    attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20performance%20report.pdf'
    api.send_attachment(sender,attachment_url,caption)

    caption = "3.*Proposed projects and funding sources*"
    attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/project%20proposals.pdf'
    api.send_attachment(sender,attachment_url,caption)
    return attachmentmessage(response,sender)

def addcomment(response,sender):

    if response == '1':
        sh.session_status(sender,session_type='8',status='1H')
        message = "*Performance Report*\nDo you have any objection regarding our performance report\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options"
        api.reply_message(sender,message)
        return '', 200

    elif response == '2':
        sh.session_status(sender,session_type='8',status='1H')
        message = "*Tarrif Schedule*\nDo you have any objection regarding our tarrif schedule\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options"
        api.reply_message(sender,message)
        return '', 200

    elif response == '3':
        sh.session_status(sender,session_type='8',status='1H')
        message = "*Proposed projects and funding*\nDo you have any objection regarding our proposed projects and fundings\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options"
        api.reply_message(sender,message)
        return '', 200
    else:
        message = "*I am sorry i didnt get that*\nWhich one of the attached documents do you want to review/comment\n*1*.Performance Report\n*2*.Tarrif Schedule\n*3*.Proposed Projects"
        api.reply_message(sender,message)
        return '', 200

def addobjection(response,sender):
    sh.session_status(sender,session_type='8',status='1I')
    if response == 'Y' or response == 'y':
        message = "*Please specify your objections*"
        api.reply_message(sender,message)
        return '', 200
    elif response == 'N' or response == 'n':
        message = "*What is your overal take on the budget,please comment on the budget*"
        api.reply_message(sender,message)
        return '', 200
        
def objectBudget(response,sender):
    sh.session_status(sender,session_type='8',status='1J')
    message = "*Details successfully have been successfully saved!!*\nHow do you rate this budget out of 10 (0-Very Bad,5-Better,10-Excellent Work)"
    api.reply_message(sender,message)
    return '', 200

def addratings(response,sender):
    
    try:
        if type(response) == int:
            sh.session_status(sender,session_type='8',status='1K')
            message = "*Your rating have been successfully saved!!*\nHow can we make this budget better"
            api.reply_message(sender,message)
            return '', 200
        else:
            message = "*I am sorry i didnt get that*\nHow do you rate this budget out of 10 (0-Very Bad,5-Better,10-Excellent Work)"
            api.reply_message(sender,message)
            return '', 200
    except:
        message = "An error occured whilst trying to log your message,Please provide a valid input"
        api.reply_message(sender,message)
        return '', 200


def addrecommendations(response,sender):
    message = "*Thank you for taking time to review our budget* Your feedback is important to us"
    api.reply_message(sender,message)
    return main.feedback(sender)

def attachmentmessage(response,sender):
    sh.session_status(sender,session_type='8',status='1G')
    message = "*Which one of the attached documents do you want to review/comment*\n\n*1*.Performance Report\n*2*.Tarrif Schedule\n*3*.Proposed Projects"
    api.reply_message(sender,message)
    return '', 200


