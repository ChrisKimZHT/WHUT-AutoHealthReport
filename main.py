from logger import log
from config import conf_student
from health_report import report_by_dict
from notification import msg
import time

if __name__ == "__main__":
    log.info("======程序启动=======")
    message = "【健康填报】[自动反馈]\n"
    for user in conf_student:
        text = ""
        log.info(f"==={user['account']}===")
        for retry in range(1, 4):  # 重试三次
            time.sleep(3)
            log.info(f"---第{retry}次尝试---")
            status, text = report_by_dict(user)
            if status:
                message += text + "\n"
                break
        else:  # 若三次都失败
            message += text + "\n"
    message += "GitHub@kmoonn"
    log.info("=======消息推送=======")
    log.debug("待推送消息:\n" + message)
    msg(message)
