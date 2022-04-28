import requests
import json
import base64

# 在此填写账号密码，账号通常为学号，密码通常为身份证后6位。注意：需要解绑微信
account = ""
password = ""

# http请求头
headers = {
    "Host": "zhxg.whut.edu.cn",
    "Connection": "keep-alive",
    # "Content-Length": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "X-Tag": "flyio",
    "content-type": "application/json",
    "encode": "true",
    "Referer": "https://servicewechat.com/wxa0738e54aae84423/21/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br"
}

log = ""  # 返回信息
result = []  # 结果


# 获取SessionID
# https://zhxg.whut.edu.cn/yqtjwx/api/login/checkBind
def check_bind():
    global headers
    global log
    url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/checkBind"
    data = dict_to_base64_bin({"sn": None, "idCard": None})
    respounce = requests.post(url=url, headers=headers, data=data).json()
    log += f"获取SessionID-返回消息：{respounce}\n"
    resp_data = base64_str_to_dict(respounce["data"])
    log += f"获取SessionID-data解码：{resp_data}\n"
    headers["Cookie"] = f"JSESSIONID={resp_data['sessionId']}"  # 写入Cookie


# 绑定身份
# https://zhxg.whut.edu.cn/yqtjwx/api/login/bindUserInfo
def bind_user_info():
    global log
    url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/bindUserInfo"
    data = dict_to_base64_bin({"sn": account, "idCard": password})
    respounce = requests.post(url=url, headers=headers, data=data).json()
    log += f"绑定身份-返回消息：{respounce}\n"
    resp_data = base64_str_to_dict(respounce["data"])
    log += f"绑定身份-data解码：{resp_data}\n"


# 健康填报
# https://zhxg.whut.edu.cn/yqtjwx/./monitorRegister
def monitor_register(province, city, county, street):
    global log
    global result
    address = province + city + county + street
    url = "https://zhxg.whut.edu.cn/yqtjwx/./monitorRegister"
    dict_data = {
        "diagnosisName": "",
        "relationWithOwn": "",
        "currentAddress": address,
        "remark": "无",
        "healthInfo": "正常",
        "isDiagnosis": "0",
        "isFever": "0",
        "isInSchool": "1",
        "isLeaveChengdu": "0",
        "isSymptom": "0",
        "temperature": "36.5°C~36.9°C",
        "province": province,
        "city": city,
        "county": county
    }
    data = dict_to_base64_bin(dict_data)
    respounce = requests.post(url=url, headers=headers, data=data).json()
    log += f"健康填报-返回消息：{respounce}\n"
    result = [respounce["status"], respounce["message"]]


# 解绑：若不解绑，下次将无法绑定
# https://zhxg.whut.edu.cn/yqtjwx/api/login/cancelBind
def cancel_bind():
    global log
    url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/cancelBind"
    respounce = requests.post(url=url, headers=headers).json()
    log += f"解绑-返回消息：{respounce}\n"
    resp_data = base64_str_to_dict(respounce["data"])
    log += f"解绑-data解码：{resp_data}\n"


def dict_to_base64_bin(data: dict) -> bin:
    string = json.dumps(data)
    binary = string.encode()
    base64_binary = base64.b64encode(binary)
    return base64_binary


def base64_str_to_dict(data: str) -> dict:
    string_binary = base64.b64decode(data)
    string = string_binary.decode()
    dictionary = json.loads(string)
    return dictionary


def report():
    check_bind()
    try:
        bind_user_info()
        monitor_register("湖北省", "武汉市", "武昌区", "友谊大道")
    finally:
        cancel_bind()
    if result[0]:
        return "填报成功，返回消息：\n" + result[1]
    else:
        return "填报失败，详细日志：\n" + log
