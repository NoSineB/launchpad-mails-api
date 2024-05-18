from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

mailgun_key = os.getenv("MAILGUN_KEY")
api_key = os.getenv("API_KEY")

app = FastAPI()

class Mail(BaseModel):
    api_key: str
    name: str
    email: str
    id: str

def send_simple_message(email, name, id):
    data = {
        str(email) : dict(NAME=name,ID=id)
    }
    return requests.post(
	    "https://api.eu.mailgun.net/v3/team.launchpadkerala.org/messages",
		auth=("api", mailgun_key),
		data={"from": "Team Launchpad Kerala <team@launchpadkerala.org>",
			"to": email,
			"subject": "Registration Confirmation | Launchpad Kerala 2024",
			"template": "confirmation",
			"recipient-variables": json.dumps(data)})

@app.get('/')
async def root():
    return {
        "message" : "Hello World"
    }

@app.post('/api/confirmation-mail')
async def send_mail(mail: Mail):
    mail_dict = mail.dict()
    if(mail_dict['api_key'] != api_key):
        raise HTTPException(status_code = 401, detail = "User not authorised")
    res = send_simple_message(mail_dict['email'], mail_dict['name'], mail_dict['id'])
    if res.status_code != 200:
        HTTPException(status_code= 400, detail= "Mail Failed")
    return {
        "response" :"success",
        "message" : f"Confirmation Email sent to {mail_dict['name']} at {mail_dict['email']}"
    }

    
    