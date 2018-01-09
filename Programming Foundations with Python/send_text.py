from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC14c05494b5899380466ab9317c8a9ce5"
auth_token = "9ae89a078b49135284acf33dc0506207"
client = Client(account_sid, auth_token)

message = client.messages.create(
        "+46765887101",
        body="Test",
        from_="+46769446877",
        )

print(message.sid)
