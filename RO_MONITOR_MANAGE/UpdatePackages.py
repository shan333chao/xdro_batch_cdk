# -*- coding:utf8 -*-
import base64
import json
import os
import subprocess
import time

import requests
from loguru import logger
import queue
import pathlib
import wget

# 启动数量
START_COUNT = 15
# 启动时间间隔秒
WAIT_SECONDS = 20
# 运行分钟数
RUN_MINUTE = 45
# 排除不跑的
EXCEPT_INDEX = []
PKG_KEY = "TEST"
PKG_API = "http://0.0.0.0:5053/pkg"
ACCOUNT_SERVER = "http://127.0.0.1:23333/account/get"

game_package_name = 'com.xd.ro.roapk'
script_package_name = 'com.god.doy'
package_file_name = 'com.god.doy.apk'
LSCONSOLE = ''

q = queue.Queue(maxsize=500)
CONFIG_NAME = "conf.dll"

current_folder = os.path.dirname(__file__)
package_file = str(pathlib.Path(current_folder, package_file_name).absolute())


def init_server():
    conf = get_lsplayer_path()
    init_conf(conf)
    logger.info(package_file)
    global LSCONSOLE
    LSCONSOLE = conf["InstallDir"] + "\\ldconsole.exe"
    logger.info(LSCONSOLE)
    logger.info("加载:{}", MAX_SERVER_COUNT)
    for index in range(1, MAX_SERVER_COUNT + 1):
        q.put(index)


def sort_windows():
    os.system(f"{LSCONSOLE} sortWnd")


def get_player_states():
    p = subprocess.Popen(f"{LSCONSOLE} list2",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         )
    result = p.communicate()[0]
    test_res = result.decode('gb2312')
    all_players = test_res.split("\r\n")
    return all_players


def quit_all_player():
    logger.info("正在退出当前运行的模拟器")
    os.system(f"{LSCONSOLE} quitall")
    time.sleep(5)
    logger.info("执行关闭模拟器，等待系统显存和内存释放")
    os.system("taskkill /f /im dnplayer.exe")
    os.system("taskkill /f /im LdVBoxHeadless.exe")
    os.system("taskkill /f /im LdVBoxSVC.exe")
    time.sleep(10)
    logger.success("所有模拟器退出完成")


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

    global PKG_KEY
    PKG_KEY = conf["PKG_KEY"]
    global PKG_API
    PKG_API = conf["PKG_API"]

    global ACCOUNT_SERVER
    ACCOUNT_SERVER = conf["ACCOUNT_SERVER"]
    logger.info("启动配置初始化完成")


def get_lsplayer_path():
    if not os.path.exists(CONFIG_NAME):
        logger.error("conf file is not exist")
        exit()

    with open(CONFIG_NAME, 'r', encoding='utf-8') as f:
        logger.info("加载启动配置")
        return json.load(f)


def get_index():
    start_array = []
    for index in range(0, START_COUNT):
        if q.qsize() > 0:
            current_index = q.get_nowait()
            start_array.append(current_index)
    return start_array


def android_loop():
    index_arr = get_index()
    if len(index_arr) == 0:
        logger.info("所有模拟器更新完成")
        os.system("start_MonitorReStart.bat")
        exit()
    quit_all_player()
    for i in range(0, START_COUNT):
        os.system(f"{LSCONSOLE} installapp --index {index_arr[i]} --filename {package_file}")
        time.sleep(5)
        logger.info("启动脚本{}", index_arr[i])
    time.sleep(30)
    logger.info("更新完成")


def check_download_apk():
    res = requests.get(f"{PKG_API}/get/{PKG_KEY}")
    data = res.json()
    if len(data["url"]) > 0:
        file_url = base64.b32decode(data["url"]).decode()
        logger.info("去更新了{}", file_url)
        if pathlib.Path(package_file).is_file():
            logger.info("删除原始文件")
            os.remove(package_file)
        try:
            logger.info("开始下载")

            wget.download(file_url, out=package_file)
            logger.success("下载完成")
            res = requests.get(f"{PKG_API}/del/{PKG_KEY}")
            logger.info(res.text)
        except Exception as ex:
            logger.error("下载失败")
            logger.error(ex)
            exit()
    else:
        logger.info("{}没有更新", PKG_KEY)


if __name__ == '__main__':
    init_server()
    check_download_apk()

    while True:
        android_loop()
