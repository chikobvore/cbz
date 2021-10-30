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
        "Gender": details['Gender'],
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
        "Age": details['Age'],
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
            "Nationality": details['Nationality'],
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
        "Nationality": details['Nationality'],
        "Account_no": response
    })
    sh.session_status(sender,session_type='8',status='1F')
    message = "*Details succesfully saved!!*,Please find attached documents"
    api.reply_message(sender,message)
    return senddocuments(sender)

def sendnationaldocuments(sender):

    caption = "SAMPLE 2022 GOVERNMENT ALLOCATION GRANT ALLOCATION REPORT AND PROPOSED PROJECTS"
    attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20Tarrif%20Schedule.pdf'
    api.send_attachment(sender,attachment_url,caption)
    return nationalattachmentmessage(sender)

def senddocuments(sender):

    caption = "2021 HALF YEAR BUDGET PERFORMANCE REPORT"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/2021%20HALF%20YEAR%20BUDGET%20PERFORMANCE%20REPORT-.docx'
    api.send_attachment(sender,attachment_url,caption)

    caption = "2022 PROPOSED TARRIF SCHEDULE"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/2022%20Budget%20Tariff%20working%20papers%20edited.xlsx'
    api.send_attachment(sender,attachment_url,caption)

    caption = "2022 PROPOSED PROJECTS AND CAPEX"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/2022%20CAPEX%20%26%20PROJECTS.xlsx'
    api.send_attachment(sender,attachment_url,caption)

    caption = "WATER TARRIF MODEL"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/water%20tariff%20study%20Mutare%20Model.xlsx'
    api.send_attachment(sender,attachment_url,caption)
    
    # caption = "RENTALS VALUATION REPORT"
    # attachment_url = 'https://github.com/chikobvore/Unlock-Technologies/raw/master/lib/RENTALS%20%20VALUATION%20REPORT.xls'
    # api.send_attachment(sender,attachment_url,caption)

    # caption = "MUTARE HEAVY INDUSTRY VALUATION REPORT"
    # attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/RENTALS%20VALUATION%20REPORT.xls'
    # api.send_attachment(sender,attachment_url,caption)

    # caption = "MUTARE HEAVY INDUSTRY VALUATION REPORT"
    # attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/RENTALS%20VALUATION%20REPORT.xls'
    # api.send_attachment(sender,attachment_url,caption)

    return attachmentmessage(sender)


def addcomment(response,sender):

    if response == '1':
        budget_type = "Performance Report"
        record = {
            "Sender": sender,
            "Budget_type": budget_type,
            "Objection": 'NULL',
            "Comment": 'NULL',
            "Rating": 'NULL',
            "Recommendations": 'NULL',
            "Status": "PENDING"
            }
        dbh.db['pending_budget_reviews'].insert_one(record)

        sh.session_status(sender,session_type='8',status='1H')
        message = "*PERFORMANCE REPORT*\nWhat is your comment regarding our performance"
        api.reply_message(sender,message)
        return '', 200

    elif response == '2':

        budget_type = "Tarrif Schedule"
        record = {
            "Sender": sender,
            "Budget_type": budget_type,
            "Objection": 'NULL',
            "Comment": 'NULL',
            "Rating": 'NULL',
            "Recommendations": 'NULL',
            "Status": "PENDING"
            }
        dbh.db['pending_budget_reviews'].insert_one(record)

        sh.session_status(sender,session_type='8',status='1H')
        message = "*TARRIF SCHEDULE*\nDo you have any objection regarding our tarrif schedule\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options *_NB ANSWERS SHOULD ONLY BE Y for Yes or N for No_*"
        api.reply_message(sender,message)
        return '', 200

    elif response == '3':

        budget_type = "Proposed Projects"
        record = {
            "Sender": sender,
            "Budget_type": budget_type,
            "Objection": 'NULL',
            "Comment": 'NULL',
            "Rating": 'NULL',
            "Recommendations": 'NULL',
            "Status": "PENDING"
            }
        dbh.db['pending_budget_reviews'].insert_one(record)

        sh.session_status(sender,session_type='8',status='1H')
        message = "*PROPOSED PROJECTS AND CAPEX*\nDo you have any objection regarding our proposed projects and capex\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options  *_NB ANSWERS SHOULD ONLY BE Y for Yes or N for No_*"
        api.reply_message(sender,message)
        return '', 200

    elif response == '4':

        budget_type = "water tarrif"
        record = {
            "Sender": sender,
            "Budget_type": budget_type,
            "Objection": 'NULL',
            "Comment": 'NULL',
            "Rating": 'NULL',
            "Recommendations": 'NULL',
            "Status": "PENDING"
            }
        dbh.db['pending_budget_reviews'].insert_one(record)

        sh.session_status(sender,session_type='8',status='1H')
        message = "*WATER TARRIF MODEL*\nDo you have any objection regarding our water tarrif model\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options  *_NB ANSWERS SHOULD ONLY BE Y for Yes or N for No_*"
        api.reply_message(sender,message)
        return '', 200
    else:
        message = "*I am sorry i didnt get that*\nWhich one of the attached documents do you want to review/comment\n*1*.Performance Report\n*2*.Proposed 2022 budget"
        api.reply_message(sender,message)
        return '', 200

def addobjection(response,sender):
    sh.session_status(sender,session_type='8',status='1I')
    if response == 'Y' or response == 'y':
        details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
        dbh.db['pending_budget_reviews'].update({"Sender": sender},{
            "Sender": sender,
            "Budget_type": details['Budget_type'],
            "Objection": 'YES',
            "Comment": 'NULL',
            "Rating": 'NULL',
            "Recommendations": 'NULL',
            "Status": "PENDING"
        })

        message = "*Please specify your objections*"
        api.reply_message(sender,message)
        return '', 200
    elif response == 'N' or response == 'n':
        
        details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
        dbh.db['pending_budget_reviews'].update({"Sender": sender},{
            "Sender": sender,
            "Budget_type": details['Budget_type'],
            "Objection": 'NO',
            "Comment": 'NULL',
            "Rating": 'NULL',
            "Recommendations": 'NULL',
            "Status": "PENDING"
        })
        message = "*What is your overal take on the budget,please comment on the budget*"
        api.reply_message(sender,message)
        return '', 200

    else:
        details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
        dbh.db['pending_budget_reviews'].update({"Sender": sender},{
            "Sender": sender,
            "Budget_type": details['Budget_type'],
            "Objection": 'NO',
            "Comment": 'NULL',
            "Rating": 'NULL',
            "Recommendations": 'NULL',
            "Status": "PENDING"
        })
        message = "*What is your overal take on the budget,please comment on the budget*"
        api.reply_message(sender,message)
        return '', 200

        
def objectBudget(response,sender):
    sh.session_status(sender,session_type='8',status='1J')

    details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
    dbh.db['pending_budget_reviews'].update({"Sender": sender},{
        "Sender": sender,
        "Budget_type": details['Budget_type'],
        "Objection": details['Objection'],
        "Comment": response,
        "Rating": 'NULL',
        "Recommendations": 'NULL',
        "Status": "PENDING"
    })
    message = "*Details successfully have been successfully saved!!*\nHow do you rate this budget out of 10\n*0* -Very Bad\n*5* -Better\n*10* -Excellent Work"
    api.reply_message(sender,message)
    return '', 200

def addratings(response,sender):
    
    try:
        rating = int(response)
        if type(rating) == int:
            if rating > 10 or rating < 0:
                message = "*Invalid input*\nPlease provide your rating in form of number\n*0* -Very Bad\n*5* -Better\n*10* -Excellent Work"
                api.reply_message(sender,message)
                return '', 200
            else:

                details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
                dbh.db['pending_budget_reviews'].update({"Sender": sender},{
                    "Sender": sender,
                    "Budget_type": details['Budget_type'],
                    "Objection": details['Objection'],
                    "Comment": details['Comment'],
                    "Rating": rating,
                    "Recommendations": 'NULL',
                    "Status": "PENDING"
                })
                sh.session_status(sender,session_type='8',status='1K')
                message = "*Your rating have been successfully saved!!*\nHow can we make this budget better,please tell us your recommendations"
                api.reply_message(sender,message)
                return '', 200
        else:
            message = "*Invalid input*\nPlease provide your rating in form of number\n*0* -Very Bad\n*5* -Better\n*10* -Excellent Work"
            api.reply_message(sender,message)
            return '', 200
    except:
        message = "An error occured whilst trying to log your message,Please provide a valid input"
        api.reply_message(sender,message)
        return '', 200


def addrecommendations(response,sender):

    details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
    dbh.db['pending_budget_reviews'].update({"Sender": sender},{
        "Sender": sender,
        "Budget_type": details['Budget_type'],
        "Objection": details['Objection'],
        "Comment": details['Comment'],
        "Rating": details['Rating'],
        "Recommendations": response,
        "Status": "PENDING"
    })

    details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
    sender_details = dbh.db['budget_reviewers'].find_one({"Sender": sender})
    
    record = {
            "Sender": sender,
            "Sender_catergory": sender_details['Catergory'],
            "Sender_gender": sender_details['Gender'],
            "Budget_type": details['Budget_type'],
            "Objection": details['Objection'],
            "Comment": details['Comment'],
            "Rating": details['Rating'],
            "Recommendations": details['Recommendations'],
            "Timestamp": datetime.datetime.now(),
            }
    dbh.db['budget_reviews'].insert_one(record)
    dbh.db['pending_budget_reviews'].find_one_and_delete({'Sender': sender})

    message = "*Thank you for taking time to review our budget* Your feedback is important to us"
    api.reply_message(sender,message)
    return main.feedback(sender)

def attachmentmessage(sender):

    sh.session_status(sender,session_type='8',status='1G')
    message = "*Which one of the attached documents do you want to review/comment*\n\n*1*.2021 HALF YEAR PERFORMANCE REPORT\n*2*.PROPOSED 2022 TARRIF SCHEDULE\n*3*.2022 PROPOSED PROJECTS AND CAPEX\n*4*.2022 WATER TARRIF MODEL\n\n _Please select one of the above options(response should either be 1,2,3 or 4)_"
    api.reply_message(sender,message)
    return '', 200

def welcomeback(response,sender):

    if response == '1':
        return resend_performance_report(sender)
    elif response == '2':
        resend_proposed_projects_report(sender)
    elif response == '3':
        return attachmentmessage(sender)  
    elif response == '4':
        return senddocuments(sender)
    elif response == '0':
        return main.menu(sender)
    else:
        message = "I am sorry, i didnt get that"
        api.reply_message(sender,message)
        return '', 200

def resend_performance_report(sender):

    caption = "2022 PROPOSED PROJECTS AND CAPEX"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/2022%20CAPEX%20%26%20PROJECTS.xlsx'
    api.send_attachment(sender,attachment_url,caption)
    return addcomment('1',sender)

def resend_tarrif_schedule(sender):

    caption = "2022 PROPOSED TARRIF SCHEDULE"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/2022%20Budget%20Tariff%20working%20papers%20edited.xlsx'
    api.send_attachment(sender,attachment_url,caption)
    return addcomment('2',sender)

def resend_proposed_projects_report(sender):

    caption = "2022 PROPOSED PROJECTS AND CAPEX"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/2022%20CAPEX%20%26%20PROJECTS.xlsx'
    api.send_attachment(sender,attachment_url,caption)
    return addcomment('3',sender)



