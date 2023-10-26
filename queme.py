import pymongo
import datetime
import random
import main
import requests
import api
import dbh
import sh
import payments
import re
def addque(sender,response,service):

    if validate_time(response):

        details = dbh.db['customers'].find_one({"Sender": sender})

        if check_availability(response):
            record = {
                "Sender": sender,
                "Full_name": details['Full_name'],
                "Service": service,
                "Time": response,
                }
            dbh.db['customer_queue'].insert_one(record)
            query_id = random.randint(1000,9999)
            message = 'Your request have been successfully logged,Your request id is '+str(query_id)+'. Your approved timeslot is '+response
            api.reply_message(sender,message)
            return '', 200
        else:
            slots = recommend_time_slots()
            message = 'Your prefered time is not available\nAvailable times are\n\n'

            for slot in slots:
                message = message + str(slot)

            message = message + '\n\nPlease enter your prefered time from the list of availble times.'
            api.reply_message(sender,message)
            return '', 200
    else:
        message = 'Invalid input time provided/nPlease enter your prefered time HH:MM'
        api.reply_message(sender,message)
        return '', 200

def validate_time(time_str):
    pattern = r'^([01][0-9]|2[0-3]):[0-5][0-9]$'
    if re.match(pattern, time_str):
        return True
    else:
        return False

def check_availability(preferred_time):
    slots = dbh.db['customer_queue'].find()
    for slot in slots:
        if preferred_time == slot['Time']:
            return True
    return False

def recommend_time_slots():
    available_slots = []
    for hour in range(8, 15):
        for minute in range(0, 60, 15):
            time_slot = f"{hour:02d}:{minute:02d}"
            if not check_availability(time_slot):
                available_slots.append(time_slot)
    return available_slots
    