from datetime import date,datetime
import pymongo
from flask import Flask, redirect, render_template, request, session, url_for
import datetime,requests
import waiting_list,account_services,payments,main,budget
import sh,api
import sys,os,random
from paynow import Paynow

# client = messagebird.Client('QQRgKx3QvpSV6SpEVewDvWJGK', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANdbh.dbOX])
# # Enable conversations API whatsapp sandbox# client = messagebird.Client('1ekjMs368KTRlP0z6zfG9P70z', #features = [messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])

app = Flask(__name__)
import dbh


@app.route('/chatbot/payments',methods=["post"])
def paynowresponse():
    print(request.get_json())
    return '',200




@app.route('/',methods=["get","post"])
def dashboard():

    if request.method == 'GET':
        # num_payments = db['payments'].count_documents({})
        # feeds = db['feedback'].count_documents({})
        # waitinglists = db['waiting_list'].count_documents({})
        return "dashboard"
        #return render_template('index.html',num_p = num_payments,feeds = feeds,waitinglists = waitinglists)

    payload = request.get_json()
    sender = payload['messages'][0]['author'].split('@')[0]
    senderName = payload['messages'][0]['senderName']
    message_id = payload['messages'][0]['id']
    response = payload['messages'][0]['body']
    
    if sender == '263714502462':
        return '', 200

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

        caption = "Hello "+ senderName +" 🙋🏽‍♂ , \nThank you for contacting Lads Africa,I'm Tau, i'm a virtual assistant,\nFor any emergency 👇 \n📞 Dial Number: +263773068901 \n\nPlease select one of the following options 👇 \n*1*.Waiting List Services 📝\n*2*.Account Services\n*3*.Book an inspection\n*4*.Payment Plan services\n*5*.Log a Query\n*6*.Make a payment\n*7*.Request a call from our customer care representatives\n*8*.Budget Consultations\n*0*.Cancel"
        attachment_url = 'https://chikobvore.github.io/Unlock-Technologies/img/logo.jpeg'
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
            message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options 👇\n*1*. Waiting List Services 📝.\n*2*.Account Services\n*3*.Book an inspection\n*4*.Payment Plan services\n*5*.Log a Query\n*6*.Make a payment\n*7*.Request a call from our customer care representatives\n*8*.Budget Consultations\n*0*.Cancel"
            api.reply_message(sender,message)
            return '', 200


        if state['session_type'] == "0":
            
            if response == "1":
                return waiting_list.waiting_list_menu(sender,response)
            elif response == "2":
                return account_services.menu(sender,response)
            elif response == "3":
                #Book an inspection
                message = "Please ensure that you have a approved plan and $0.00 accrued areas before booking an inspection"
                api.reply_message(sender,message)
                return '', 200

            elif response == "4":
                #payment plan services
                message = "No payment plan found for this account"
                api.reply_message(sender,message)
                return '', 200

            elif response == "5":
                #query logging
                sh.session_status(sender,session_type=response,status='0')
                message =  "*Query logging*\nPlease select one of the following options 👇\n*1*.Water Queries.\n*2*.Sewer Queries\n*3*.Account/Bill Queries\n*4*.Road Query\n*5*.Health Query\n*6*.Other/General Queries\n*0*.Return to main menu"
                api.reply_message(sender,message)
                return '', 200

            elif response == "6":
                return payments.pay(sender,response)
        
            elif response == "7":

                sh.session_status(sender,session_type=response,status='0')

                message = "Our customer services representatives are currently occupied, please leave your message an agent ll assist you in the nearest possible time"
                api.reply_message(sender,message)
                return '', 200

            elif response == "8":
                
                existance = dbh.db['budget_reviewers'].count_documents({"Sender": sender}) 
                #check if session exist
                if existance < 1:
                    sh.session_status(sender,session_type=response,status='0')
                    message = "*Budget consultations*\nThank you for reaching us, we value your feedback and support.\nFor the purposes of quality evaluation please provide your full name"
                    api.reply_message(sender,message)
                    return '', 200
                else:
                    sh.session_status(sender,session_type='8',status='1B')
                    message = "*Welcome Back* "+ sender
                    api.reply_message(sender,message)
                    return budget.attachmentmessage(sender)
            
            elif response == "0":
                return main.menu(sender)
            else:
                #invalid response from user
                message =  "*Previous session expired*\nHello *"+ senderName +"* 🙋🏽‍♂,\nPlease select one of the following options 👇\n*1*. Waiting List Services 📝.\n*2*.Account Services\n*3*.Book an inspection\n*4*.Payment Plan services\n*5*.Log a Query\n*6*.Make a payment\n*7*.Request a call from our customer care representatives\n*8*Budget Consultations\n*0*.Cancel"
                api.reply_message(sender,message)
                return '', 200

        elif state['session_type'] == "1":

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

                if response == '1':
                    sh.session_status(sender,session_type=state['session_type'],status=response)
                    message =  "*Water related queries*\nPlease select one of the following options 👇\n*1*.Water Quality.\n*2*.Water Leakages\n*3*.Other\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '2':
                    #sewer queries
                    sh.session_status(sender,session_type=state['session_type'],status=response)
                    message =  "*Sewer related queries*\nPlease select one of the following options 👇\n*1*.Sewer connection.\n*2*.Sewer Leakages\n*3*.Other\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '3':
                    #bill queries
                    sh.session_status(sender,session_type=state['session_type'],status = response)
                    message =  "*Account/Bill related queries*\nPlease select one of the following options 👇\n*1*.Double billing.\n*2*.Incorrect bill(high/low)\n*3*.Other\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200

                elif response == '4':
                    #road queries
                    sh.session_status(sender,session_type=state['session_type'],status =response)
                    message =  "*Road related queries*\nPlease select one of the following options 👇\n*1*.Bad Road.\n*2*.Road network\n*3*.Parking queries\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '5':
                    #health queries
                    sh.session_status(sender,session_type=state['session_type'],status = response)
                    message =  "*Health related queries*\nPlease select one of the following options 👇\n*1*.Clinics.\n*2*.Covid Related\n*3*.Vaccination\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '6':
                    #general querues
                    sh.session_status(sender,session_type=state['session_type'],status =response)
                    message =  "*General Queries*\nPlease select one of the following options 👇\n*1*.General query.\n*0*.Return back"
                    api.reply_message(sender,message)
                    return '', 200
                elif response == '0':
                    return main.menu(sender)
                else:
                    message = '*Invalid response*'
                    api.reply_message(sender,message)
                    return '', 200
            else:
                if state['Status'] == "1":
                    
                    if response == '1':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Water related",
                            "Query_type": "Water Quality",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '2':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Water related",
                            "Query_type": "Water Leakages",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '3':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Water related",
                            "Query_type": "Other",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200
                elif state['Status'] == "2":
                    
                    if response == '1':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Sewer related",
                            "Query_type": "Sewer connection",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '2':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Sewer related",
                            "Query_type": "Sewer Leakages",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '3':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Sewer related",
                            "Query_type": "Other",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200

                elif state['Status'] == "3":
                    
                    if response == '1':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Account related",
                            "Query_type": "Double billing",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '2':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Account related",
                            "Query_type": "Incorrect bil amount",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '3':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Account related",
                            "Query_type": "Other",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200

                elif state['Status'] == '4':

                    if response == '1':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Road related",
                            "Query_type": "Bad Road",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Road related",
                            "Query_type": "Road network",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '2':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Road related",
                            "Query_type": "Road network",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '3':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Road related",
                            "Query_type": "Parking queries",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200

                elif state['Status'] == '5':

                    if response == '1':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Health related",
                            "Query_type": "Clinics",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '2':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Health related",
                            "Query_type": "Road network",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')
                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    elif response == '3':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "Health related",
                            "Query_type": "Covid related",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status = 'log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200

                elif state['Status'] == '6':

                    if response == '1':
                        record = {
                            "Sender": sender,
                            "Query_catergory": "General Queries",
                            "Query_type": "general",
                            "Query": " "
                            }
                        dbh.db['Queries'].insert_one(record)
                        sh.session_status(sender,session_type=state['session_type'],status ='log')

                        message = '*Logging Query*\nMy apologies for the bad experience with,Please briefly explain your query.'
                        api.reply_message(sender,message)
                        return '', 200

                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200
                else:
                    if state['Status'] == 'log':
                        query = dbh.db['Queries'].find_one({"Sender": sender})
                        query_id = random.randint(1000,9999)

                        dbh.db['Queries'].update({"Sender": sender},{
                            "Sender": sender,
                            "reference": query_id,
                            "Query_catergory": query['Query_catergory'],
                            "Query_type": query['Query_type'],
                            "Query": response
                        })
                        message = 'Your query have been successfully logged,Your query id is '+str(query_id)+'. You can use your id to check the status of your query'
                        api.reply_message(sender,message)
                        return main.menu(sender)
                    else:
                        message = '*Invalid response*'
                        api.reply_message(sender,message)
                        return '', 200

        elif state['session_type'] == "7":
            if state['Status'] == "0":

                payload = {
                    "phone": sender
                }

                payload1 = {
                    "phone": sender,
                    "labelId": '6'
                }

                
                payload2 = {
                    "phone": 263775531297,
                    "messageId": message_id
                }
                
                response = requests.post("https://api.chat-api.com/instance265454/pinChat?token=7krlsiflsx994ms4", data=payload)
                response2 = requests.post("https://api.chat-api.com/instance265454/labelChat?token=7krlsiflsx994ms4", data=payload1)
                response3 = requests.post("https://api.chat-api.com/instance265454/forwardMessage?token=7krlsiflsx994ms4", data=payload2)
                message = "*We have forwarded your message to our call center, our agent ll call you in nearest possible time*"
                api.reply_message(sender,message)
                return main.menu(sender)
            else:
                message = "*We have forwarded your message to our call center, our agent ll call you in nearest possible time*"
                api.reply_message(sender,message)
                return '', 200

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

        
if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(host= '0.0.0.0', debug = True)