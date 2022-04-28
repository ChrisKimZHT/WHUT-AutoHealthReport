from health_report import report
from notification import msg

if __name__ == "__main__":
    text = report()
    print(text)
    msg(text)
