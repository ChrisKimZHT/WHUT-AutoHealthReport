# WHUT-AutoHealthReport

通过访问学校健康填报接口，模拟健康填报过程，并且通过 cqhttp 发送结果到 QQ 号，或通过邮件发送结果到指定邮箱。

配置方法非常简单，只需填写填写相关信息，即可健康填报并发送结果消息。

配置完成后，可通过 crontab 等手段定时运行 `main.py`，即可每日自动填报。

### 使用方法

1. 在 `health_report.py` 中填写账号、密码、填报地址、填报体温。
2. 在 `notification.py` 中填写你需要的发信方式，支持 cqhttp 和邮件。
3. 定时运行 `main.py` 即可。

### 所需模块

- requests
    - `pip install requests`

### 警告

该自动填报程序仅为了方便每日填报过程，严禁通过该程序伪造填报地址、健康状态。**若使用该程序导致不良后果，使用者需承担所有责任！**

强烈建议将该程序自动运行时间改为起床后，若起床发现体温异常等身体不适，请立即关闭该天的定时运行，手动如实填写身体状况！

### 鸣谢

程序有借鉴 [xiaozhangtongx/WHUT-JKRBTB](https://github.com/xiaozhangtongx/WHUT-JKRBTB)
，因学校给每次的请求都进行了base64编码，因此该程序已经失效，我重新抓包重构了该程序。在此感谢原作者。
