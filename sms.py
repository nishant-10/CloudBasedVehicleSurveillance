
import os
from twilio.rest import Client

os.environ['SID'] = 'ACf37741b2f79ca0003f3cc4c1194bdcae'
os.environ['TOK'] = '43cc53d5fd7ad866e033180787a1bc06'
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['SID']
auth_token = os.environ['TOK']
client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Driver drowsiness has been detected by the survillance system.',
    messaging_service_sid='MG7689a3caa66a71e9acf8923fb2b257bb',
    to='+918828074063'
)

print(message.sid)
