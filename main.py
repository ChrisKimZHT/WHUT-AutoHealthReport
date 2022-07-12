from config import conf_student
from health_report import report
from notification import msg

if __name__ == "__main__":
    message = "【健康填报】v1.1.0\n"
    for user in conf_student:
        text = report(user["account"], user["password"], user["is_graduate"],
                      user["province"], user["city"], user["county"], user["street"],
                      user["is_inschool"], user["is_leacecity"], user["temperature"])
        message += text + "\n"
    message += "GitHub@ChrisKimZHT"
    msg(message)
