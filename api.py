import requests

#EMAIL: tau@ladsafrica.co.zw
def reply_message(sender,message):
  payload = {
        "phone": sender,
        "body": message
        }

  response = requests.post("https://api.chat-api.com/instance315523/sendMessage?token=j3sn7u4f0mv5plbf", data=payload)
  return str(response.status_code)

def send_attachment(sender,attachment_url,caption):
      payload = {
            "phone": sender,
            "filename": attachment_url,
            "caption": caption,
            "body": attachment_url
      }
      response = requests.post("https://api.chat-api.com/instance315523/sendFile?token=j3sn7u4f0mv5plbf", data=payload)
      return str(response.status_code)
