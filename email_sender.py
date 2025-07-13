import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pywhatkit
import time

def send_email(recipient, articles, sender_email, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "📰🔥 Today’s Top Medium Picks"

    body = ""
    for article in articles:
        body += f"<h3>{article['title']}</h3><br>"
        body += f"<b style='color: red;'>Category:</b> {article['category']}<br><br>"
        body += f"<b style='color: green;'>Summary:</b> {article['summary']}<br><br>"
        body += f"<b style='color: blue;'>Key Idea:</b> {article['key_idea']}<br><br>"
        body += f"<b>Published:</b> {article['published']}<br><br>"
        body += f"<b>Tags:</b> {article['tags']}<br><br>"
        body += f"<a href='{article['link']}'>Read Full Article</a><hr><br>"

    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def send_whatsapp_message(phone_number, message):
    # Sends message instantly; the user needs to scan WhatsApp Web QR code at first run
    # Scheduled to send 1 minute from now to allow time for WhatsApp Web to open
    from datetime import datetime, timedelta
    now = datetime.now() + timedelta(minutes=1)
    hour = now.hour
    minute = now.minute
    message1 = format_articles_for_whatsapp(message)

    pywhatkit.sendwhatmsg(phone_number, message1, hour, minute, wait_time=10, tab_close=True)

def format_articles_for_whatsapp(articles):
    message = "📰 Your Daily Medium Digest\n\n"
    for article in articles:
        message += f"Title: {article['title']}\n"
        message += f"Category: {article['category']}\n"
        message += f"Summary: {article['summary']}\n"
        message += f"Key Idea: {article['key_idea']}\n"
        message += f"Link: {article['link']}\n\n"
    return message