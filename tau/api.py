import requests

#EMAIL: tau@ladsafrica.co.zw
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }

  response = requests.post("https://api.chat-api.com/instance305026/sendMessage?token=rjfobyzhzlzwr4v8", data=payload)
  return str(response.status_code)