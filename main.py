import time
from config import conf_student
from health_report import report_by_dict
from notification import msg

if __name__ == "__main__":
    message = "【健康填报】v1.2.0\n"
    for user in conf_student:
        text = ""
        for _ in range(1, 4):  # 重试三次
            time.sleep(3)
            status, text = report_by_dict(user)
            if status:
                message += text + "\n"
                break
        else:  # 若三次都失败
            message += text + "\n"
    message += "GitHub@ChrisKimZHT"
    msg(message)
