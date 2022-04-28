import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# ===== cqhttp配置 =====
cqhttp = False  # 是否启用cqhttp
api = "http://127.0.0.1:5700/send_msg"  # cqhttp http API 地址
uid = ""  # 收信QQ号
# ===== 邮件设置 =====
mail = False  # 是否启用邮件
ssl = True  # 是否启用SSL
host = ""  # SMTP服务器地址（如smtp.qq.com）
port = 465  # 输入SMTP服务器端口（如465）
account = ""  # 发信账号
password = ""  # 发信密码
sender = ""  # 发信人邮箱
receiver = ""  # 收信人邮箱


def msg(text):
    if cqhttp:
        send_cqhttp(text)
    if mail:
        send_mail(text)


def send_cqhttp(text):
    data = {
        "user_id": uid,
        "message": text
    }
    requests.get(api, params=data)


def send_mail(text):
    if ssl:
        server = smtplib.SMTP_SSL(host, port)
    else:
        server = smtplib.SMTP_SSL(host, port)
    server.login(account, password)
    mail_msg = MIMEText(text, "plain", "utf-8")
    mail_msg["From"] = formataddr(["WHUT-AutoHealthReport", sender])
    mail_msg["Subject"] = "【WHUT-AutoHealthReport】"
    server.sendmail(sender, receiver, mail_msg.as_string())
    server.close()
