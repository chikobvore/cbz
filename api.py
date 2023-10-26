import requests
from paynow import Paynow

#production
api_token = 'gvrrohawtwyfm6he'
headers = {'content-type': 'application/x-www-form-urlencoded'}
api_instance_url = 'https://api.ultramsg.com/instance66456/messages/'
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



def makepayment(sender,order_no,email,package,amount,pay_number):

      paynow = Paynow(15469,'0199efc4-1967-4808-97c2-499b16a34c2d','https://tauraikatsekera.herokuapp.com/chatbot/payments', 'https://tauraikatsekera.herokuapp.com/chatbot/payments')
      payment = paynow.create_payment(order_no,email)
      payment.add(package,amount)

      response = paynow.send_mobile(payment,pay_number,'Ecocash')

      if(response.success):

            poll_url = response.poll_url
            print("Poll Url: ", poll_url)
            # Get the poll url (used to check the status of a transaction). You might want to save this in your DB
            r=requests.get(poll_url)
            actualResponse = r.text
            
            tr = actualResponse.split("&")
      
            diction = {}
            
            for string in tr:
                  values = string.split("=")
                  print(values)
                  diction[values[0]] = values[1]

            #get date
            # mytime = str(pd.to_datetime('now'))
            # mydate = mytime.split(' ')
            # mydate[0]

            message = "*Transaction Confirmation*\n*Reference number*: "+diction['paynowreference']+ "\n\n*Please note this is not a proof of payment,if your money has been deducted please note that the money will be credited at end-of-day settlement.*\n\nTo view the transaction online please follow this link\n\n"+poll_url
            reply_message(sender,message)
            return True
      else:
            message = "*Transaction Failed*"
            reply_message(sender,message)
            return False