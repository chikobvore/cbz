import pymongo
import requests
import api
import dbh,sh
import re
import datetime

def menu(sender):
    sh.session_status(sender,session_type='0',status='0')  
    message = "Please select one of the following options 👇\n*1*.Waiting List Services 📝\n*2*.Account Services\n*3*.Book an inspection \n*4*.Payment Plan services\n*5*.Log a Query\n*6*.Make a payment\n*7*.Request a call from our customer care representatives\n*8*.Budget Consultation\n*0*.Cancel"
    api.reply_message(sender,message)
    return '', 200

def feedback(sender):
    sh.session_status(sender,session_type='Feedback',status='0')  
    message = "Thank you for using Mutare City Chatbot. We’d love to hear what you think of our service. Your feedback will help us determine what features to add and how we can make the product better for you."
    api.reply_message(sender,message)
    return '', 200

def endchat(sender):
    sh.session_status(sender,session_type='0',status='0')  
    message = "Your feedback is important to us.thank you very much for the valuable feedback.We have forwarded your message to our engineers.\nHave a good day\nRegards Mutare City Council"
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