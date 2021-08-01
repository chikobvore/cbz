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

        
        caption = "1.*Performance Report*,\nComments from council about performace report comes here\n\nHow satisfied are you with our performance report,to respond to this question,please reply your message as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n1,8,You are performing very well"
        attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20Tarrif%20Schedule.pdf'
        api.send_attachment(sender,attachment_url,caption)

        caption = "2.*Tarrif Schedule*,\nComments from council about *tarrif schedule* comes here\n\nHow satisfied are you with our Tarrif Schedule,to respond to this question,please reply your message as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n2,7,Reasonable tarrifs"
        attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20performance%20report.pdf'
        api.send_attachment(sender,attachment_url,caption)

        caption = "3.*Proposed projects and funding sources*,\nComments from council about *Proposed projects and funding sources* comes here\n\nHow satisfied are you with our proposed projects,to respond to this question,please reply your message as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n1,9,well done"
        attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/project%20proposals.pdf'
        api.send_attachment(sender,attachment_url,caption)

        sh.session_status(sender,session_type='8',status='1B')

        message = "Thank you for reviewing our budget,if you are done juss type *Done* to save your views"
        api.reply_message(sender,message)
        return '', 200
    except:
        
        message = "Please provide the following as follows\n(Your area,Your category,your account number(optional))\n*For Example*\nDangamvura Area 13,Resident,12345678\nCBD,Shop License,12345678"
        api.reply_message(sender,message)
        return '', 200

    return '', 200

def addcomment(response,sender):

    try:
        details = response.split(',')

        record = {
            "Sender": sender,
            "Review": details[0],
            "Objection": details[1],
            "Comment": details[2],
            }
        dbh.db['budget_reviews'].insert_one(record)
        
        message = "*Details successfully saved*\nTo continue reviewing please reply as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n1,9,well done"
        api.reply_message(sender,message)
        return '', 200

    except:
        message = "please reply your message as follows\n(1,rating out of 10 (1-very poor,5-moderate,10-excellent),Your comments)\n*For Example*\n1,9,well done"
        api.reply_message(sender,message)
        return '', 200

        
