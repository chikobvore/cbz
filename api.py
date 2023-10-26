import requests
from paynow import Paynow

#production
api_token = 'euetd8rpfnfzcz1m'
headers = {'content-type': 'application/x-www-form-urlencoded'}
api_instance_url = 'https://api.ultramsg.com/instance66488/messages/'
#https://lochichabot.herokuapp.com/

def reply_message(sender,message):

      message = message.encode('utf8').decode('latin-1')
      payload = "token="+api_token+"&to="+sender+"&body="+str(message)+"&priority=10&referenceId="
      response = requests.request("POST",api_instance_url+'chat', data=payload, headers=headers)

      return True

def send_attachment(sender,attachment_url,caption):
      caption = caption.encode('utf8').decode('latin-1')
      payload = "token="+api_token+"&to="+sender+"&document="+attachment_url+"&filename="+caption+"&referenceId=&nocache="
      response = requests.request("POST", api_instance_url+'document', data=payload, headers=headers)

      return True

def send_image(sender,attachment_url,caption):
      caption = caption.encode('utf8').decode('latin-1')
      payload = "token="+api_token+"&to="+sender+"&image="+attachment_url+"&caption="+caption+"&referenceId=&nocache="
      response = requests.request("POST", api_instance_url+'image', data=payload, headers=headers)

      return True
def send_sms(sender,message):
      SenderID ='CBZ PULSE'
      url_string = 'senderid='+SenderID+'&&user=Unlock&password=Unl106@&mobiles='+sender+'&sms='+message
      response = requests.request("GET",'https://smsportal.vas.co.zw/teleoss/sendsms.jsp?'+url_string)
      return True

def get_part_of_day(h):
      h = h + 2
      if 0 < h <= 11:
            return "*morning* " +str('🌅')
      elif 12 < h <= 17:
            return "*afternoon* " + str('🌞')
      elif 18 < h <= 23:
            return "*evening* " + str('🌇')
      else:
            return "*day*" + str('🌠') 


def send_sms(sender,message):
      SenderID ='CBZ PULSE'
      url_string = 'senderid='+SenderID+'&&user=Unlock&password=Ulc109@&mobiles='+sender+'&sms='+message
      response = requests.request("GET",'https://smsportal.vas.co.zw/teleoss/sendsms.jsp?'+url_string)
      return True