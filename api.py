import requests

#EMAIL: tau@ladsafrica.co.zw
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }

  response = requests.post(" https://api.chat-api.com/instance313121/sendMessage?token=rl2kp4l061iae12j", data=payload)
  return str(response.status_code)