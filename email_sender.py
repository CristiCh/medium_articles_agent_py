import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid
# import pywhatkit
import time
import os
from PIL import Image
from io import BytesIO

def send_email(recipient, articles, sender_email, sender_password, weather_info):
    msg = MIMEMultipart("related")
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "📰🔥 Today’s Top Medium Picks"

    # Build HTML and collect image paths + cids
    html_body, image_attachments = build_email_content(articles, weather_info)

    # Attach HTML
    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)
    msg_alternative.attach(MIMEText(html_body, "html"))

    # Attach resized images
    for image_path, cid in image_attachments:
        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                img.thumbnail((400, 400))  # Resize keeping aspect ratio
                img_bytes = BytesIO()
                img.save(img_bytes, format="JPEG", quality=85)
                img_bytes.seek(0)

                mime_img = MIMEImage(img_bytes.read(), _subtype="jpeg")
                mime_img.add_header('Content-ID', cid)
                mime_img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
                msg.attach(mime_img)
        except Exception as e:
            print(f"Failed to process and attach image {image_path}: {e}")

    # Send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


def build_email_content(articles, weather_info):
    html_parts = []
    image_attachments = []

    html_parts.append(f"""
    <p style="font-size:18px; margin-bottom:20px;">
    <b>🌤 Weather in Cluj-Napoca today:</b> {weather_info}</p>
    """)

    for index, article in enumerate(articles):
        img_html = ""
        if article.get("image") and os.path.exists(article["image"]):
            cid = make_msgid(domain='mediumagent.local')  # e.g. <1234@domain>
            image_attachments.append((article["image"], cid))
            img_html = f'<img src="cid:{cid[1:-1]}" width="600"><br>'

        html_parts.append(f"""
            {img_html}
            <p><b style="color:yellow; font-size:24px;">{article['title']}</b></p>
            <p><b style="color:red;">Category:</b> {article['category']}</p>
            <p><b style="color:green;">Summary:</b> {article['summary']}</p>
            <p><b style="color:blue;">Key Idea:</b> {article['key_idea']}</p>
            <p><b>Published:</b> {article['published']}</p>
            <p><b>Tags:</b> {', '.join(article.get('tags', []))}</p>
            <p><a href="{article['link']}">Read Full Article</a></p>
            <hr style="margin:30px 0;">
        """)

    return "<html><body style='font-family:Arial, sans-serif;'>" + "\n".join(html_parts) + "</body></html>", image_attachments


# def send_email(recipient, articles, sender_email, sender_password):
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient
#     msg['Subject'] = "📰🔥 Today’s Top Medium Picks"

#     body = ""
#     for article in articles:
#         body += f"<h3>{article['title']}</h3><br>"
#         body += f"<b style='color: red;'>Category:</b> {article['category']}<br><br>"
#         body += f"<b style='color: green;'>Summary:</b> {article['summary']}<br><br>"
#         body += f"<b style='color: blue;'>Key Idea:</b> {article['key_idea']}<br><br>"
#         body += f"<b>Published:</b> {article['published']}<br><br>"
#         body += f"<b>Tags:</b> {article['tags']}<br><br>"
#         body += f"<a href='{article['link']}'>Read Full Article</a><hr><br>"

#     msg.attach(MIMEText(body, 'html'))

#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(msg)

# def send_whatsapp_message(phone_number, message):
#     # Sends message instantly; the user needs to scan WhatsApp Web QR code at first run
#     # Scheduled to send 1 minute from now to allow time for WhatsApp Web to open
#     from datetime import datetime, timedelta
#     now = datetime.now() + timedelta(minutes=1)
#     hour = now.hour
#     minute = now.minute
#     message1 = format_articles_for_whatsapp(message)

#     pywhatkit.sendwhatmsg(phone_number, message1, hour, minute, wait_time=10, tab_close=True)

def format_articles_for_whatsapp(articles):
    message = "📰 Your Daily Medium Digest\n\n"
    for article in articles:
        message += f"Title: {article['title']}\n"
        message += f"Category: {article['category']}\n"
        message += f"Summary: {article['summary']}\n"
        message += f"Key Idea: {article['key_idea']}\n"
        message += f"Link: {article['link']}\n\n"
    return message
