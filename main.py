from health_report import report
from notification import msg

# 在此填写账号密码，账号通常为学号，密码通常为身份证后6位，可添加更多用户。注意：需要解绑微信
user_list = [
    {"account": "", "password": ""},
    # {"account": "", "password": ""},
    # {"account": "", "password": ""},
    # {"account": "", "password": ""},
]

if __name__ == "__main__":
    for user in user_list:
        text = report(user["account"], user["password"])
        msg(text)
