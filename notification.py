import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# ===== 邮件设置 =====
# 正确配置并启用后，每次填报后程序会发送电子邮件到对应账户。
# 邮件发送使用SMTP协议，可在各大电子邮箱平台找到配置方法。
mail = False  # 是否启用邮件
ssl = True  # 是否启用SSL
host = ""  # SMTP服务器地址（如smtp.qq.com）
port = 465  # 输入SMTP服务器端口（如465）
account = ""  # 发信账号
password = ""  # 发信密码
sender = ""  # 发信人邮箱
receiver = ""  # 收信人邮箱
# ===== go-cqhttp配置 =====
# 正确配置并启用后，每次填报后程序会发送QQ消息到对应收信QQ号或QQ群。
# 需要正确配置go-cqhttp(https://github.com/Mrs4s/go-cqhttp)并启用HTTP API接口。
# ！若你不知道这是什么，请不要启用！
cqhttp = False  # 是否启用go-cqhttp发信
api = "http://127.0.0.1:5700/send_msg"  # cqhttp http API 地址
uid = ""  # 收信QQ号，不填则不发送
gid = ""  # 收信群号，不填则不发送


def msg(text):
    if cqhttp:
        send_cqhttp(text)
    if mail:
        send_mail(text)


def send_cqhttp(text):
    data_user = {
        "user_id": uid,
        "message": text
    }
    data_group = {
        "group_id": gid,
        "message": text
    }
    if data_user["user_id"] != "":
        requests.get(api, params=data_user)
    if data_group["group_id"] != "":
        requests.get(api, params=data_group)


def send_mail(text):
    if ssl:
        server = smtplib.SMTP_SSL(host, port)
    else:
        server = smtplib.SMTP(host, port)
    server.login(account, password)
    mail_msg = MIMEText(text, "plain", "utf-8")
    mail_msg["From"] = formataddr(["WHUT-AutoHealthReport", sender])
    mail_msg["Subject"] = "【WHUT-AutoHealthReport】"
    server.sendmail(sender, receiver, mail_msg.as_string())
    server.close()
