import os
import yaml

conf_notification = {
    "mail": {
        "enable": False,
        "ssl": False,
        "host": "",
        "port": 0,
        "account": "",
        "password": "",
        "sender": "",
        "receiver": "",
    },
    "cqhttp": {
        "enable": False,
        "api": "",
        "uid": "",
        "gid": "",
    }
}
conf_student = []


def save_config():
    all_config = {
        "notification": conf_notification,
        "student": conf_student,
    }
    try:
        with open("config.yaml", "w") as config_file:
            yaml.safe_dump(all_config, config_file, sort_keys=False)
    except:
        print("配置文件保存失败")


def load_config():
    global conf_notification, conf_student
    try:
        with open("config.yaml", "r") as config_file:
            all_config = yaml.safe_load(config_file)
        conf_notification = all_config["notification"]
        conf_student = all_config["student"]
    except:
        print("配置文件读取失败，请检查配置文件是否有格式错误")


def student_dict(global_province: str = "湖北省", global_city: str = "武汉市",
                 global_county: str = "武昌区", global_street: str = "友谊大道") -> dict:
    account = input("输入账号: ")
    password = input("输入密码: ")
    is_graduate = input("是否为研究生(Y/N，留空默认否): ")
    if is_graduate == "Y" or is_graduate == "y":
        is_graduate = True
    else:
        is_graduate = False
    province = input(f"填报省份(留空默认\"{global_province}\"): ") or global_province
    city = input(f"填报城市(留空默认\"{global_city}\"): ") or global_city
    county = input(f"填报区县(留空默认\"{global_county}\"): ") or global_county
    street = input(f"填报街道(留空默认\"{global_street}\"): ") or global_street
    temperature = input("填报温度，若要修改请与微信小程序一致(留空默认\"36.5°C~36.9°C\"): ") or "36.5°C~36.9°C"
    return {
        "account": account,
        "password": password,
        "is_graduate": is_graduate,
        "province": province,
        "city": city,
        "county": county,
        "street": street,
        "temperature": temperature,
    }


def init_config():
    print("======身份设置======")
    batch = input("是否批量填报，即一次填报多人(Y/N): ")
    if batch == "Y" or batch == "y":
        count = int(input("批量填报人数(留空默认\"1\"): ") or "1")
        print("---全局设置---\n"
              "填写后会成为默认值，方便后续每位同学的填写")
        province = input("填报省份(留空默认\"湖北省\"): ") or "湖北省"
        city = input("填报城市(留空默认\"武汉市\"): ") or "武汉市"
        county = input("填报区县(留空默认\"武昌区\"): ") or "武昌区"
        street = input("填报街道(留空默认\"友谊大道\"): ") or "友谊大道"
        for i in range(1, count + 1):
            print(f"---学生{i}---")
            conf_student.append(student_dict(province, city, county, street))
    else:
        conf_student.append(student_dict())
    print("======推送设置======")
    print("---邮件推送---\n"
          "正确配置并启用后，每次填报后程序会发送电子邮件到对应账户。\n"
          "邮件发送使用SMTP协议，可在各大电子邮箱平台找到配置方法。")
    enable_email = input("是否启用邮件推送(Y/N): ")
    if enable_email == "Y" or enable_email == "y":
        conf_notification["mail"]["enable"] = True
        ssl = input("是否启用SSL(Y/N): ")
        if ssl == "Y" or ssl == "y":
            conf_notification["mail"]["ssl"] = True
        else:
            conf_notification["mail"]["ssl"] = False
        conf_notification["mail"]["host"] = input("输入SMTP服务器地址，如smtp.qq.com: ")
        conf_notification["mail"]["port"] = int(input("输入SMTP服务器端口，如465: "))
        conf_notification["mail"]["account"] = input("输入发信账号: ")
        conf_notification["mail"]["password"] = input("输入发信密码: ")
        conf_notification["mail"]["sender"] = input("输入发信邮箱: ")
        conf_notification["mail"]["receiver"] = input("输入收信邮箱: ")
    print("---QQ推送---\n"
          "正确配置并启用后，每次填报后程序会发送QQ消息到对应收信QQ号或QQ群。\n"
          "需要正确配置go-cqhttp(https://github.com/Mrs4s/go-cqhttp)并启用HTTP API接口。\n"
          "！若你不知道cqhttp是什么，请不要启用！")
    enable_cqhttp = input("是否启用QQ推送(Y/N): ")
    if enable_cqhttp == "Y" or enable_cqhttp == "y":
        conf_notification["cqhttp"]["enable"] = True
        conf_notification["cqhttp"]["api"] = input(
            "cqhttp http API 地址(留空默认\"http://127.0.0.1:5700/send_msg\"): ") or "http://127.0.0.1:5700/send_msg"
        conf_notification["cqhttp"]["uid"] = input("收信QQ号，不填则不发送: ")
        conf_notification["cqhttp"]["gid"] = input("收信群号，不填则不发送: ")
    print("======设置完成======")
    save_config()
    print("======保存完成======")


if os.path.exists("config.yaml"):
    load_config()
else:
    print("未发现配置文件，进行配置文件初始化")
    init_config()
