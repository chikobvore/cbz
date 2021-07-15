import requests

#EMAIL: tau@ladsafrica.co.zw
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }

  response = requests.post("https://api.chat-api.com/instance265454/sendMessage?token=7krlsiflsx994ms4", data=payload)
  return str(response.status_code)