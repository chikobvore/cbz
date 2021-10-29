import pymongo
import requests
import api
import dbh,sh
import re
import datetime

def menu(sender):
    
    sh.session_status(sender,session_type='0',status='0')  
    dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
    dbh.db['pending_budget_reviews'].find_one_and_delete({'Sender': sender})
    dbh.db['Queries'].find_one_and_delete({'Sender': sender})
    message = "Please select one of the following options 👇\n\n"+ str('1️⃣') +" *Budget Consultations (Own Revenue)*\n\n"+ str('2️⃣') +" *Budget Consultations (Government Grants)*\n\n"+ str('3️⃣') +" Account Services\n\n" + str('4️⃣') +" Log a Query\n\n"+ str('5️⃣') +" Make Payment\n\n" + str('6️⃣')+ " Waiting List Services\n\n"+ str('7️⃣')+ " Request a call from our customer care representatives\n\n"+ str('8️⃣')+" Payment Plan Services\n\n"+str('9️⃣')+" Compliment our good works\n\n"+ str('0️⃣')+" Cancel \n*Please select the corresponding number for the type of service you wish to access or Done to return to this menu*"
    api.reply_message(sender,message)
    return '', 200

def feedback(sender):
    sh.session_status(sender,session_type='Feedback',status='0')  
    message = "Thank you for using Mutare City Chatbot. We’d love to hear what you think of our service. Your feedback will help us determine what features to add and how we can make the product better for you."
    api.reply_message(sender,message)
    return '', 200

def endchat(sender):
    sh.session_status(sender,session_type='0',status='0')  
    message = "Your feedback is important to us.thank you very much for the valuable feedback.We have forwarded your message to our engineers.\nHave a good day\nUnited together, we shall make Mutare a great city again\n\nRegards Mutare City Council"
    api.reply_message(sender,message)
    return '', 200


def validatephone(phone_number):
    if len(phone_number) <= 9:
        return False

    if phone_number.isdigit():
        return True
    else:
        return False

    return True 

def validateemail(email):
    if(re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", email) != None):
        return True
    else:
        return False

    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    # if(re.search(regex,email)):  
    #     return True
          
    # else:  
    #     return False

def validatedate(sender,date_string):
    format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(date_string, format)
        return True

    except ValueError:
        # message = "This is the incorrect date string format. It should be YYYY-MM-DD"
        # api.reply_message(sender,message)
        return False