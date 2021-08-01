import pymongo
import datetime
import random
import main
import requests
import api
import dbh
import sh
import payments

def addpersonaldetails(response,sender):

    try:
        details = response.split(',')
        record = {
                "Sender": sender,
                "Full_name": details[0],
                "Gender": details[1],
                "Age": details[2],
                "Nationality": details[3]
                }
        dbh.db['budget_reviewers'].insert_one(record)

        sh.session_status(sender,session_type='8',status='1A')

        message = "*Personal details successfully saved*\nPlease provide the following as follows\n(Your area,Your category,your account number(optional))\n*For Example*\nDangamvura Area 13,Resident,12345678\nCBD,Shop License,12345678"
        api.reply_message(sender,message)
        return '', 200
    except:
            message = "*im sorry i didnt get that*Please provide your personal details as follows\n*(Full Name,Gender,Age,Nationality)*\nFor example *John Doe,Male,27,Zimbabwean*"
            api.reply_message(sender,message)
            return '', 200

def addcategory(response,sender):
    try:
        cat_details = response.split(',')

        if cat_details[2]:
            account_no = cat_details[2]
        else:
            account_no = 'Null'

        details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
        dbh.db['budget_reviewers'].update({"Sender": sender},{
            "Sender": sender,
            "Full_name": details['Full_name'],
            "Gender": details['Gender'],
            "Age": details['Age'],
            "Nationality": details['Nationality'],
            "Location": cat_details[0],
            "Status": cat_details[1],
            "Account_no": account_no
            })

        message = "*Details successfully saved*\nPlease find attached documents"
        api.reply_message(sender,message)

        
        caption = "1.*Performance Report*,\nComments from council about performace report comes here\nHow satisfied are you with our performance report,to respond to this question,please reply your message as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n1,8,You are performing very well"
        attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
        api.send_attachment(sender,attachment_url,caption)

        caption = "2.*Tarrif Schedule*,\nComments from council about *tarrif schedule* comes here\nHow satisfied are you with our Tarrif Schedule,to respond to this question,please reply your message as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n2,7,Reasonable tarrifs"
        attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
        api.send_attachment(sender,attachment_url,caption)

        caption = "3.*Proposed projects and funding sources*,\nComments from council about *Proposed projects and funding sources* comes here\nHow satisfied are you with our proposed projects,to respond to this question,please reply your message as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n1,9,well done"
        attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/11.jpg'
        api.send_attachment(sender,attachment_url,caption)

        message = "We value your feedback"
        api.reply_message(sender,message)

        sh.session_status(sender,session_type='8',status='1B')
        return '', 200
    except:
        pass

    return '', 200


