from health_report import report_multi
from notification import msg

if __name__ == "__main__":
    text = report_multi()
    msg(text)
