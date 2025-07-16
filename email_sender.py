import smtplib
import html
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid
from PIL import Image
from io import BytesIO

def send_email(recipient, articles, sender_email, sender_password, weather_info, quote, exercise):
    msg = MIMEMultipart("related")
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "🔥 Today's Spark 🚀"

    # Build HTML and collect image paths + cids
    html_body, image_attachments = build_email_content(articles, weather_info, quote, exercise)

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

def build_email_content(articles, weather_info, quote, exercise):
    html_parts = []
    image_attachments = []

    html_parts.append(f"""
    <p style="font-size:18px; margin-bottom:20px;">
        <b>{weather_info}</b><br><br>
        <b>💡 Today's quote:</b> <i>{quote}</i><br><br>
        <b>📰 Your daily articles</b>
    </p>
    """)

    for index, article in enumerate(articles):
        img_html = ""
        if article.get("image") and os.path.exists(article["image"]):
            cid = make_msgid(domain='mediumagent.local')  # e.g. <1234@domain>
            image_attachments.append((article["image"], cid))
            img_html = f'<img src="cid:{cid[1:-1]}" width="600"><br>'

        html_parts.append(f"""
            {img_html}
            <p><b style="color:yellow; font-size:24px;">{html.escape(article['title'])}</b></p>
            <p><b style="color:red;">Category:</b> {html.escape(article['category'])}</p>
            <p><b style="color:green;">Summary:</b> {html.escape(article['summary'])}</p>
            <p><b style="color:blue;">Key Idea:</b> {html.escape(article['key_idea'])}</p>
            <p><b>Published:</b> {html.escape(article['published'])}</p>
            <p><b>Tags:</b> {', '.join(map(html.escape, article.get('tags', [])))}</p>
            <p><a href="{html.escape(article['link'])}">Read Full Article</a></p>
            <hr style="margin:30px 0;">
        """)

    # Format exercise: convert newlines to <br>, preserve code blocks in <pre>
    # A simple approach:
    exercise_html = "<h2>📝 Swift Algorithm Exercise of the Day</h2>"

    # Escape HTML special chars in exercise text to avoid breaking HTML
    escaped_exercise = html.escape(exercise)

    # Replace triple backticks with <pre><code> blocks for code
    # e.g. ```swift ... ``` -> <pre><code>...</code></pre>
    import re
    def code_replacer(match):
        code_content = match.group(1)
        return f'<pre style="background:#f0f0f0; padding:10px; border-radius:5px;"><code>{code_content}</code></pre>'
    escaped_exercise = re.sub(r'```(?:swift)?\n([\s\S]*?)```', code_replacer, escaped_exercise)

    # Replace remaining newlines with <br> for readability
    escaped_exercise = escaped_exercise.replace('\n', '<br>')

    exercise_html += f"<p style='font-family:monospace; font-size:14px;'>{escaped_exercise}</p>"

    html_parts.append(exercise_html)

    full_html = "<html><body style='font-family:Arial, sans-serif;'>" + "\n".join(html_parts) + "</body></html>"

    return full_html, image_attachments

def format_articles_for_whatsapp(articles):
    message = "📰 Your Daily Medium Digest\n\n"
    for article in articles:
        message += f"Title: {article['title']}\n"
        message += f"Category: {article['category']}\n"
        message += f"Summary: {article['summary']}\n"
        message += f"Key Idea: {article['key_idea']}\n"
        message += f"Link: {article['link']}\n\n"
    return message
