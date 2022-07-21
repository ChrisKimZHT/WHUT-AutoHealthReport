import requests
import json
import base64
import random
from logger import log

# User-Agent列表 分别是Android微信、iOS微信、PC微信
ua_list = [
    "Mozilla/5.0 (Linux; Android 11; POCO F2 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MMWEBID/1230 MicroMessenger/8.0.17.2040(0x28001133) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x1800142f) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
]

# http请求头
headers = {
    # "Host": "",
    "Connection": "keep-alive",
    # "Content-Length": "",
    # "User-Agent": "",
    "X-Tag": "flyio",
    "content-type": "application/json",
    "encode": "true",
    "Referer": "https://servicewechat.com/wxa0738e54aae84423/21/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br"
}

error_log = ""


# 获取SessionID
# https://zhxg.whut.edu.cn/yqtjwx/api/login/checkBind
# https://yjsxx.whut.edu.cn/wx/api/login/checkBind
def check_bind(is_graduate: bool) -> bool:
    global error_log
    log.info("[1] 正在创建会话")
    # 设置header
    if is_graduate:
        url = "https://yjsxx.whut.edu.cn/wx/api/login/checkBind"
        headers["Host"] = "yjsxx.whut.edu.cn"
    else:
        url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/checkBind"
        headers["Host"] = "zhxg.whut.edu.cn"
    headers["User-Agent"] = random.choice(ua_list)
    log.debug(f"设置header完成: {headers}")
    data = dict_to_base64_bin({"sn": None, "idCard": None})
    respounce = requests.post(url=url, headers=headers, data=data).json()
    log.debug(f"请求发送完成，收到响应: {respounce}")
    if respounce["status"]:
        resp_data = base64_str_to_dict(respounce["data"])
        log.debug(f"响应data解码: {resp_data}")
        headers["Cookie"] = f"JSESSIONID={resp_data['sessionId']}"  # 写入Cookie
        return True
    else:
        error_log += str(respounce)
        log.error("[X] 创建会话出现错误，详情见log.txt")
        return False


# 绑定身份
# https://zhxg.whut.edu.cn/yqtjwx/api/login/bindUserInfo
# https://yjsxx.whut.edu.cn/wx/api/login/bindUserInfo
def bind_user_info(account: str, password: str, is_graduate: bool) -> bool:
    global error_log
    log.info("[2] 正在绑定身份")
    if is_graduate:
        url = "https://yjsxx.whut.edu.cn/wx/api/login/bindUserInfo"
    else:
        url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/bindUserInfo"
    data = dict_to_base64_bin({"sn": account, "idCard": password})
    respounce = requests.post(url=url, headers=headers, data=data).json()
    log.debug(f"请求发送完成，收到响应: {respounce}")
    if respounce["status"]:
        resp_data = base64_str_to_dict(respounce["data"])
        log.debug(f"响应data解码: {resp_data}")
        return True
    else:
        error_log += str(respounce)
        log.error("[X] 绑定身份出现错误，详情见log.txt")
        return False


# 健康填报
# https://zhxg.whut.edu.cn/yqtjwx/./monitorRegister
# https://yjsxx.whut.edu.cn/wx/./monitorRegister
def monitor_register(is_graduate: bool, province: str, city: str, county: str, street: str,
                     is_inschool: bool, is_leavecity: bool, temperature: str) -> bool:
    global error_log
    log.info("[3] 正在填报操作")
    address = province + city + county + street
    if is_graduate:
        url = "https://yjsxx.whut.edu.cn/wx/./monitorRegister"
    else:
        url = "https://zhxg.whut.edu.cn/yqtjwx/./monitorRegister"
    dict_data = {
        "diagnosisName": "",
        "relationWithOwn": "",
        "currentAddress": address,
        "remark": "无",
        "healthInfo": "正常",
        "isDiagnosis": "0",
        "isFever": "0",
        "isInSchool": str(int(is_inschool)),
        "isLeaveChengdu": str(int(is_leavecity)),
        "isSymptom": "0",
        "temperature": temperature,
        "province": province,
        "city": city,
        "county": county
    }
    log.debug(f"填报数据生成完成: {dict_data}")
    data = dict_to_base64_bin(dict_data)
    respounce = requests.post(url=url, headers=headers, data=data).json()
    log.debug(f"请求发送完成，收到响应: {respounce}")
    if respounce["status"]:
        resp_data = base64_str_to_dict(respounce["data"])
        log.debug(f"响应data解码: {resp_data}")
        return True
    else:
        error_log += str(respounce)
        log.error("[X] 填报操作出现错误，详情见log.txt")
        return False


# 解绑：若不解绑，下次将无法绑定
# https://zhxg.whut.edu.cn/yqtjwx/api/login/cancelBind
# "https://zhxg.whut.edu.cn/yqtjwx/api/login/cancelBind"
def cancel_bind(is_graduate: bool) -> bool:
    global error_log
    log.info("[4] 正在解绑身份")
    if is_graduate:
        url = "https://yjsxx.whut.edu.cn/wx/api/login/cancelBind"
    else:
        url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/cancelBind"
    respounce = requests.post(url=url, headers=headers).json()
    log.debug(f"请求发送完成，收到响应: {respounce}")
    if respounce["status"]:
        resp_data = base64_str_to_dict(respounce["data"])
        log.debug(f"响应data解码: {resp_data}")
        return True
    else:
        error_log += str(respounce)
        log.error("[X] 解绑身份出现错误，详情见log.txt")
        return False


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


def report(account: str, password: str, is_graduate: bool,
           province: str, city: str, county: str, street: str,
           is_inschool: bool, is_leacecity: bool, temperature: str) -> tuple:
    global error_log
    log.debug(f"开始填报: {account}")
    status = True  # 填报状态
    headers["Cookie"] = ""  # 重置headers
    error_log = ""  # 重置错误日志
    try:
        if not (check_bind(is_graduate) and
                bind_user_info(account, password, is_graduate) and
                monitor_register(is_graduate, province, city, county, street, is_inschool, is_leacecity, temperature)):
            status = False
    finally:
        status &= cancel_bind(is_graduate)
    if status:
        log.info(f"学生{account}填报成功")
        return True, f"学生 {account} 填报成功！"
    else:
        log.error(f"学生{account}填报失败")
        return False, f"学生 {account} 填报失败！\n" + error_log


def report_by_dict(user: dict) -> tuple:  # 一层套娃而已
    return report(user["account"], user["password"], user["is_graduate"],
                  user["province"], user["city"], user["county"], user["street"],
                  user["is_inschool"], user["is_leacecity"], user["temperature"])
