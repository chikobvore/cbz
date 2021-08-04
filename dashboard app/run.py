from datetime import datetime
import numpy as np
import pandas as pd
import pymongo
from flask import Flask, redirect, render_template, request, session, url_for,jsonify
from bson import json_util
import json
import ssl
import mysql.connector
import requests

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client.tau

# client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority")
# db = client.tau


@app.route('/') 
def index():
    num_payments = db['payments'].count_documents({})
    feeds = db['feedback'].count_documents({})
    waitinglists = db['waiting_list'].count_documents({})
    return render_template('index.html',num_p = num_payments,feeds = feeds,waitinglists = waitinglists)


@app.route('/housing') 
def housing():
    feeds = db['feedback'].count_documents({})
    waitinglists = db['waiting_list'].count_documents({})
    return render_template('housingdashboard.html',feeds = feeds,waitinglists = waitinglists)

@app.route('/finance') 
def finance():
    accounts = db['accounts'].count_documents({})
    balances = db['account_balances'].count_documents({})
    payments = db['payments'].count_documents({})
    feeds = db['feedback'].count_documents({})

    print(accounts)
    return render_template('financedashboard.html',myaccounts = accounts,num_balances = balances,num_payments = payments,num_feeds = feeds)


@app.route('/balances') 
def balances():
    myaccounts = []

    accounts = db['account_balances'].find().limit(500)

    for account in accounts:
        myaccounts.append(account)
        
    return render_template('balances.html',accounts = myaccounts)


@app.route('/importbalances') 
def importbalances():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lads"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT account_name,account_number,account_balance FROM account_balances")

    myresult = mycursor.fetchall()

    for x in myresult:
        row = list(x)
        record = {
            "account_no": row[1],
            "account_name": row[0],
            "balance": row[2]
        }
        db['test_account_balances'].insert_one(record)

    return redirect('/balances')


@app.route('/accounts') 
def account():
    myaccounts = []

    accounts = db['accounts'].find().limit(500)

    for account in accounts:
        myaccounts.append(account)
        
    return render_template('accounts.html',accounts = myaccounts)

@app.route('/payments') 
def payments():
    mypayments = []

    payments = db['payments'].find().limit(500)

    for payment in payments:
        mypayments.append(payment)
        
    return render_template('payments.html',payments = mypayments)

@app.route('/feedback') 
def feedback():
    feedbacks = []

    feedback = db['feedback'].find().limit(500)

    for feed in feedback:
        feedbacks.append(feed)
        
    return render_template('feedback.html',feedbacks = feedbacks)

@app.route('/payments/export',methods = ['post']) 
def export_payments():

    if request.method == 'POST':

        payments = db['payments'].find()

        mypayments = db['payments'].find().limit(100)

        
        Dataset = pd.DataFrame(payments,columns= [
                "account",
                "reference_no",
                "paynow_ref",
                "pay_number",
                "email",
                "amount",
                "Purpose",
                "Service_code",
                "Status",
                "Date_paid"
        ])
        Export = Dataset.to_csv('payments.csv',index=None,header=True)
            
        return render_template('payments.html',payments = mypayments,message = 'File export was successful, please chech file explorer')

@app.route('/payments/search',methods = ['post']) 
def searchpayments():

    if request.method == 'POST':

        payments = db['payments'].find({"account": request.form['search']})
            
        return render_template('payments.html',payments = payments)


@app.route('/waitinglist',methods = ['get','post']) 
def waitinglist():
    applicants = db['waiting_list'].find()
    details = db['waiting_list_specifics'].find()

    return render_template('waitinglist.html',applications = applicants,details = details)

@app.route('/waitinglist/<reference>/<wnumber>',methods = ['get','post']) 
def dropwaitinglist(reference,wnumber):

    db['waiting_list'].find_one_and_delete({"contact": reference})
    db['waiting_list_specifics'].find_one_and_delete({"contact": reference})

    message = "Good day 🙋🏽‍♂,\nI'm Tau, i'm a virtual assistant from Mutare City Council,\nFor any emergency 👇 \n📞 Dial Number: +263202060823 \n\nI am pleased to inform you that your application to join waiting list of City of Mutare was successfull. Your waiting list number is below👇 \n*"+ wnumber +"*\nPlease be reminded that your waiting list expires on the last of December every year (31 December).To avoid disapointments please ensure that you renew your position on or before the date\nRegards\nMutare City Council"
    payload = {
        "phone": reference,
        "filename": 'https://www.mutarecity.co.zw/images/mutarelogo.png',
        "caption": message,
        "body": 'https://www.mutarecity.co.zw/images/mutarelogo.png'
    }
        
    response = requests.post("https://api.chat-api.com/instance265454/sendFile?token=7krlsiflsx994ms4", data=payload)
    print('....replied: '+ reference + '...........')

    return redirect('/waitinglist')


@app.route('/waitinglist/sync/<reference>',methods = ['post','get']) 
def addwaitinglist(reference):
    print(reference)

    existance = db['waiting_list'].count_documents({"contact": reference})
    if existance > 0:
        Applicant = db['waiting_list'].find_one({"contact": reference})

        return redirect("http://127.0.0.1:8000/whatsappchatbot/waitinglist/sync/"+Applicant['full_name']+'/'+Applicant['gender']+'/'+Applicant['national_id']+'/'+Applicant['dob']+'/'+Applicant['physical_address']+'/'+Applicant['marital_status']+'/'+Applicant['contact']+'/'+Applicant['national_id']+'/'+Applicant['stand_type'], code=302)

    else:
        return "tarishaya"


        
    return "boo"


        
if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(host= '0.0.0.0', debug = True,port='5080')
