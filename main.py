import smtplib 
import email
import imaplib
from fastapi import FastAPI # importing fastapi for creating the API
from email.message import EmailMessage
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # Importing CORS middleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

email_address="++++++++++++++++" 
password = "+++++++++++++" 
class EmailSchma(BaseModel):
    to:str
    subject:str
    body:str

def send_email_func(to,subject,body):
    msg=EmailMessage()
    msg["From"]=email_address
    msg["To"]=to
    msg["subject"]=subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(email_address,password)
        smtp.send_message(msg)
def get_email():
    mail=imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_address,password)
    mail.select("inbox")

    _, data=mail.search(None,"ALL")
    emails_ids=data[0].split()[-5:]
    emails=[]
     
    for i in emails_ids:
        _, msg_data =mail.fetch(i,"(RFC822)")
        raw_emails = msg_data[0][1]
        msg = email.message_from_bytes(raw_emails)

        body=""
        emails.append({
            "from": msg["From"],
            "subject": msg["Subject"],
            "body": body,
        })            

    return emails

def delete_email(email_ids):
  mail=imaplib.IMAP4_SSL("imap.gmail.com")
  mail.login(email_address,password)
  mail.select("inbox")
  

  _, data=mail.search(None,"ALL")
  eamils_ids=data[0].split()[-5:]

  lasemails=email_ids[-1]
  mail.store(laseemails, '+FLAGS', '\\Deleted')
  mail.expunge()

@app.get("/emails")
def get_emails():
    try:
        emails = get_email()
        return {"emails": emails}
    except Exception as e:
        return {"error": str(e)}
@app.get("/")
def root():
   return {"message":"hello world"}

@app.post("/sendemail")
def send_email(emaill:EmailSchma):
    try:
        send_email_func(emaill.to,emaill.subject,emaill.body)
        return {"message":"email sent successfully"}
    except Exception as e:
        return {"message":"failed to send email"}
    
@app.delete("/deleteemail")
def delete_email(email_ids: list[int]):
    try:
        delete_email(email_ids)
        return {"message": "Email deleted successfully"}
    except Exception as e:
        return {"message": "Failed to delete email"}