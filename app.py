from datetime import date,datetime
import pymongo
from flask import Flask, redirect, render_template, request, session, url_for
import datetime,requests
from pymongo import message
import waiting_list,account_services,payments,main,budget,nationalgrants
import sh,api,queries
import sys,os,random
from paynow import Paynow


#Import the machine learning modules
import text2emotion as te

# client = messagebird.Client('QQRgKx3QvpSV6SpEVewDvWJGK', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANdbh.dbOX])
# # Enable conversations API whatsapp sandbox# client = messagebird.Client('1ekjMs368KTRlP0z6zfG9P70z', #features = [messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])

#-*- mode: python -*-
# -*- coding: utf-8 -*-

app = Flask(__name__)
app.secret_key = 'LADS-AFRICA'

try:
    import dbh
except:
    message = "PREVIOUS SESSION EXPIRED DUE TO POOR NETWORK CONNECTION"
    print(message)
    render_template('login.htm',message = message)


@app.route('/api',methods=["post"])
def chatmenu():

    payload = request.get_json()
    sender = payload['messages'][0]['author'].split('@')[0]

    senderName = payload['messages'][0]['senderName']
    message_id = payload['messages'][0]['id']
    response = payload['messages'][0]['body']
    
    if sender == '263771067779':
        return '', 200

    # if sender == '263716897966':
    #     return '', 200

    if response == 'Done' or response == 'done':
        return main.menu(sender)

    existance = dbh.db['Senders'].count_documents({"Sender": sender}) 

    #check if session exist
    if existance < 1:
        #create new session
        record = {
            "Sender": sender,
            "Timestamp": datetime.datetime.now(),
            "session_type": "0",
            "Status": "0"
            }
        dbh.db['Senders'].insert_one(record)
        # -*- coding: utf-8 -*-
        caption = "Hello "+ senderName +" 🙋🏽‍♂ , \nThank you for contacting Mutare City Council,I'm Tau, i'm a virtual assistant,\nFor any emergency 👇 \n📞 Dial Number: +263202060823 \n\nPlease select one of the following options 👇\n\n"+ str('1️⃣') +" *Budget Consultations (Own Revenue)*\n\n"+ str('2️⃣') +" *Budget Consultations (Government Grants)*\n\n"+ str('3️⃣') +" Account Services\n\n" + str('4️⃣') +" Log a Query\n\n"+ str('5️⃣') +" Make Payment\n\n" + str('6️⃣')+ " Waiting List Services\n\n"+ str('7️⃣')+ " Request a call from our customer care representatives\n\n"+ str('8️⃣')+" Payment Plan Services\n\n"+str('9️⃣')+" Compliment our good works\n\n"+ str('0️⃣')+" Cancel \n*Please select the corresponding number for the type of service you wish to access or Done to return to this menu*"
        attachment_url = 'https://www.mutarecity.co.zw/images/mutarelogo.png'
        api.send_attachment(sender,attachment_url,caption)
        return '', 200

    else:
        response = response
        state = dbh.db['Senders'].find_one({"Sender": sender})

        date2 = datetime.datetime.now()
        date1 = state['Timestamp']

        time_delta = (date2 - date1)

        total_seconds = time_delta.total_seconds()

        minutes = total_seconds/60
        if minutes > 10:
            sh.session_status(sender,'0','0')
            dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
            dbh.db['pending_budget_reviews'].find_one_and_delete({'Sender': sender})
            dbh.db['Queries'].find_one_and_delete({'Sender': sender})
            message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options 👇\n\n"+ str('1️⃣') +" *Budget Consultations (Own Revenue)*\n\n"+ str('2️⃣') +" *Budget Consultations (Government Grants)*\n\n"+ str('3️⃣') +" Account Services\n\n" + str('4️⃣') +" Log a Query\n\n"+ str('5️⃣') +" Make Payment\n\n" + str('6️⃣')+ " Waiting List Services\n\n"+ str('7️⃣')+ " Request a call from our customer care representatives\n\n"+ str('8️⃣')+" Payment Plan Services\n\n"+str('9️⃣')+" Compliment our good works\n\n"+ str('0️⃣')+" Cancel \n*Please select the corresponding number for the type of service you wish to access or Done to return to this menu*"
            api.reply_message(sender,message)
            return '', 200

        if state['session_type'] == "0":
            
            if response == "1":

                #budget consultations own revenue
                existance = dbh.db['budget_reviewers'].count_documents({"Sender": sender}) 
                #check if session exist
                if existance < 1:
                    sh.session_status(sender,session_type='8',status='0')
                    message = "*Budget consultations*\nThank you for reaching us, we value your feedback and support.\nFor the purposes of quality evaluation please provide your full name"
                    api.reply_message(sender,message)
                    return '', 200
                else:
                    sh.session_status(sender,session_type='8',status='1L')
                    message = "*Welcome Back* "+ sender +"\nPlease select one of the following options\n*1*.Resend Performance Report\n*2*.Resend Proposed budget\n*3*.Continue reviewing\n*4*.Resend all attachments\n*0.Return to main menu*"
                    api.reply_message(sender,message)
                    return '', 200

            elif response == "2":
                #budget consultations government grants

                existance = dbh.db['budget_reviewers'].count_documents({"Sender": sender}) 
                if existance < 1:
                    sh.session_status(sender,session_type='10',status='0')
                    message = "*Budget consultations*\nThank you for reaching us, we value your feedback and support.\nFor the purposes of quality evaluation please provide your full name"
                    api.reply_message(sender,message)
                    return '', 200
                else:
                    sh.session_status(sender,session_type='10',status='1L')
                    message = "*Welcome Back* "+ sender +"\nPlease select one of the following options\n*1*.RESEND 2022 DEVOLUTION FUNDS ALLOCATIONS AND PROPOSED PROJECTS\n*2*.Continue reviewing\n*0*. Return to main menu\n*_NB RESPONSE SHOULD EITHER BE 1 , 2 OR 0_*"
                    api.reply_message(sender,message)
                    return '', 200

                
            elif response == "3":

                return account_services.menu(sender,response)

            elif response == "4":
                #query logging
                sh.session_status(sender,session_type='5',status='0')
                message= "*Query logging*\nOur sincere apologies for the bad experiene with us, for the purposes of quality evaluation please provide us your full name"
                api.reply_message(sender,message)
                return '', 200

            elif response == "5":
                #make payments
                return payments.pay(sender,response)

            elif response == "6":
                #waiting list services
                return waiting_list.waiting_list_menu(sender,response)
                
            elif response == "7":

                sh.session_status(sender,session_type=response,status='1')

                message = "Our customer services representatives are currently occupied, please leave your message an agent ll assist you in the nearest possible time"
                api.reply_message(sender,message)
                return '', 200

            elif response == "8":

                message= "*Payment Plan Services*\nThis service is under maintainance, kindly bear with us"
                api.reply_message(sender,message)
                return main.menu(sender)
            elif response == '9':
                
                sh.session_status(sender,session_type='Feedback',status='Feedback')
                message = "*Compliments*\nThank you for reaching us, we value your feedback and support.\nPlease briefly tell us your compliments"
                api.reply_message(sender,message)
                return '', 200
            
            elif response == "0":
                return main.menu(sender)
            else:
                sh.session_status(sender,'0','0')
                dbh.db['pending_payments'].find_one_and_delete({'Sender': sender})
                dbh.db['pending_budget_reviews'].find_one_and_delete({'Sender': sender})
                dbh.db['Queries'].find_one_and_delete({'Sender': sender})
                message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options 👇\n\n"+ str('1️⃣') +" *Budget Consultations (Own Revenue)*\n\n"+ str('2️⃣') +" *Budget Consultations (Government Grants)*\n\n"+ str('3️⃣') +" Account Services\n\n" + str('4️⃣') +" Log a Query\n\n"+ str('5️⃣') +" Make Payment\n\n" + str('6️⃣')+ " Waiting List Services\n\n"+ str('7️⃣')+ " Request a call from our customer care representatives\n\n"+ str('8️⃣')+" Payment Plan Services\n\n"+str('9️⃣')+" Compliment our good works\n\n"+ str('0️⃣')+" Cancel \n*Please select the corresponding number for the type of service you wish to access or Done to return to this menu*"
                api.reply_message(sender,message)
                return '', 200



        elif state['session_type'] == "1":

            if state['Status'] == '0':
                if response == "1":
                    sh.session_status(sender,state['session_type'],'terms')
                    message = "*Terms and Conditions* \nplease read our terms and conditions carefully before proceeding\n*1*.The applicant undertakes to comply with council's terms of offer of stand.Failure to do so will result in the applicant being disqualified.\n*2*.Applicant should renew his application during the month of january every year.Failure to do so will result in applicant being removed from the waiting list.\n\n*Yes*.I have read, understood and accepted the terms and conditions of joining the waiting list.\n*No*.I dont agree with the stated terms and conditions of joing waiting list."
                    api.reply_message(sender,message)
                    return '', 200

                elif response == "2":

                    message = "*This feature is not yet working*"
                    api.reply_message(sender,message)
                    return '', 200

                elif response == "3":
                    return waiting_list.preview(sender)
                elif response == "0":
                    return main.menu(sender)
            else:
                if state['Status'] == "terms":
                    return waiting_list.terms(sender,response)
                if state['Status'] == "1A":
                    return waiting_list.addname(sender,response,state)
                elif state['Status'] == "1B":
                    return waiting_list.add_nationalid(sender,response,state)
                elif state['Status'] == "1C":
                    return waiting_list.adddob(sender,response,state)
                elif state['Status'] == "1D":
                    return waiting_list.addmarital(sender,response,state)
                elif state['Status'] == "1E":
                    return waiting_list.addgender(sender,response,state)
                elif state['Status'] == "1F":
                    return waiting_list.addspouse(sender,response,state)
                elif state['Status'] == "1G":
                    return waiting_list.addemail(sender,response,state)
                elif state['Status'] == "1H":
                    return waiting_list.addaddress(sender,response,state)
                elif state['Status'] == "1PA":
                    return waiting_list.addnature(sender,response,state)
                elif state['Status'] == "1PB":
                    return waiting_list.addarea(sender,response,state)
                elif state['Status'] == "1PD":
                    return waiting_list.addcat(sender,response,state)
                elif state['Status'] == "1PE":
                    return waiting_list.addtype(sender,response,state)
                elif state['Status'] == "Confirm":
                    return waiting_list.confirm(sender,response,state)
                elif state['Status'] == "Complete":
                    return waiting_list.complete(sender,response,state)    
                elif state['Status'] == "PaymentMethod":
                    return waiting_list.paylist(sender,response,state)
                elif state['Status'] == "PaymentAccount":
                    return waiting_list.addnumber(sender,response)       
                elif state['Status'] == "completepayment":
                    return waiting_list.completetransaction(sender,response)    
                else:
                    message = "*Invalid response*"
                    api.reply_message(sender,message)
                    return '', 200

        elif state['session_type'] == "2":

            if response == "1":

                sh.session_status(sender,state['session_type'],'2A')
                message = "*Balance Inquiry* \nPlease enter your account number"
                api.reply_message(sender,message)
                return '', 200

            elif response == "2":
                message = "*This feature is not yet working*"
                api.reply_message(sender,message)
                return main.menu(sender)

            elif response == "3":

                sh.session_status(sender,state['session_type'],'2B')
                message = "*Verify account details* \nPlease enter your account number"
                api.reply_message(sender,message)
                return '', 200

            elif response == "Yes" or response == 'yes' or response == 'Yes':
                sh.session_status(sender,session_type=state['session_type'],status='2D')
                message = "*Please provide your email address*"
                api.reply_message(sender,message)
                return '', 200

            elif response == "No" or response == 'no':
                return account_services.menu(sender,2)

            elif response == "0":
                return main.menu(sender)
            else:
                if state['Status'] == "2A":
                    return account_services.balance(sender,response)

                elif state['Status'] == "2B":
                    return account_services.verify_account(sender,response)

                elif state['Status'] == "2D":
                    return account_services.addemail(sender,response)
                elif state['Status'] == "2E":
                    return account_services.addphone(sender,response)
                elif state['Status'] == "Register_fone":
                    sh.session_status(sender,session_type="2",status='set_pin')
                    
                    existance = dbh.db['account_balances'].count_documents({"account_no": response})
                    
                    if existance > 0:
                        record = {
                            "Sender": sender,
                            "account_no": response,
                            "pin": "----"
                            }
                        dbh.db['registered_users'].insert_one(record)
                        message = "*Account details successfully saved, please set a pin for your account*"
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message = "Invalid account number,please verify your account number before trying again4"
                        api.reply_message(sender,message)
                        return '', 200
                elif state['Status'] == "set_pin":

                    account = dbh.db['registered_users'].find_one({"Sender": sender})
                    dbh.db['registered_users'].update({"Sender": sender},
                    {
                        "Sender": sender,
                        "account_no": account['account_no'],
                        "pin": response
                        })
                    message = "Details successfully saved"
                    sh.session_status(sender,session_type="2",status='0')
                    api.reply_message(sender,message)
                    return account_services.menu(sender,2)
                else:
                    message = "*This feature is not yet working*"
                    api.reply_message(sender,message)
                    return '', 200

        elif state['session_type'] == "6":

            if state['Status'] == "0":
                if response == "1" or response == "2" or response == "3":
                    sh.session_status(sender,session_type=state['session_type'],status='6A')
                    
                    if response == '1':
                        payment_method = 'ecocash'
                    elif response == '2':
                        payment_method = 'telecash'
                    elif response == '3':
                        payment_method = 'onemoney'
                    else:
                        message = "*invalid input*\nplease select a valid payment method\n*1*.Ecocash\n*2*.Telecash\n*3*.One Money\n*0*.Cancel transaction"
                        api.reply_message(sender,message)
                        return '', 200

                    record = {
                            "Sender": sender,
                            "account": "",
                            "reference_no": random.randint(10000,99999),
                            "pay_number": '',
                            "email": "",
                            "amount": "",
                            "Purpose": "",
                            "Payment_method": payment_method,
                            "Date_paid": datetime.datetime.now()
                            }
                    dbh.db['pending_payments'].insert_one(record)
                    message = "*Please provide your mobile number*"
                    api.reply_message(sender,message)
                    return '', 200
                
                else:
                    return main.menu(sender)

            elif state['Status'] == "6A":
                return payments.addphone(sender,response)

            elif state['Status'] == "6B":
                return payments.addemail(sender,response)
            elif state['Status'] == "6C":
                return payments.addamount(sender,response)
            elif state['Status'] == "6D": 
                return payments.addpurpose(sender,response)
            elif state['Status'] == "6E":
                return payments.confirm(sender,response)
            elif state['Status'] == "6F":
                return payments.makepayment(sender,response)
            else:
                pass

        elif state['session_type'] == '5':

            if state['Status'] == "0":
                return queries.addname(sender,response)
            elif state['Status'] == 'A':
                
                details = dbh.db['Queries'].find_one({"Sender": sender})
                dbh.db['Queries'].update({"Sender": sender},{
                    "Sender": details['Sender'],
                    "Complainant": details['Complainant'],
                    "Address": response,
                    "Query_catergory": "",
                    "Query_type": "",
                    "Query": " "
                })
            
                sh.session_status(sender,session_type='5',status = 'B')
                message =  "*Query logging*\nPlease select one of the following options 👇\n*1*.Water Queries.\n*2*.Sewer Queries\n*3*.Account/Bill Queries\n*4*.Road Query\n*5*.Health Query\n*6*.Other/General Queries\n*7*.Parking Queries\n*0*.Return to main menu"
                api.reply_message(sender,message)
                return '', 200

            elif state['Status'] == 'B':

                if response == '1':

                    sh.session_status(sender,session_type='5',status='1A')
                    message =  "*Water related queries*\nPlease select one of the following options 👇\n*1*.Water Quality.\n*2*.Water Burst\n*3*.Water Shortage\n*4*.Water Connection\n*5*.Other \n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '2':
                    #sewer queries

                    sh.session_status(sender,session_type='5',status='1B')
                    message =  "*Sewer related queries*\nPlease select one of the following options 👇\n*1*.Sewer connection.\n*2*.Sewer Blockage\n*3*.Other\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '3':
                    #bill queries
                    sh.session_status(sender,session_type='5',status = '1C')
                    message =  "*Account/Bill related queries*\nPlease select one of the following options 👇\n*1*.Request current statements.\n*2*.Incorrect bill(high/low)\n*3*.Other\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '4':
                    #road queries
                    sh.session_status(sender,session_type='5',status ='1D')
                    message =  "*Road related queries*\nPlease select one of the following options 👇\n*1*.Not working traffic light.\n*2*.Report pothole\n*3*.Report blocked road drainage\n*4*.Report not visible road sign\n*5*.Not visible road marking"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '5':
                    #health queries
                    sh.session_status(sender,session_type='5',status = '1E')
                    message =  "*Health related queries*\nPlease select one of the following options 👇\n*1*.Refuse Collection.\n*2*.Dumping\n*3*.Litteering\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '6':
                    #general querues
                    sh.session_status(sender,session_type='5',status ='1F')
                    message =  "*General Queries*\nPlease provide the type of your query"
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '7':
                    #parking queries
                    sh.session_status(sender,session_type='5',status ='1G')
                    message =  "*Parking related queries*\nPlease select one of the following options 👇\n*1*.Shortage of parking space.\n*2*.Unavailable attended\n*3*.Corrupt attended\n*4*.Dangerous parking\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '0':
                    return main.menu(sender)
                else:
                    message = '*Invalid response*'
                    api.reply_message(sender,message)
                    return '', 200

            elif state['Status'] == "1A":
                
                if response == '1':
                    
                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Water related",
                        "Query_type": "Water Quality",
                        "Query": " "
                            })

                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '2':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                            "Query_catergory": "Water related",
                        "Query_type": "Water Burst",
                        "Query": " "
                            })

                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '3':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                            "Query_catergory": "Water related",
                        "Query_type": "Water Shortages",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '4':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                            "Query_catergory": "Water related",
                        "Query_type": "Water Connection",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                elif response == '5':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                            "Query_catergory": "Water related",
                        "Query_type": "Other",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                else:
                    message = '*Invalid response*'
                    api.reply_message(sender,message)
                    return '', 200
            elif state['Status'] == "1B":
                
                if response == '1':
                    
                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Sewer related",
                        "Query_type": "Sewer connection",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '2':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Sewer related",
                        "Query_type": "Sewer Blockage",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '3':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Sewer related",
                        "Query_type": "Other",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                else:
                    message = '*Invalid response*'
                    api.reply_message(sender,message)
                    return '', 200

            elif state['Status'] == "1C":
                
                if response == '1':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Account related",
                        "Query_type": "Request current statement",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nPlease provide your account number,phone number,email address eg 1234567,07XXXXXXXXX,youremail@email.com.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '2':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Account related",
                        "Query_type": "Incorrect bil amount",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '3':
                    
                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Account related",
                        "Query_type": "Other",
                        "Query": " "
                            })

                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                else:
                    message = '*Invalid response*'
                    api.reply_message(sender,message)
                    return '', 200

            elif state['Status'] == '1D':

                if response == '1':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Road related",
                        "Query_type": "Not working traffic light",
                        "Query": " "
                            })

                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '2':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Road related",
                        "Query_type": "Road Potholes",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '3':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Road related",
                        "Query_type": "Blocked road drainage",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '4':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Road related",
                        "Query_type": "Road Sign",
                        "Query": " "
                            })

                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '5':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Road related",
                        "Query_type": "Road Marking",
                        "Query": " "
                            })

                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                else:
                    message = '*Invalid response*'
                    api.reply_message(sender,message)
                    return '', 200

            elif state['Status'] == '1E':

                if response == '1':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Health related",
                        "Query_type": "Uncollect Refuse",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '2':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Health related",
                        "Query_type": "Illegal Dumping",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')
                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '3':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Health related",
                        "Query_type": "Littering",
                        "Query": " "
                            })

                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                else:
                    message = '*Invalid response*'
                    api.reply_message(sender,message)
                    return '', 200

            elif state['Status'] == '1F':
                
                details = dbh.db['Queries'].find_one({"Sender": sender})
                dbh.db['Queries'].update({"Sender": sender},{
                    "Sender": details['Sender'],
                    "Complainant": details['Complainant'],
                    "Address": details['Address'],
                    "Query_catergory": "General Queries",
                    "Query_type": response,
                    "Query": " "
                        })

                sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    
                message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                api.reply_message(sender,message)
                return '', 200
    
            elif state['Status'] == '1G':

                if response == '1':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Parking related",
                        "Query_type": "Shortage of parking space",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200
                
                if response == '2':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Parking related",
                        "Query_type": "Unavailable parking attendant",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

                if response == '3':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Parking related",
                        "Query_type": "Corrupt attended",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200
                    
                if response == '4':

                    details = dbh.db['Queries'].find_one({"Sender": sender})
                    dbh.db['Queries'].update({"Sender": sender},{
                        "Sender": details['Sender'],
                        "Complainant": details['Complainant'],
                        "Address": details['Address'],
                        "Query_catergory": "Parking related",
                        "Query_type": "Dangerous Parking",
                        "Query": " "
                            })
                    sh.session_status(sender,session_type=state['session_type'],status = 'log')

                    message = '*Logging Query*\nOur sincere apologies for the bad experience with us,Please briefly explain your query.'
                    api.reply_message(sender,message)
                    return '', 200

            else:
                    if state['Status'] == 'log':
                        query = dbh.db['Queries'].find_one({"Sender": sender})
                        query_id = random.randint(1000,9999)

                        dbh.db['Queries'].update({"Sender": sender},{
                            
                            "Sender": query['Sender'],
                            "Complainant": query['Complainant'],
                            "reference": query_id,
                            "Address": query['Address'],
                            "Query_catergory": query['Query_catergory'],
                            "Query_type": query['Query_type'],
                            "Query": response
                        })
                        
                        query = dbh.db['Queries'].find_one({"Sender": sender})

                        
                        record = {
                            "Sender": query['Sender'],
                            "Complainant": query['Complainant'],
                            "reference": query_id,
                            "Address": query['Address'],
                            "Query_catergory": query['Query_catergory'],
                            "Query_type": query['Query_type'],
                            "Query": query['Query']
                            }
                        dbh.db['CustomerQueries'].insert_one(record)
                        dbh.db['Queries'].find_one_and_delete({'Sender': sender})

                        message = "Thank you for registering the query, we have taken note of your concern and feedback shall be provided."
                        api.reply_message(sender,message)

                        message = 'Your query have been successfully logged,Your query id is '+str(query_id)+'. You can use your id to check the status of your query\n\n*United Together, we shall make City of Mutare Great once again*'
                        api.reply_message(sender,message)

                        message = "*Attention public Relations*\nKindly assist complainant with details below\n*Contact number*: "+ sender + "\n*Complainant*: " + query['Complainant'] + "\n*Complanaint address*: " + query['Address'] + "\n*Query Category*: " + query['Query_catergory'] +"\n*Query Type*: " + query['Query_type'] + "\n*Complain* : " + query['Query'] +"\n\n*Your assistance will be greatly appreciated*"
                        api.reply_message('263772963833',message)

                        message = "*Attention public Relations*\nKindly assist complainant with details below\n*Contact number*: "+ sender + "\n*Complainant*: " + query['Complainant'] + "\n*Complanaint address*: " + query['Address'] + "\n*Query Category*: " + query['Query_catergory'] +"\n*Query Type*: " + query['Query_type'] + "\n*Complain* : " + query['Query'] +"\n\n*Your assistance will be greatly appreciated*"
                        api.reply_message('263775792461',message)
                        

                        return main.menu(sender)
                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200
        elif state['session_type'] == "7":

            if state['Status'] == "0":

                message = "*Attention public Relations*\nYou have received a direct message from "+ sender + "\n*Username*: " + senderName+"\n\n*Your assistance will be greatly appreciated,kindly login into the systen to assist*"
                api.reply_message('263775792461',message)
                api.reply_message('263772963833',message)
                
                record = {
                    "Sender":sender,
                    "reference": state['Reference'],
                    "message": message,
                    "status": "RECEIVED",
                    "Timestamp": datetime.datetime.now()
                }
                dbh.db['chats'].insert_one(record)
                return '',200

            else:
                message = "*Attention public Relations*\nKindly call " + senderName+" on contact number "+ sender +" He/She is requesting for assistance on below matter\n\n*"+ response +"*\n\n*Your assistance will be greatly appreciated*"
                api.reply_message('263775792461',message)
                api.reply_message('263772963833',message)

                message = "*We have forwarded your message to our call center, our agent ll call you in nearest possible time*"
                api.reply_message(sender,message)
                return main.menu(sender)

        elif state['session_type'] == "8":

            if state['Status'] == "0":
                return budget.addfullname(response,sender)
            elif state['Status'] == "1A":
                return budget.addgender(response,sender)
            elif state['Status'] == "1B":
                return budget.addage(response,sender)
            elif state['Status'] == "1C":
                return budget.addnation(response,sender)
            elif state['Status'] == "1D":
                return budget.addcategory(response,sender)
            elif state['Status'] == "1E":
                return budget.addaccount(response,sender)
            elif state['Status'] == "1F":
                return budget.senddocuments(response,sender)
            elif state['Status'] == "1G":
                return budget.addcomment(response,sender)
            elif state['Status'] == "1H":
                return budget.addobjection(response,sender)
            elif state['Status'] == "1I":
                return budget.objectBudget(response,sender)
            elif state['Status'] == "1J":
                return budget.addratings(response,sender)
            elif state['Status'] == "1K":
                return budget.addrecommendations(response,sender)
            elif state['Status'] == "1L":
                return budget.welcomeback(response,sender)
            else:
                message = "*im sorry i didnt get that*"
                api.reply_message(sender,message)
                return '', 200

        elif state['session_type'] == "10":
            
            if state['Status'] == "0":
                return nationalgrants.addfullname(response,sender)
            elif state['Status'] == "1A":
                return nationalgrants.addgender(response,sender)
            elif state['Status'] == "1B":
                return nationalgrants.addage(response,sender)
            elif state['Status'] == "1C":
                return nationalgrants.addnation(response,sender)
            elif state['Status'] == "1D":
                return nationalgrants.addcategory(response,sender)
            elif state['Status'] == "1E":
                return nationalgrants.addaccount(response,sender)
            elif state['Status'] == "1F":
                return nationalgrants.sendnationaldocuments(response,sender)
            elif state['Status'] == "1G":
                return nationalgrants.addnationlcomment(response,sender)
            elif state['Status'] == "1H":
                return nationalgrants.addobjection(response,sender)
            elif state['Status'] == "1I":
                return nationalgrants.objectBudget(response,sender)
            elif state['Status'] == "1J":
                return nationalgrants.addrecommendations(response,sender)
            elif state['Status'] == "1K":
                return nationalgrants.addrecommendations(response,sender)
            elif state['Status'] == "1L":
                return nationalgrants.welcomeback(response,sender)
            else:
                message = "*im sorry i didnt get that*"
                api.reply_message(sender,message)
                return '', 200

        elif state['session_type'] == "Feedback":
            record = {
                "Sender": sender,
                "Timestamp": datetime.datetime.now(),
                "feedback": response 
                }
            dbh.db['feedback'].insert_one(record)
            return main.endchat(sender)

        else:
            message = "*im sorry i didnt get that*"
            api.reply_message(sender,message)
            return '', 200

            
@app.route('/',methods=["get"])
def dashboard():

    if 'username' in session:
        total_reviews = dbh.db['budget_reviewers'].count_documents({})
        performance_review = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Performance Report"})
        tarrif_review = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Tarrif Schedule"})
        projects_review = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Proposed Projects"})
    
        objections = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Performance Report","Objection" :"YES"})

        avg = dbh.db['budget_reviews'].aggregate(
            [
                {
                    "$group":
                    {
                        "_id": "$Budget_type",
                        "avgRating": { "$avg": "$Rating" }
                    }
                }
            ]
        )

        performance_avgrating = 0
        tarrif_avgrating = 0
        projects_avgrating =0
        for a in avg:

            if a['_id'] == 'Performance Report':
                performance_avgrating = round(a['avgRating'])
            elif a['_id'] == 'Tarrif Schedule':
                tarrif_avgrating =  round(a['avgRating'])
            elif a['_id'] == 'Proposed Projects':
                projects_avgrating =  round(a['avgRating'])
            else:
                print('unidentified budget type')
        comments = dbh.db['budget_reviews'].find().limit(100)
        #return "Total"+ str(total_reviews) +"<br>" + "Performance"+ str(performance_review) + "<br>" + "Tarrif" + str(tarrif_review) + "<br>"+ "Projects" + str(projects_review)
        return render_template('index.htm',total_reviews = total_reviews,
        performance_review = performance_review,tarrif_review = tarrif_review,
        projects_review = projects_review,comments = comments,performance_avgrating = performance_avgrating,
        tarrif_avgrating = tarrif_avgrating,projects_avgrating = projects_avgrating)
   
    else:
        return redirect('/login')
     

@app.route('/performance-report/statistics',methods=["get"]) 
def performance_stats():
    performance_review = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Performance Report"})
    objections = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Performance Report","Objection" :"YES"})
    
    avg = dbh.db['budget_reviews'].aggregate(
        [
            {
                "$group":
                {
                    "_id": "$Budget_type",
                    "avgRating": { "$avg": "$Rating" }
                }
            }
        ]
    )
    performance_avgrating = 0
    for a in avg:

        if a['_id'] == 'Performance Report':
            performance_avgrating = a['avgRating']
        else:
            pass
    return render_template('performance_stats.htm',performance_avgrating = performance_avgrating,performance_review = performance_review,
    objections = objections)

@app.route('/performance-report/comments',methods=["get"])
def performance_comments():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"Performance Report"}).limit(100)
    return render_template('performance_comments.htm',comments = comments)


@app.route('/performance-report/generatereport',methods=["post"])
def generate_performance_report():

    if request.method == 'POST':
        report_type = request.form['report']

        if report_type == "analyze":
            comments = dbh.db['budget_reviews'].find({"Budget_type" :"Performance Report"})
            analysis_results = []
            
            for comment in comments:
                
                text = comment['Comment']
                #Call to the function
                results = te.get_emotion(text)
                result = max(results, key=results.get)
                if result == 'Happy':

                    current_mood = "😀 Happy face"

                elif result == 'Angry':
                    
                    current_mood = "☹️ Angry Face"

                elif result == 'Sad':

                    current_mood = "😞 Sad Face"
                
                elif result == 'Fear':

                    current_mood = "😨 Surprised/Fearing face"

                elif result == 'Suprise':
                    
                    current_mood = "😨 Surprised/Fearing face"

                else:
                     current_mood = "☺️ Informative"


                record = {
                    "Sender": comment['Sender'],
                    "Objection": comment['Objection'],
                    "Comment": comment['Comment'],
                    "Rating": comment['Rating'],
                    "Mood": current_mood
                }
                analysis_results.append(record)
            print(analysis_results)
            return render_template('performance_analyisis.htm', results = analysis_results)
        elif report_type == "analysis_summary":

            comments = dbh.db['budget_reviews'].find({"Budget_type" :"Performance Report"})
            analysis_results = []

            happy = 0
            Angry = 0
            Sad = 0
            Fear = 0
            Suprise = 0
            unknown = 0

            
            for comment in comments:
                text = comment['Comment']
                #Call to the function
                results = te.get_emotion(text)
                result = max(results, key=results.get)

                if results[result] == 0:
                    unknown = unknown + 1
                else:

                    if result == 'Happy':
                        happy = happy + 1

                    elif result == 'Angry':
                        
                        Angry = Angry + 1

                    elif result == 'Sad':

                        Sad = Sad + 1
                    
                    elif result == 'Fear':

                        Fear = Fear + 1

                    elif result == 'Suprise':
                        
                        Suprise = Suprise + 1

                    else:
                        unknown = unknown + 1


            record = {
                "Happy": happy,
                "Angry": Angry,
                "Sad": Sad,
                "Fear": Fear,
                "Suprise": Suprise,
                "Unknown": unknown
            }

            return render_template('performance_analysis_stats.htm', results = record)
        elif report_type== "withinaperiod":

            start_date = request.form['sd']
            end_date = request.form['ed']

            comments = dbh.db['budget_reviews'].find({"Budget_type" :"Performance Report"})
            return render_template('performance_comments.htm',comments = comments)

        elif report_type == 'bymood':
            comments = dbh.db['budget_reviews'].find({"Budget_type" :"Performance Report"})
            analysis_results = []
            
            for comment in comments:
                text = comment['Comment']
                #Call to the function
                results = te.get_emotion(text)
                result = max(results, key=results.get)
                print(request.form['mood'])
                if result == request.form['mood']:

                    if result == 'Happy':

                        current_mood = "😀 Happy face"

                    elif result == 'Angry':
                        
                        current_mood = "☹️ Angry Face"

                    elif result == 'Sad':

                        current_mood = "😞 Sad Face"
                    
                    elif result == 'Fear':

                        current_mood = "😨 Surprised/Fearing face"

                    elif result == 'Suprise':
                        
                        current_mood = "😨 Surprised/Fearing face"

                    else:
                        current_mood = "☺️ Informative"


                    record = {
                        "Sender": comment['Sender'],
                        "Objection": comment['Objection'],
                        "Comment": comment['Comment'],
                        "Rating": comment['Rating'],
                        "Mood": current_mood
                    }
                    analysis_results.append(record)
            return render_template('performance_analyisis.htm', results = analysis_results)

        else:
            pass
    else:
        return redirect('/performance-report/comments')

#MANAGEMENT REPORTS
@app.route('/management-reports/generate/<report_type>',methods=["get","post"])
def managementreports(report_type):

        report_type = report_type
        analysis_results = []

        if report_type == "analyze":
            comments = dbh.db['budget_reviews'].find()
              
            for comment in comments:
                try:
                    text = comment['Comment']
                    rating = comment['Rating'] 
                    myobjection = comment['Objection']
                    budget_type = comment['Budget_type']
                except KeyError:
                    text = "No comment at the moment"
                    rating = 0
                    myobjection = "NO"
                    budget_type = "--"

                #Call to the function
                results = te.get_emotion(text)
                result = max(results, key=results.get)

                if results[result] == 0:
                    current_mood = "😞 Could not get the mood"

                else:
                    if result == 'Happy':

                        current_mood = "😀 Happy face"

                    elif result == 'Angry':
                        
                        current_mood = "☹️ Angry Face"

                    elif result == 'Sad':

                        current_mood = "😞 Sad Face"
                    
                    elif result == 'Fear':

                        current_mood = "😨 Surprised/Fearing face"

                    elif result == 'Suprise':
                        
                        current_mood = "😨 Surprised/Fearing face"

                    else:
                        current_mood = "☺️ Informative"


                record = {
                    "Sender": comment['Sender'],
                    "Budget_type": budget_type,
                    "Objection": myobjection,
                    "Comment": text,
                    "Rating": rating,
                    "Mood": current_mood
                }
                analysis_results.append(record)
            print(analysis_results)
            

        elif report_type == "analysis_summary":

            comments = dbh.db['budget_reviews'].find()
            analysis_results = []

            happy = 0
            Angry = 0
            Sad = 0
            Fear = 0
            Suprise = 0
            unknown = 0

            
            comments = dbh.db['budget_reviews'].find()
              
            for comment in comments:
                try:
                    text = comment['Comment']
                    rating = comment['Rating'] 
                    myobjection = comment['Objection']
                    budget_type = comment['Budget_type']
                except KeyError:
                    text = "No comment at the moment"
                    rating = 0
                    myobjection = "NO"
                    budget_type = "--"

                results = te.get_emotion(text)
                result = max(results, key=results.get)

                if results[result] == 0:
                    unknown = unknown + 1
                else:

                    if result == 'Happy':
                        happy = happy + 1

                    elif result == 'Angry':
                        
                        Angry = Angry + 1

                    elif result == 'Sad':

                        Sad = Sad + 1
                    
                    elif result == 'Fear':

                        Fear = Fear + 1

                    elif result == 'Suprise':
                        
                        Suprise = Suprise + 1

                    else:
                        unknown = unknown + 1


            record = {
                "Happy": happy,
                "Angry": Angry,
                "Sad": Sad,
                "Fear": Fear,
                "Suprise": Suprise,
                "Unknown": unknown
            }
            return render_template('performance_analysis_stats.htm', results = record)
        else:
            comments = dbh.db['budget_reviews'].find()
            analysis_results = []
            
            for comment in comments:

                try:
                    text = comment['Comment']
                    rating = comment['Rating'] 
                    myobjection = comment['Objection']
                    budget_type = comment['Budget_type']
                except KeyError:
                    text = "No comment at the moment"
                    rating = 0
                    myobjection = "NO"
                    budget_type = "--"
                #Call to the function
                results = te.get_emotion(text)
                result = max(results, key=results.get)

                if result == report_type:

                    if result == 'Happy':

                        current_mood = "😀 Happy face"

                    elif result == 'Angry':
                        
                        current_mood = "☹️ Angry Face"

                    elif result == 'Sad':

                        current_mood = "😞 Sad Face"
                    
                    elif result == 'Fear':

                        current_mood = "😨 Surprised/Fearing face"

                    elif result == 'Suprise':
                        
                        current_mood = "😨 Surprised/Fearing face"

                    else:
                        current_mood = "☺️ Informative"

                    record = {
                        "Sender": comment['Sender'],
                        "Budget_type": budget_type,
                        "Objection": myobjection,
                        "Comment": text,
                        "Rating": rating,
                        "Mood": current_mood
                    }
                    analysis_results.append(record)
            return render_template('Analysis_report.htm', results = analysis_results)
            
        return render_template('Analysis_report.htm', results = analysis_results)


#REPORTS END HERE


@app.route('/performance-report/recommendations')
def performance_recommendations():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"Performance Report"}).limit(100)
    return render_template('performance_recommendations.htm',comments = comments) 
    

@app.route('/tarrif-schedule/statistics',methods=["get"]) 
def tarrif_stats():
    performance_review = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Tarrif Schedule"})
    objections = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Tarrif Schedule","Objection" :"YES"})
    
    avg = dbh.db['budget_reviews'].aggregate(
        [
            {
                "$group":
                {
                    "_id": "$Budget_type",
                    "avgRating": { "$avg": "$Rating" }
                }
            }
        ]
    )
    performance_avgrating = 0
    for a in avg:

        if a['_id'] == 'Tarrif Schedule':
            performance_avgrating = a['avgRating']
        else:
            pass
    return render_template('tarrif_stats.htm',performance_avgrating = performance_avgrating,performance_review = performance_review,
    objections = objections)

@app.route('/water-tarrif/statistics',methods=["get"]) 
def water_stats():
    performance_review = dbh.db['budget_reviews'].count_documents({"Budget_type" :"water tarrif"})
    objections = dbh.db['budget_reviews'].count_documents({"Budget_type" :"water tarrif","Objection" :"YES"})
    
    avg = dbh.db['budget_reviews'].aggregate(
        [
            {
                "$group":
                {
                    "_id": "$Budget_type",
                    "avgRating": { "$avg": "$Rating" }
                }
            }
        ]
    )
    performance_avgrating = 0
    for a in avg:

        if a['_id'] == 'water tarrif':
            performance_avgrating = a['avgRating']
        else:
            pass
    return render_template('water_stats.htm',performance_avgrating = performance_avgrating,performance_review = performance_review,
    objections = objections)

@app.route('/water-tarrif/comments',methods=["get"])
def water_comments():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"water tarrif"}).limit(100)
    return render_template('water_comments.htm',comments = comments)

@app.route('/water-tarrif/recommendations')
def water_recommendations():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"water tarrif"}).limit(100)
    return render_template('water_recommendations.htm',comments = comments) 


@app.route('/tarrif-schedule/comments',methods=["get"])
def tarrif_comments():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"Tarrif Schedule"}).limit(100)
    return render_template('tarrif_comments.htm',comments = comments)

@app.route('/tarrif-schedule/recommendations')
def tarrif_recommendations():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"Tarrif Schedule"}).limit(100)
    return render_template('tarrif_recommendation.htm',comments = comments) 


@app.route('/proposed-projects/statistics',methods=["get"]) 
def projects_stats():
    performance_review = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Proposed Projects"})
    objections = dbh.db['budget_reviews'].count_documents({"Budget_type" :"Proposed Projects","Objection" :"YES"})
    
    avg = dbh.db['budget_reviews'].aggregate(
        [
            {
                "$group":
                {
                    "_id": "$Budget_type",
                    "avgRating": { "$avg": "$Rating" }
                }
            }
        ]
    )
    performance_avgrating = 0
    for a in avg:

        if a['_id'] == 'Proposed Projects':
            performance_avgrating = a['avgRating']
        else:
            pass
    return render_template('projects_stats.htm',performance_avgrating = performance_avgrating,performance_review = performance_review,
    objections = objections)

@app.route('/proposed-projects/comments',methods=["get"])
def projects_comments():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"Proposed Projects"}).limit(100)
    return render_template('projects_comments.htm',comments = comments)

@app.route('/proposed-projects/recommendations',methods=["get"])
def projects_recommendations():
    comments = dbh.db['budget_reviews'].find({"Budget_type" :"Proposed Projects"}).limit(100)
    return render_template('projects_recommendations.htm',comments = comments) 

@app.route('/login',methods=["GET","POST"])
def login():
    
    if request.method == 'POST':
        name = request.form['email']
        password = request.form['password']
        
        for user in dbh.db['System_users'].find():
            if user['Email'] == name:
                if user['Password'] == password:
                    session['username'] = user['username']

                    return redirect('/')
                else:
                    message = "Invalid Password"
                    return render_template('login.htm',message = message)

            else:
                message = "Unidentified User, Please ensure your station is registered"
                return render_template('login.htm',message = message)
    else:
        return render_template('login.htm')

    return render_template('login.htm') 

@app.route('/signup',methods = ['GET','POST'])
def signup():

    if request.method == 'POST':

        if request.form['pass1'] == request.form['pass2']:

            email = request.form['email']
            if main.validateemail(email):

                user = {
                    "username": request.form['username'],
                    "Email": request.form['email'],
                    "Password": request.form['pass1']
                }
                dbh.db['System_users'].insert_one(user)

                message = "User successfully saved"
                return render_template('signup.htm',message = message)
            else:
                message = "Invalid email address"
                return render_template('signup.htm',message = message)
        
        else:

            message = "Invalid email address"
            return render_template('signup.htm',message = message)
            
    else:
        print(request.method)
        return render_template('signup.htm')

@app.route('/logout')
def loggout():
    session.pop('username', None)
    return redirect('/login')

        
if __name__ == '__main__':
   app.secret_key = 'LADS-AFRICA'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(host= '0.0.0.0', debug = True)
