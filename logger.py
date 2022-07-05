import logging

# 创建log
log = logging.getLogger("log.txt")
log.setLevel(logging.DEBUG)
# 控制台输出Handler
shandler = logging.StreamHandler()
shandler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
shandler.setLevel(logging.INFO)
# 文件输出Handler
fhandler = logging.FileHandler(filename="log.txt", mode="w", encoding="utf-8")
fhandler.setFormatter(logging.Formatter("<%(asctime)s> [%(levelname)s] %(message)s"))
fhandler.setLevel(logging.DEBUG)
# 添加Handler
log.addHandler(shandler)
log.addHandler(fhandler)
