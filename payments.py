import pymongo
import datetime
import random
import main
import requests
from paynow import Paynow
import api
import dbh
import sh
import pandas as pd

def pay(sender,response):

    state = dbh.db['Senders'].find_one({"Sender": sender})
    sh.session_status(sender,session_type=response,status='0')
    message =  "*Make Payment*\nPlease select your payment method👇 \n *1*.Ecocash. \n *2*.Telecash\n *3*.One Money\n\n*0*.Cancel"
    api.reply_message(sender,message)
    return '', 200

def addphone(sender,response):

    state = dbh.db['Senders'].find_one({"Sender": sender})
    sh.session_status(sender,state['session_type'],status='6B')
    details = dbh.db['pending_payments'].find_one({"Sender": sender})

    dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": response,
                "email": '',
                "amount": "",
                "Purpose": "",
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

    message =  "*Make Payment*\nPlease provide your email address"
    api.reply_message(sender,message)
    return '', 200

def addemail(sender,response):

    if main.validateemail(email=response):

        state = dbh.db['Senders'].find_one({"Sender": sender})
        sh.session_status(sender,state['session_type'],status='6C')
        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": details['pay_number'],
                "email": response,
                "amount": "",
                "Purpose": "",
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

        message =  "*Make Payment*\nPlease enter amount"
        api.reply_message(sender,message)
        return '', 200

    else:
        message =  "Please enter a valid email address"
        api.reply_message(sender,message)
        return '', 200

def addamount(sender,response):

    state = dbh.db['Senders'].find_one({"Sender": sender})
    sh.session_status(sender,session_type=state['session_type'],status='6D')

    details = dbh.db['pending_payments'].find_one({"Sender": sender})
    dbh.db['pending_payments'].update({"Sender": sender},
    {
            "Sender": sender,
            "account": "",
            "reference_no": details['reference_no'],
            "pay_number": details['pay_number'],
            "email": details['email'],
            "amount": response,
            "Purpose": "",
            "Payment_method": details['Payment_method'],
            "Date_paid": datetime.datetime.now()
        })

    message =  "*Make Payment*\nPlease select your payment reason \n *1*.Pay Rates. \n *2*.Payment Plan\n *3*.Inspection Booking\n *4*. Waiting List\n*0*.Cancel"
    api.reply_message(sender,message)
    return '', 200

def addpurpose(sender,response):

    state = dbh.db['Senders'].find_one({"Sender": sender})
    sh.session_status(sender,session_type=state['session_type'],status='6E')

    if response == '1':
        purpose = 'Rates Payment'
        code = '0011'
        
        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": details['pay_number'],
                "email": details['email'],
                "amount": details['amount'],
                "Purpose": purpose,
                "Service code": code,
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

        message =  "*Make Payment*\nPlease enter your *account number*"
        api.reply_message(sender,message)
        return '', 200

    elif response == '2':
        purpose = 'Payment Plan'
        code = '0012'

        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": details['pay_number'],
                "email": details['email'],
                "amount": details['amount'],
                "Purpose": purpose,
                "Service code": code,
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

        message =  "*Make Payment*\nPlease provide  your *Payment Plan number/account number*"
        api.reply_message(sender,message)
        return '', 200

    elif response == '3':
        purpose = 'Inspection Fee'
        code = '0013'

        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": details['pay_number'],
                "email": details['email'],
                "amount": details['amount'],
                "Purpose": purpose,
                "Service code": code,
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

        message =  "*Make Payment*\nPlease enter your *account number*"
        api.reply_message(sender,message)
        return '', 200
    elif response == '4':
        purpose = 'Waiting List Fee'
        code = '0014'

        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": details['pay_number'],
                "email": details['email'],
                "amount": details['amount'],
                "Purpose": purpose,
                "Service code": code,
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

        existance = dbh.db['waiting_list'].count_documents({"contact": sender})
        if existance > 0:
            sh.session_status(sender,session_type=state['session_type'],status='6E')
            Applicant = dbh.db['waiting_list'].find_one({"contact": sender})

            message =   "*Waiting List Status*\n Applicant Name: "+ Applicant['full_name'] +"\nNational ID: " + Applicant['national_id'] + "\nDate of Birth: "+ Applicant['dob'] + "\nPhysical address: "+ Applicant['physical_address'] + "\nMarital Status: "+ Applicant['marital_status']+'\n*1*.Proceed to Pay\n*2*.Cancel'
            api.reply_message(sender,message)
            return '', 200

        else:

            message =   "You dont have a pending application"
            api.reply_message(sender,message)
            return '',200

        message =  "*Make Payment*\nPlease enter your *account number*"
        api.reply_message(sender,message)
        return '', 200
    elif response == '5':
        purpose = 'Parking Fee'
        code = '0015'

        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": details['pay_number'],
                "email": details['email'],
                "amount": details['amount'],
                "Purpose": purpose,
                "Service code": code,
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

        message =  "*Make Payment*\nPlease enter your *account number*"
        api.reply_message(sender,message)
        return '', 200

    else:
        purpose = 'Other Fee'
        code = '0016'

        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        dbh.db['pending_payments'].update({"Sender": sender},
        {
                "Sender": sender,
                "account": "",
                "reference_no": details['reference_no'],
                "pay_number": details['pay_number'],
                "email": details['email'],
                "amount": details['amount'],
                "Purpose": purpose,
                "Service code": code,
                "Payment_method": details['Payment_method'],
                "Date_paid": datetime.datetime.now()
            })

        message =  "*Make Payment*\nPlease enter your *account number*"
        api.reply_message(sender,message)
        return '', 200


def confirm(sender,response):



    state = dbh.db['Senders'].find_one({"Sender": sender})
    details = dbh.db['pending_payments'].find_one({"Sender": sender})
    

    if details['Purpose'] == 'Waiting List Fee':
        if response == '1':
            dbh.db['pending_payments'].update({"Sender": sender},
            {
                    "Sender": sender,
                    "account": "",
                    "reference_no": details['reference_no'],
                    "pay_number": details['pay_number'],
                    "email": details['email'],
                    "amount": "1938.47",
                    "Purpose": details['Purpose'],
                    "Service code": details['Service code'],
                    "Payment_method": details['Payment_method'],
                    "Date_paid": datetime.datetime.now()
                })
            Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
            details = dbh.db['pending_payments'].find_one({"Sender": sender})
            sh.session_status(sender,session_type=state['session_type'],status='6F')
                    
            message = "*Confirm Payment*\n\nPlease confirm details below\n*Applicant*: "+ Applicant['full_name'] +"\n*Reference*: "+ str(Applicant['waiting_list_no'])+"\n*Phone No*: "+ str(details['pay_number']) + "\n*Email*: "+  details['email'] + "\n*Amount*: "+  details['amount']+  "\n\nPress 1 to continue or 0 to cancel"
            api.reply_message(sender,message)
            return '', 200

        else:
            message = "Transaction cancelled 😔"
            api.reply_message(sender,message)
            return main.menu(sender)

    elif details['Purpose'] == 'Rates Payment':

        existance = dbh.db['account_balances'].count_documents({"account_no": response})

        if existance > 0:
            sh.session_status(sender,session_type=state['session_type'],status='6F')
            dbh.db['pending_payments'].update({"Sender": sender},
            {
                    "Sender": sender,
                    "account": response,
                    "reference_no": details['reference_no'],
                    "pay_number": details['pay_number'],
                    "email": details['email'],
                    "amount": details['amount'],
                    "Purpose": details['Purpose'],
                    "Service code": details['Service code'],
                    "Payment_method": details['Payment_method'],
                    "Date_paid": datetime.datetime.now()
                })
            account = dbh.db['account_balances'].find_one({"account_no": response}) 
            details = dbh.db['pending_payments'].find_one({"Sender": sender})

            message = "*Confirm Payment*\n\nPlease confirm details below\n*Account name*: "+ account['account_name'] +"\n*Account number*: "+account['account_no']+"\n*Phone No*: "+ details['pay_number'] + "\n*Email*: "+  details['email'] + "\n*Amount*: "+  details['amount']+  "\n\nPress 1 to continue or 0 to cancel"
            api.reply_message(sender,message)
            return '', 200

        else:
            #dbh.db['Senders'].find_one_and_delete({"Sender": sender})  
            message = "The account *"+ response + "* doesnt not exist\nPlease verify your account number before trying again"
            api.reply_message(sender,message)
            return '', 200


def makepayment(sender,response):

    if response == '0':
        dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
        message = "Transaction cancelled 😔"
        api.reply_message(sender,message)
        return main.menu(sender)

    details = dbh.db['pending_payments'].find_one({"Sender": sender})
    paynow = Paynow(9415,'3d7f4aed-ab06-42f5-b155-0e12e41fc714','https://tauraikatsekera.herokuapp.com/chatbot/payments', 'https://tauraikatsekera.herokuapp.com/chatbot/payments')
    #paynow = Paynow(10724,'31008a64-6945-43d6-aed2-000961c04d5a','https://tauraikatsekera.herokuapp.com/chatbot/payments', 'https://tauraikatsekera.herokuapp.com/chatbot/payments')
    payment = paynow.create_payment(details['reference_no'], details['email'])
    
    payment.add(details['Purpose'], details['amount'])
    response = paynow.send_mobile(payment, details['pay_number'], details['Payment_method'])


    if(response.success):
        poll_url = response.poll_url
        print("Poll Url: ", poll_url)
        # Get the poll url (used to check the status of a transaction). You might want to save this in your DB
        r=requests.get(poll_url)
        actualResponse = r.text
        
        tr = actualResponse.split("&")
    
        diction = {}
        
        for string in tr:
            values = string.split("=")
            print(values)
            diction[values[0]] = values[1]

        #get date
        mytime = str(pd.to_datetime('now'))
        mydate = mytime.split(' ')
        mydate[0]


        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
        if details['Purpose'] == 'Waiting List Fee':
            dbh.db['waiting_list'].update({"contact": sender},{
                "full_name": Applicant['full_name'],
                "gender": Applicant['gender'],
                "national_id": Applicant['national_id'],
                "dob": Applicant['dob'],
                "nationality": "N/A",
                "region": "N/A",
                "city": "N/A",
                "physical_address": Applicant['physical_address'],
                "marital_status": Applicant['marital_status'],
                "contact": sender,
                "email": Applicant['email'],
                "disablity": "N/A",
                "yor": "N/A",
                "waiting_list_no": Applicant['waiting_list_no'],
                "profile": "N/A",
                "stand_type": Applicant['stand_type'],
                "status": "PAID",
                "created_at": Applicant['created_at'],
                "updated_at": datetime.datetime.now()
            })
        
        record = {
            "Sender": sender,
            "account": details['account'],
            "reference_no": details['reference_no'],
            "paynow_ref": diction['paynowreference'],
            "pay_number": details['pay_number'],
            "email": details['email'],
            "amount": details['amount'],
            "Purpose": details['Purpose'],
            "Service_code": details['Service code'],
            "Status": "PAID",
            "Date_paid": mydate[0]
            }
        dbh.db['payments'].insert_one(record)
        dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})

        message = "*Payment Confirmation*\n*Reference number*: "+diction['paynowreference']+ "\n\n*Please note that the money will reflect in your account after next end-of-day settlement.*\n\nTo view the transaction online please follow this link\n"+poll_url
        api.reply_message(sender,message)
        return main.feedback(sender)

    else:
        details = dbh.db['pending_payments'].find_one({"Sender": sender})
        record = {
            "Sender": sender,
            "account": details['account'],
            "reference_no": details['reference_no'],
            "paynow_ref": '--',
            "pay_number": details['pay_number'],
            "email": details['email'],
            "amount": details['amount'],
            "Purpose": details['Purpose'],
            "Service_code": details['Service code'],
            "Status": "FAILED",
            "Date_paid": datetime.datetime.now()
            }
        dbh.db['payments'].insert_one(record)
        dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
        message = "Transaction Failed"
        api.reply_message(sender,message)
        return main.feedback(sender)