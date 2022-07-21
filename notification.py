import requests
import smtplib
from config import conf_notification
from logger import log
from email.mime.text import MIMEText
from email.utils import formataddr

# ===== 邮件设置 =====
# 正确配置并启用后，每次填报后程序会发送电子邮件到对应账户。
# 邮件发送使用SMTP协议，可在各大电子邮箱平台找到配置方法。
mail = conf_notification["mail"]["enable"]  # 是否启用邮件
ssl = conf_notification["mail"]["ssl"]  # 是否启用SSL
host = conf_notification["mail"]["host"]  # SMTP服务器地址（如smtp.qq.com）
port = conf_notification["mail"]["port"]  # 输入SMTP服务器端口（如465）
account = conf_notification["mail"]["account"]  # 发信账号
password = conf_notification["mail"]["password"]  # 发信密码
sender = conf_notification["mail"]["sender"]  # 发信人邮箱
receiver = conf_notification["mail"]["receiver"]  # 收信人邮箱
# ===== go-cqhttp配置 =====
# 正确配置并启用后，每次填报后程序会发送QQ消息到对应收信QQ号或QQ群。
# 需要正确配置go-cqhttp(https://github.com/Mrs4s/go-cqhttp)并启用HTTP API接口。
# ！若你不知道这是什么，请不要启用！
cqhttp = conf_notification["cqhttp"]["enable"]  # 是否启用go-cqhttp发信
api = conf_notification["cqhttp"]["api"]  # cqhttp http API 地址
uid = conf_notification["cqhttp"]["uid"]  # 收信QQ号，不填则不发送
gid = conf_notification["cqhttp"]["gid"]  # 收信群号，不填则不发送


def msg(text):
    if cqhttp:
        try:
            send_cqhttp(text)
            log.info("成功发送cqhttp消息")
        except:
            log.error("发送cqhttp消息失败")
    else:
        log.info("未启用cqhttp推送")
    if mail:
        try:
            send_mail(text)
            log.info("成功发送邮件")
        except:
            log.error("发送邮件失败")
    else:
        log.info("未启用邮件发信")


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
