from twilio.rest import Client 
from qfit.settings import TWILIO_CODE
 
account_sid = 'AC7727dd61dab28c7a073c7702515da0e8' 
auth_token = TWILIO_CODE 
client = Client(account_sid, auth_token) 
 
message = client.messages.create(to='+77011242693', body="ХАЙ", messaging_service_sid="MG6ab91f013109df58bc4811e674231c85") 

print(message.sid)