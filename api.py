import requests

api_instance_url = 'https://api.chat-api.com/instance350843'
api_token = 'z5juamogjbjj9yih'

#EMAIL: chigumbubyron@gmail.com
def reply_message(sender,message):

      payload = {
            "phone": sender,
            "body": message
            }

      response = requests.post( api_instance_url+"/sendMessage?token="+api_token, data=payload)
      return str(response.status_code)

def send_attachment(sender,attachment_url,caption):
      
      payload = {
            "phone": sender,
            "filename": caption,
            "caption": caption,
            "body": attachment_url
      }
      response = requests.post(api_instance_url+"/sendFile?token="+api_token, data=payload)
      return str(response.status_code)
