import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_email_notification(subject, body_text):
    """發送 Email 的函式"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject

        # 加入內文
        msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
        msg.attach(MIMEText("\nhttps://tradead.tixplus.jp/wbc2026", 'plain', 'utf-8'))

        # 連線到 SMTP Server 發送
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email 通知發送成功！")
    except Exception as e:
        print(f"❌ Email 發送失敗: {e}")