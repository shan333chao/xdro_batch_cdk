import os
import pathlib
import json
from loguru import logger
import PhontBands

# 启动数量
START_COUNT = 15
# 启动时间间隔秒
WAIT_SECONDS = 20
# 运行分钟数
RUN_MINUTE = 45
# 排除不跑的
EXCEPT_INDEX = []
MAX_SERVER_COUNT = 140
CONFIG_NAME = "conf.dll"
LSCONSOLE = ""

import random


def get_phone_num():
    second_spot = random.choice([3, 5, 8])
    third_spot = {3: random.randint(0, 9),
                  4: random.choice([5, 7, 9]),
                  5: random.choice([i for i in range(10) if i != 4]),
                  7: random.choice([i for i in range(10) if i not in [4, 9]]),
                  8: random.randint(0, 9), }[second_spot]
    remain_spot = random.randint(9999999, 100000000)
    phone_num = "1{}{}{}".format(second_spot, third_spot, remain_spot)
    return phone_num


def init_config():
    conf = get_lsplayer_path()
    init_conf(conf)
    global LSCONSOLE
    LSCONSOLE = conf["InstallDir"] + "\\ldconsole.exe"
    logger.info(LSCONSOLE)
    logger.info("加载:{}", MAX_SERVER_COUNT)


def init_conf(conf):
    # 启动数量
    global START_COUNT
    START_COUNT = conf["START_COUNT"]
    # 启动时间间隔秒
    global WAIT_SECONDS
    WAIT_SECONDS = conf["WAIT_SECONDS"]
    # 运行分钟数
    global RUN_MINUTE
    RUN_MINUTE = conf["RUN_MINUTE"]
    # 排除不跑的
    global EXCEPT_INDEX
    EXCEPT_INDEX = conf["EXCEPT_INDEX"]

    global MAX_SERVER_COUNT
    MAX_SERVER_COUNT = conf["MAX_SERVER_COUNT"]
    logger.info("启动配置初始化完成")
    logger.info("模拟器数量:{}", MAX_SERVER_COUNT)


def get_lsplayer_path():
    if not os.path.exists(CONFIG_NAME):
        logger.error("conf file is not exist")
        exit()

    with open(CONFIG_NAME, 'r', encoding='utf-8') as f:
        logger.info("加载启动配置")
        return json.load(f)



def main():
    init_config()
    all_phone_count = len(PhontBands.BANDS_ARR)
    for i in range(0, MAX_SERVER_COUNT+1):
        phone_type = PhontBands.BANDS_ARR[random.randint(0, all_phone_count)]
        pnumber = get_phone_num()
        logger.info(
            f"{LSCONSOLE} modify --index {i} --cpu 2 --memory 3072  --imei auto  --androidid auto --mac auto --simserial auto  --pnumber {pnumber} --manufacturer {phone_type[1]} --model '{phone_type[0]}' --resolution 960,540,160")
        os.system(f"{LSCONSOLE} modify --index {i} --cpu 2 --memory 3072  --imei auto  --androidid auto --mac auto --simserial auto  --pnumber {pnumber} --manufacturer {phone_type[1]} --model {phone_type[0]} --resolution 960,540,160")

if __name__ == "__main__":
    main()
