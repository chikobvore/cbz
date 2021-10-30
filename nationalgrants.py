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

        sh.session_status(sender,session_type='10',status='1A')

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
        sh.session_status(sender,session_type='10',status='1B')
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
        sh.session_status(sender,session_type='10',status='1B')
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
    sh.session_status(sender,session_type='10',status='1C')
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
    sh.session_status(sender,session_type='10',status='1D')
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
        sh.session_status(sender,session_type='10',status='1E')

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
    sh.session_status(sender,session_type='10',status='1F')
    message = "*Details succesfully saved!!*,Please find attached documents"
    api.reply_message(sender,message)
    return sendnationaldocuments(sender)

def sendnationaldocuments(sender):

    caption = "2022 DEVOLUTION FUNDS ALLOCATIONS AND PROPOSED PROJECTS"
    attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/Proposed%20Devolution%20funded%20projects.docx'
    api.send_attachment(sender,attachment_url,caption)
    return nationalattachmentmessage(sender)

def nationalattachmentmessage(sender):
    
    sh.session_status(sender,session_type='10',status='1G')
    message = "Review 2022 DEVOLUTION FUNDS ALLOCATIONS AND PROPOSED PROJECTS herein. Press 1 to continue and review or press 0 to return to main menu"
    api.reply_message(sender,message)
    return '', 200


def addnationlcomment(response,sender):

    if response == '1':
        budget_type = "PROPOSED PROJECTS"
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

        sh.session_status(sender,session_type='10',status='1H')
        message = "*2022 DEVOLUTION FUNDS ALLOCATIONS AND PROPOSED PROJECTS*\nWhat is your preferred devolution project"
        api.reply_message(sender,message)
        return '', 200

    elif response == '0':
        return main.menu(sender)

    # elif response == '2':

    #     budget_type = "Tarrif Schedule"
    #     record = {
    #         "Sender": sender,
    #         "Budget_type": budget_type,
    #         "Objection": 'NULL',
    #         "Comment": 'NULL',
    #         "Rating": 'NULL',
    #         "Recommendations": 'NULL',
    #         "Status": "PENDING"
    #         }
    #     dbh.db['pending_budget_reviews'].insert_one(record)

    #     sh.session_status(sender,session_type='8',status='1H')
    #     message = "*PROPOSED 2022 BUDGET*\nDo you have any objection regarding our proposed budget\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options"
    #     api.reply_message(sender,message)
    #     return '', 200

    # elif response == '3':

    #     budget_type = "Proposed Projects"
    #     record = {
    #         "Sender": sender,
    #         "Budget_type": budget_type,
    #         "Objection": 'NULL',
    #         "Comment": 'NULL',
    #         "Rating": 'NULL',
    #         "Recommendations": 'NULL',
    #         "Status": "PENDING"
    #         }
    #     dbh.db['pending_budget_reviews'].insert_one(record)

    #     sh.session_status(sender,session_type='8',status='1H')
    #     message = "*Proposed projects and funding*\nDo you have any objection regarding our proposed projects and fundings\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options"
    #     api.reply_message(sender,message)
    #     return '', 200
    else:
        message = "*I am sorry i didnt get that*\nWhich one of the attached documents do you want to review/comment\n*1*.Proposed projects"
        api.reply_message(sender,message)
        return '', 200


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

        sh.session_status(sender,session_type='10',status='1H')
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

        sh.session_status(sender,session_type='10',status='1H')
        message = "*PROPOSED 2022 BUDGET*\nDo you have any objection regarding our proposed budget\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options"
        api.reply_message(sender,message)
        return '', 200

    # elif response == '3':

    #     budget_type = "Proposed Projects"
    #     record = {
    #         "Sender": sender,
    #         "Budget_type": budget_type,
    #         "Objection": 'NULL',
    #         "Comment": 'NULL',
    #         "Rating": 'NULL',
    #         "Recommendations": 'NULL',
    #         "Status": "PENDING"
    #         }
    #     dbh.db['pending_budget_reviews'].insert_one(record)

    #     sh.session_status(sender,session_type='8',status='1H')
    #     message = "*Proposed projects and funding*\nDo you have any objection regarding our proposed projects and fundings\n*Y*.Yes\n*N*.No\n\nPlease respond with one of the above options"
    #     api.reply_message(sender,message)
    #     return '', 200
    else:
        message = "*I am sorry i didnt get that*\nWhich one of the attached documents do you want to review/comment\n*1*.Performance Report\n*2*.Proposed 2022 budget"
        api.reply_message(sender,message)
        return '', 200

def addobjection(response,sender):
    sh.session_status(sender,session_type='10',status='1I')

    details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
    dbh.db['pending_budget_reviews'].update({"Sender": sender},{
        "Sender": sender,
        "Budget_type": details['Budget_type'],
        "Prefered": response,
        "Objection": 'NO',
        "Comment": 'NULL',
        "Rating": 'NULL',
        "Recommendations": 'NULL',
        "Status": "PENDING"
    })

    message = "*2022 DEVOLUTION FUNDS ALLOCATIONS AND PROPOSED PROJECTS*\n\n_Where do you want devolution project to be located_"
    api.reply_message(sender,message)
    return '', 200

def objectBudget(response,sender):
    sh.session_status(sender,session_type='10',status='1J')

    details = dbh.db['pending_budget_reviews'].find_one({"Sender": sender})
    dbh.db['pending_budget_reviews'].update({"Sender": sender},{
        "Sender": sender,
        "Budget_type": details['Budget_type'],
        "Objection": details['Objection'],
        "Prefered": details['Prefered'],
        "Location": response,
        "Comment": '',
        "Rating": 'NULL',
        "Recommendations": 'NULL',
        "Status": "PENDING"
    })
    message = "*Details successfully have been successfully saved!!*\nDo you have any other suggestion on devolution  funded projects"
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
                sh.session_status(sender,session_type='10',status='1K')
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
        "Prefered": details['Prefered'],
        "Location": details['Location'],
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
            "Prefered": details['Prefered'],
            "Location": details['Location'],
            "Recommendations": details['Recommendations'],
            "Timestamp": datetime.datetime.now(),
            }
    dbh.db['budget_reviews'].insert_one(record)
    dbh.db['pending_budget_reviews'].find_one_and_delete({'Sender': sender})

    message = "*Thank you for taking time to review our budget* Your feedback is important to us"
    api.reply_message(sender,message)
    return main.feedback(sender)

def attachmentmessage(sender):

    sh.session_status(sender,session_type='10',status='1G')
    message = "*Which one of the attached documents do you want to review/comment*\n\n*1*.PERFORMANCE REPORT\n*2*.PROPOSED 2022 BUDGET"
    api.reply_message(sender,message)
    return '', 200

def welcomeback(response,sender):

    if response == '1':
        return sendnationaldocuments(sender)
    elif response == '2':
        return nationalattachmentmessage(sender)
    else:
        message = "I am sorry, i didnt get that"
        api.reply_message(sender,message)
        return '', 200

def resend_performance_report(sender):

    caption = "PERFORMANCE REPORT"
    attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20Tarrif%20Schedule.pdf'
    #attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/BUDGET%20PERFORMANCE%20REVIEW%202021.pdf'
    api.send_attachment(sender,attachment_url,caption)
    return addcomment('1',sender)

def resend_tarrif_schedule(sender):
    
    caption = "SUPPLIMENTARY BUDGET AND PROPOSED 2022 BUDGET"
    attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20performance%20report.pdf'
    #attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/SUPPLEMENTARY%20BUDGET%20AND%202022%20BUDGET%20PROPOSAL.pdf'
    api.send_attachment(sender,attachment_url,caption)
    return addcomment('2',sender)

def resend_proposed_projects_report(sender):

    caption = "SUPPLIMENTARY BUDGET AND PROPOSED 2022 BUDGET"
    attachment_url = 'https://chikobvore.github.io/dura_online_shop/images/Sample%20performance%20report.pdf'
    #attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/lib/SUPPLEMENTARY%20BUDGET%20AND%202022%20BUDGET%20PROPOSAL.pdf'
    api.send_attachment(sender,attachment_url,caption)
    return addcomment('3',sender)



