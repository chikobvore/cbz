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
from datetime import datetime, timedelta
def addque(sender,response,service):

    if validate_time(response):
        response = round_to_nearest_15(response)
        details = dbh.db['customers'].find_one({"Sender": sender})
        sh.session_status(sender,'0','0')
        if check_availability(response):
            record = {
                "Sender": sender,
                "Full_name": details['Full_name'],
                "Service": service,
                "Time": response,
                }
            dbh.db['customer_queue'].insert_one(record)
            query_id = random.randint(1000,9999)
            message = 'Your request have been successfully logged,Your request id is *'+service+':'+str(query_id)+'* . Your approved timeslot is '+response
            api.send_sms(sender,message)
            api.reply_message(sender,message)
            return '', 200
        else:
            
            slots = recommend_time_slots()
            message = 'Your prefered time is not available\nAvailable times are\n\n'

            for slot in slots:
                message = message + str(slot) + '\n'

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
            return False
    return True

def recommend_time_slots():
    available_slots = []
    for hour in range(8, 15):
        for minute in range(0, 60, 15):
            time_slot = f"{hour:02d}:{minute:02d}"
            if check_availability(time_slot):
                available_slots.append(time_slot)
    return available_slots

def round_to_nearest_15(time_str):
    time = datetime.strptime(time_str, "%H:%M")
    minutes = (time.minute // 15) * 15
    rounded_time = time.replace(minute=minutes, second=0, microsecond=0)
    return rounded_time.strftime("%H:%M")