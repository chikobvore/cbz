import pymongo
import datetime
import random
import main
import requests
import api
import dbh
import sh
import payments


def waiting_list_menu(sender,response):

    state = dbh.db['Senders'].find_one({"Sender": sender})
    sh.session_status(sender,session_type=response,status='0')

    message = "Waiting List services,\nPlease select one of the following option 👇 \n *1*. Join Waiting List*📝. \n *2*.Renew waiting list 📝\n *3*. View Status \n *0*.Return to main menu\n *"
    api.reply_message(sender,message)
    return '', 200


def addname(sender,response,state):


    #CREATING A RECORD FRO WAITING LIST
    record = {
        "full_name": response,
        "gender": "N/A",
        "national_id": "N/A",
        "dob": "N/A",
        "nationality": "N/A",
        "region": "N/A",
        "city": "N/A",
        "physical_address": "N/A",
        "marital_status": "N/A",
        "contact": sender,
        "email": "N/A",
        "disablity": "N/A",
        "yor": "N/A",
        "waiting_list_no": "N/A",
        "profile": "N/A",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
        }

    dbh.db['waiting_list'].insert_one(record)
    #RECORD SUCCESSFULLY ADDED
    print("Waiting list record successfully added")

    sh.session_status(sender,session_type=state['session_type'],status='1B')

    message = "*Joining Waiting List* \nThank you " + response +" for joining list,\nPlease provide your National ID number"
    api.reply_message(sender,message)
    return '', 200

def add_nationalid(sender,response,state):

    Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
    dbh.db['waiting_list'].update({"contact": sender},{
        "full_name": Applicant['full_name'],
        "gender": "N/A",
        "national_id": response,
        "dob": "N/A",
        "nationality": "N/A",
        "region": "N/A",
        "city": "N/A",
        "physical_address": "N/A",
        "marital_status": "N/A",
        "contact": sender,
        "email": "N/A",
        "disablity": "N/A",
        "yor": "N/A",
        "waiting_list_no": "N/A",
        "profile": "N/A",
        "created_at": Applicant['created_at'],
        "updated_at": datetime.datetime.now()
        })
        
    sh.session_status(sender,session_type=state['session_type'],status='1C')

    message = "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your Date of Birth (YYYY-MM-DD)"
    api.reply_message(sender,message)
    return '', 200

def adddob(sender,response,state):

    if  main.validatedate(sender,response):

        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
        dbh.db['waiting_list'].update({"contact": sender},{
            "full_name": Applicant['full_name'],
            "gender": "N/A",
            "national_id": Applicant['national_id'],
            "dob": response,
            "nationality": "N/A",
            "region": "N/A",
            "city": "N/A",
            "physical_address": "N/A",
            "marital_status": "N/A",
            "contact": sender,
            "email": "N/A",
            "disablity": "N/A",
            "yor": "N/A",
            "waiting_list_no": "N/A",
            "profile": "N/A",
            "created_at": Applicant['created_at'],
            "updated_at": datetime.datetime.now()
            })
        #record updated
        sh.session_status(sender,session_type= state['session_type'],status='1D')
        
        message =  "*Joining Waiting List*,\nDetails successfully saved ✅ \nWhat is your marital Status? \nS. Single \nM. Married"
        api.reply_message(sender,message)
        return '', 200
    
    else:
        message =  "This is the incorrect date string format. It should be YYYY-MM-DD"
        api.reply_message(sender,message)
        return '', 200

def addmarital(sender,response,state):

    if response == "S" or response == "s":

        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
        dbh.db['waiting_list'].update({"contact": sender},{
            "full_name": Applicant['full_name'],
            "gender": "N/A",
            "national_id": Applicant['national_id'],
            "dob": Applicant['dob'],
            "nationality": "N/A",
            "region": "N/A",
            "city": "N/A",
            "physical_address": "N/A",
            "marital_status": "Single",
            "contact": sender,
            "email": "N/A",
            "disablity": "N/A",
            "yor": "N/A",
            "waiting_list_no": "N/A",
            "profile": "N/A",
            "created_at": Applicant['created_at'],
            "updated_at": datetime.datetime.now()
            })

        sh.session_status(sender,session_type=state['session_type'],status='1E')

        message =  "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your Gender\nM.Male\nF.Female"
        api.reply_message(sender,message)
        return '', 200


    elif response == "M" or response == "m":

        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
        dbh.db['waiting_list'].update({"contact": sender},{
            "full_name": Applicant['full_name'],
            "gender": "N/A",
            "national_id": Applicant['national_id'],
            "dob": Applicant['dob'],
            "nationality": "N/A",
            "region": "N/A",
            "city": "N/A",
            "physical_address": "N/A",
            "marital_status": "Married",
            "contact": sender,
            "email": "N/A",
            "disablity": "N/A",
            "yor": "N/A",
            "waiting_list_no": "N/A",
            "profile": "N/A",
            "created_at": Applicant['created_at'],
            "updated_at": datetime.datetime.now()
            })
        sh.session_status(sender,session_type=state['session_type'],status='1F')

        message = "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your Spouse name"
        api.reply_message(sender,message)
        return '', 200

    else:

        message = "*Joining Waiting List*,\nI'm sorry i didnt get that \nWhat is your marital Status? \nS. Single \nM. Married"
        api.reply_message(sender,message)
        return '', 200

def addgender(sender,response,state):
    
    if response == "M" or response == "m":
        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
        dbh.db['waiting_list'].update({"contact": sender},{
            "full_name": Applicant['full_name'],
            "gender": "Male",
            "national_id": Applicant['national_id'],
            "dob": Applicant['dob'],
            "nationality": "N/A",
            "region": "N/A",
            "city": "N/A",
            "physical_address": "N/A",
            "marital_status": Applicant['marital_status'],
            "contact": sender,
            "email": "N/A",
            "disablity": "N/A",
            "yor": "N/A",
            "waiting_list_no": "N/A",
            "profile": "N/A",
            "created_at": Applicant['created_at'],
            "updated_at": datetime.datetime.now()
            })
                    #record updated

        sh.session_status(sender,session_type=state['session_type'],status='1G')

        message =  "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your email address"
        api.reply_message(sender,message)
        return '', 200
        

    elif response == "F" or response =="f":
        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
        dbh.db['waiting_list'].update({"contact": sender},{
            "full_name": Applicant['full_name'],
            "gender": "Male",
            "national_id": Applicant['national_id'],
            "dob": Applicant['dob'],
            "nationality": "N/A",
            "region": "N/A",
            "city": "N/A",
            "physical_address": "N/A",
            "marital_status": Applicant['marital_status'],
            "contact": sender,
            "email": "N/A",
            "disablity": "N/A",
            "yor": "N/A",
            "waiting_list_no": "N/A",
            "profile": "N/A",
            "created_at": Applicant['created_at'],
            "updated_at": datetime.datetime.now()
            })
                    #record updated
        sh.session_status(sender,session_type=state['session_type'],status='1G')
            
        
        message =  "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your email address"
        api.reply_message(sender,message)
        return '', 200
    else:

        message =  "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your Gender\nM.Male\nF.Female"
        api.reply_message(sender,message)
        return '', 200    

def addspouse(sender,response,state):

    sh.session_status(sender,session_type=state['session_type'],status='1E')

    message =  "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your Gender\nM.Male\nF.Female"
    api.reply_message(sender,message)
    return '', 200  


def addaddress(sender,response,state):

    Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
    dbh.db['waiting_list'].update({"contact": sender},{
        "full_name": Applicant['full_name'],
        "gender": Applicant['gender'],
        "national_id": Applicant['national_id'],
        "dob": Applicant['dob'],
        "nationality": "N/A",
        "region": "N/A",
        "city": "N/A",
        "physical_address": response,
        "marital_status": Applicant['marital_status'],
        "contact": sender,
        "email": "N/A",
        "disablity": "N/A",
        "yor": "N/A",
        "waiting_list_no": random.randint(10000, 99999),
        "profile": "N/A",
        "created_at": Applicant['created_at'],
        "updated_at": datetime.datetime.now()
        })
    #record updated
    sh.session_status(sender,session_type=state['session_type'],status='1PA')


    message =   "*Joining Waiting List*,\nAll Personal Details successfully saved ✅✅✅ \n\nPlease select the type of stand you are applying for\n*H*.High Density\n*M*.Medium density.\n*L*.Low density"
    api.reply_message(sender,message)
    return '', 200  

def addemail(sender,response,state):

    if main.validateemail(email=response):

        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
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
            "email": response,
            "disablity": "N/A",
            "yor": "N/A",
            "waiting_list_no": random.randint(1000,9999),
            "profile": "N/A",
            "created_at": Applicant['created_at'],
            "updated_at": datetime.datetime.now()
            })
                        #record updated

        sh.session_status(sender,session_type=state['session_type'],status='1H')

        message =  "*Joining Waiting List*,\nDetails successfully saved ✅ \nPlease provide your physical address"
        api.reply_message(sender,message)
        return '', 200  
    else:
        message =  "Please enter a valid email address"
        api.reply_message(sender,message)
        return '', 200
    

def addnature(sender,response,state):

    if response == 'H' or response == 'h':
        stand = 'High Density'
    if response == 'M' or response == 'm':
        stand = 'Medium Density'
    if response == 'L' or response == 'l':
        stand = 'Low Density'


    Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
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
        "waiting_list_no": random.randint(1000,9999),
        "profile": "N/A",
        "stand_type": stand,
        "status": "PENDING PAYMENT",
        "created_at": Applicant['created_at'],
        "updated_at": datetime.datetime.now()
        })




    #RECORD SUCCESSFULLY ADDED
    Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
    sh.session_status(sender,session_type=state['session_type'],status='Complete')

    message =  "*Please Confirm details below*\n Applicant Name: "+ Applicant['full_name'] +"\nNational ID: " + Applicant['national_id'] + "\nDate of Birth: "+ Applicant['dob'] + "\nPhysical address: "+ Applicant['physical_address'] + "\nMarital Status: "+ Applicant['marital_status']+ "\nType of stand applied for: "+Applicant['stand_type']+"\nStatus: "+ Applicant['status']+"\n*Y*.Yes my details are  correct please proceed\n*N*.No they was an error in my details please cancel my application"
    api.reply_message(sender,message)
    return '', 200

# def addarea(sender,response,state):

#     app_detail = dbh.db['waiting_list_specifics'].find_one({"sender": sender})

#     dbh.db['waiting_list_specifics'].update({"sender": sender},{
#         "sender": sender,
#         "nature": app_detail['nature'],
#         "area": response,
#         "class": "N/A",
#         "catergory": "N/A",
#         "type": "N/A",
#         "development": "N/A",
#         "application_date": datetime.datetime.now(),
#         "expiary_date": datetime.datetime.now(),
#         "capital": "N/A",
#         "receipt_no": "N/A",
#         "created_by": sender,
#         "created_at": datetime.datetime.now(),
#         "updated_at": datetime.datetime.now()
#         })
#     #record updated

#     sh.session_status(sender,session_type=state['session_type'],status='1PD')

#     message =  "*Application Specifics*,\nPlease provide your application Specifications details,\n Please Select the Category of stand you are applying for\n\n C. Commercial \n R. Residential"
#     api.reply_message(sender,message)
#     return '', 200  

# def addcat(sender,response,state):


#     if response == "C" or response == "c":
#         app_detail = dbh.db['waiting_list_specifics'].find_one({"sender": sender})
#         dbh.db['waiting_list_specifics'].update({"sender": sender},{
#             "sender": sender,
#             "nature": app_detail['nature'],
#             "area": app_detail['area'],
#             "class": "N/A",
#             "catergory": "Commercial",
#             "type": "N/A",
#             "development": "N/A",
#             "application_date": datetime.datetime.now(),
#             "expiary_date": datetime.datetime.now(),
#             "capital": "N/A",
#             "receipt_no": "N/A",
#             "created_by": sender,
#             "created_at": datetime.datetime.now(),
#             "updated_at": datetime.datetime.now()
#             })
#         #record updated

#         sh.session_status(sender,session_type=state['session_type'],status='1PE')
        
#         message =  "*Application Specifics*,\nPlease provide your application Specifications details,\n Please Select the Type of stand you are applying for\n\n 2A. Commercial"
#         api.reply_message(sender,message)
#         return '', 200

#     elif response == "R" or response == "r":
#         app_detail = dbh.db['waiting_list_specifics'].find_one({"sender": sender})
#         dbh.db['waiting_list_specifics'].update({"sender": sender},{
#             "sender": sender,
#             "nature": app_detail['nature'],
#             "area": app_detail['area'],
#             "class": "N/A",
#             "catergory": "Residential",
#             "type": "N/A",
#             "development": "N/A",
#             "application_date": datetime.datetime.now(),
#             "expiary_date": datetime.datetime.now(),
#             "capital": "N/A",
#             "receipt_no": "N/A",
#             "created_by": sender,
#             "created_at": datetime.datetime.now(),
#             "updated_at": datetime.datetime.now()
#             })
#         #record updated

#         sh.session_status(sender,session_type=state['session_type'],status='1PE')

#         message =  "*Application Specifics*,\nPlease provide your application Specifications details,\n Please Select the Type of stand you are applying for\n\n 2A. High Density \n 2B. Medium Density \n 3B. Low Density"
#         api.reply_message(sender,message)
#         return '', 200

#     else:
#         message =  "Invalid response"
#         api.reply_message(sender,message)
#         return '', 200
    

# def addtype(sender,response,state):

#     Applicant = dbh.db['waiting_list_specifics'].find_one({"sender": sender})
#     dbh.db['waiting_list_specifics'].update({"sender": sender},{
#        "sender": sender,
#         "nature": Applicant['nature'],
#         "area": Applicant['area'],
#         "class": "N/A",
#         "catergory": Applicant['catergory'],
#         "type": "Physical Property",
#         "development": "N/A",
#         "application_date": datetime.datetime.now(),
#         "expiary_date": datetime.datetime.now(),
#         "capital": "N/A",
#         "receipt_no": "N/A",
#         "created_by": sender,
#         "created_at": datetime.datetime.now(),
#         "updated_at": datetime.datetime.now()
#         })
#     #record updated

#     sh.session_status(sender,session_type=state['session_type'],status='Confirm')

#     message =  "*Application Specifics*,\nPlease provide your application Specifications details,\nWhat is the intended development for the stand?"
#     api.reply_message(sender,message)
#     return '', 200

def confirm(sender,response,state):
    
    if response == 'H' or response == 'h':
        stand = 'High Density'
    if response == 'M' or response == 'm':
        stand = 'Medium Density'
    if response == 'L' or response == 'l':
        stand = 'Low Density'


    Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
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
        "waiting_list_no": random.randint(1000,9999),
        "profile": "N/A",
        "stand_type": stand,
        "status": "PENDING PAYMENT",
        "created_at": Applicant['created_at'],
        "updated_at": datetime.datetime.now()
        })




    #RECORD SUCCESSFULLY ADDED
    Applicant = dbh.db['waiting_list'].find_one({"contact": sender})
    sh.session_status(sender,session_type=state['session_type'],status='Complete')

    message =  "*Please Confirm details below*\n Applicant Name: "+ Applicant['full_name'] +"\nNational ID: " + Applicant['national_id'] + "\nDate of Birth: "+ Applicant['dob'] + "\nPhysical address: "+ Applicant['physical_address'] + "\nMarital Status: "+ Applicant['marital_status']+ "\nType of stand applied for: "+Applicant['stand_type']+"\nStatus: "+ Applicant['status']+"\n*Y*.Yes my details are  correct please proceed\n*N*.No they was an error in my details please cancel my application"
    api.reply_message(sender,message)
    return '', 200

def complete(sender,response,state):

    if response == "Y" or response == "y":

        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})   

        message =  "Thank you for joining our waiting list\nYour application reference number is "+ str(Applicant['waiting_list_no'])+'\nPlease note for your application to be processed you need to make a payment of $1,913.54 RTGS/22.90 USD for the application fee.'
        api.reply_message(sender,message)
        return payments.pay(sender,'6')

    else:
        #to cancel application here
        dbh.db['waiting_list'].find_one_and_delete({"contact": sender})
        dbh.db['waiting_list_specifics'].find_one_and_delete({"contact": sender})
        return main.menu(sender)

def preview(sender):
    
    existance = dbh.db['waiting_list'].count_documents({"contact": sender})
    if existance > 0:
        Applicant = dbh.db['waiting_list'].find_one({"contact": sender})

        message =   "*Waiting List Status*\n Applicant Name: "+ Applicant['full_name'] +"\nNational ID: " + Applicant['national_id'] + "\nDate of Birth: "+ Applicant['dob'] + "\nPhysical address: "+ Applicant['physical_address'] + "\nMarital Status: "+ Applicant['marital_status']
        api.reply_message(sender,message)
        return main.feedback(sender)

    else:

        message =   "You dont have a pending application"
        api.reply_message(sender,message)
        return main.feedback(sender)


def terms(sender,response):
    if response == "Yes" or response == 'yes' or response == 'YES' or 'y' or 'Y':
        sh.session_status(sender,'1','1A')
        message = "*Joining waiting list* \nPlease enter your full name"
        api.reply_message(sender,message)
        return '', 200
    elif response == "No" or response == 'no' or response == 'NO' or 'N' or 'n':
        message = "session cancelled..."
        api.reply_message(sender,message)
        return main.menu(sender)
    else:
        message = "*Invalid response 😔*\nPlease read  carefully our terms and conditions before proceeding\n\nEnter *Yes*. To continue \n*No*.To cancel"
        api.reply_message(sender,message)
        return '', 200


