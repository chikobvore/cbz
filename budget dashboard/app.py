from datetime import datetime
import numpy as np
import pandas as pd
import pymongo
from flask import Flask, redirect, render_template, request, session,jsonify,url_for
from bson import json_util
import json
import ssl
import requests

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client.tau

@app.route('/') 
def index():

    total_reviews = db['budget_reviewers'].count_documents({})
    performance_review = db['budget_reviews'].count_documents({"Budget_type" :"Performance Report"})
    tarrif_review = db['budget_reviews'].count_documents({"Budget_type" :"Tarrif Schedule"})
    projects_review = db['budget_reviews'].count_documents({"Budget_type" :"Proposed Projects"})


    avg = db['budget_reviews'].aggregate(
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
            performance_avgrating = a['avgRating']
        elif a['_id'] == 'Tarrif Schedule':
            tarrif_avgrating =  a['avgRating']
        elif a['_id'] == 'Proposed Projects':
            projects_avgrating =  a['avgRating']
        else:
            print('unidentified')
    comments = db['budget_reviews'].find().limit(10)
    #return "Total"+ str(total_reviews) +"<br>" + "Performance"+ str(performance_review) + "<br>" + "Tarrif" + str(tarrif_review) + "<br>"+ "Projects" + str(projects_review)
    return render_template('index.htm',total_reviews = total_reviews,
    performance_review = performance_review,tarrif_review = tarrif_review,
    projects_review = projects_review,comments = comments,performance_avgrating = performance_avgrating,
    tarrif_avgrating = tarrif_avgrating,projects_avgrating = projects_avgrating)


@app.route('/performance-report/statistics') 
def performance_stats():
    performance_review = db['budget_reviews'].count_documents({"Budget_type" :"Performance Report"})
    objections = db['budget_reviews'].count_documents({"Budget_type" :"Performance Report","Objection" :"YES"})
    
    avg = db['budget_reviews'].aggregate(
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

@app.route('/performance-report/comments')
def performance_comments():
    comments = db['budget_reviews'].find({"Budget_type" :"Performance Report"}).limit(10)
    return render_template('performance_comments.htm',comments = comments)

@app.route('/performance-report/recommendations')
def performance_recommendations():
    comments = db['budget_reviews'].find({"Budget_type" :"Performance Report"}).limit(10)
    return render_template('performance_recommendations.htm',comments = comments) 
    

@app.route('/tarrif-schedule/statistics') 
def tarrif_stats():
    performance_review = db['budget_reviews'].count_documents({"Budget_type" :"Tarrif Schedule"})
    objections = db['budget_reviews'].count_documents({"Budget_type" :"Tarrif Schedule","Objection" :"YES"})
    
    avg = db['budget_reviews'].aggregate(
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

@app.route('/tarrif-schedule/comments')
def tarrif_comments():
    comments = db['budget_reviews'].find({"Budget_type" :"Tarrif Schedule"}).limit(10)
    return render_template('tarrif_comments.htm',comments = comments)

@app.route('/tarrif-schedule/recommendations')
def tarrif_recommendations():
    comments = db['budget_reviews'].find({"Budget_type" :"Tarrif Schedule"}).limit(10)
    return render_template('tarrif_recommendation.htm',comments = comments) 


@app.route('/proposed-projects/statistics') 
def projects_stats():
    performance_review = db['budget_reviews'].count_documents({"Budget_type" :"Proposed Projects"})
    objections = db['budget_reviews'].count_documents({"Budget_type" :"Proposed Projects","Objection" :"YES"})
    
    avg = db['budget_reviews'].aggregate(
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

@app.route('/proposed-projects/comments')
def projects_comments():
    comments = db['budget_reviews'].find({"Budget_type" :"Proposed Projects"}).limit(10)
    return render_template('projects_comments.htm',comments = comments)

@app.route('/proposed-projects/recommendations')
def projects_recommendations():
    comments = db['budget_reviews'].find({"Budget_type" :"Proposed Projects"}).limit(10)
    return render_template('projects_recommendations.htm',comments = comments) 


if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(host= '0.0.0.0', debug = True)