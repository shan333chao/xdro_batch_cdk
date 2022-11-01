# -*- coding:utf8 -*-
import os
import subprocess
import winreg
from queue import Queue
import schedule
import time
from loguru import logger
import arrow

logger.add("file_{time}.log", rotation="12:00")

start_count = 2
wait_seconds = 5
run_minute = 30
game_package_name = 'com.xd.ro.roapk'
script_package_name = ''
last_run_time = arrow.now()

LSCONSOLE = ''
LS2CONSOLE = ''
VM_COUNT = 0
LOOP_QUEUE = Queue(1)
FILE_NAME = "queue_process.json"


def get_lsplayer_path():
    res = {}
    lsplayer_reg = r'SOFTWARE\baizhi\lsplayer64'
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, lsplayer_reg)
    try:
        i = 0
        while True:
            k, v, t = winreg.EnumValue(key, i)
            i += 1
            res[k] = v
    except Exception as e:
        winreg.CloseKey(key)
    return res


def get_vmbox_count(lsplayer: dict):
    leidian_folder = lsplayer["DataDir"]
    count = 0
    for i in range(0, 200):
        if not os.path.exists(f'{leidian_folder}\\leidian{i}'):
            break
        count = i
    return count


def sort_windows():
    os.system(f"{LSCONSOLE} sortWnd")


def run_app(index_list: list):
    logger.info("启动了 {}", index_list)
    while 1:
        player_windows = get_player_states()
        for player in player_windows:
            player_info = player.split(",")
            if len(player_info) == 7 and int(player_info[-2]) > 0 and int(player_info[4]) == 1 and player_info[
                0] in index_list:
                os.system(f"{LSCONSOLE} runapp --index {player_info[0]} --packagename {game_package_name}")
                index_list.remove(player_info[0])
                logger.info("启动{}--{} roapk", player_info[0], player_info[1])
                time.sleep(1)
        if len(index_list) == 0:
            break
        time.sleep(1)


def start_ls(index: int):
    os.system(f"{LSCONSOLE} launch --index {index}")


def get_player_states():
    p = subprocess.Popen(f"{LS2CONSOLE} list2",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         )
    result = p.communicate()[0]
    test_res = result.decode('gb2312')
    all_players = test_res.split("\r\n")
    return all_players


def show_ls_states():
    all_players = get_player_states()
    # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
    for item in all_players:
        item_info = item.split(",")
        if len(item_info) == 7 and int(item_info[-2]) > 0:
            logger.info(f"player {item_info[0]}-{item_info[1]} running")
    logger.warning("-------------------------------------------------\n\n")
    now_time = arrow.now()
    next_time = last_run_time.shift(minutes=run_minute)
    durn = next_time.humanize(now_time, granularity=["minute", "second"])
    logger.info("{} 启动下一轮", durn)


def fill_queue(max_size):
    q = Queue(maxsize=max_size)

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf8') as f:
            name_str = f.readline()
            queue_arr = name_str.split(",")
            for index in reversed(queue_arr):
                q.put(index)
    else:
        for index in range(0, max_size):
            q.put(str(index))
    return q


def save_queue():
    items = []
    for idx in range(0, VM_COUNT):
        origin_index = LOOP_QUEUE.get()
        items.append(origin_index)
        LOOP_QUEUE.put(origin_index)
    exist_names_str = ",".join(items)
    with open(FILE_NAME, mode='w') as filename:
        filename.write(exist_names_str)


def android_loop():
    need_to_run = []
    quit_all_player()
    for item in range(0, start_count):
        index = LOOP_QUEUE.get()
        logger.info(f"正在启动第{index}个")
        start_ls(index)
        LOOP_QUEUE.put(index)
        need_to_run.append(index)
        time.sleep(wait_seconds)

    logger.success(f"本次{start_count}个模拟器启动完成")
    run_app(need_to_run)
    sort_windows()
    save_queue()
    last_run_time = arrow.now()


def quit_all_player():
    logger.info("正在退出当前运行的模拟器")
    os.system(f"{LSCONSOLE} quitall")
    time.sleep(5)
    logger.success("所有模拟器退出完成")


if __name__ == '__main__':
    lsplayer_info = get_lsplayer_path()
    VM_COUNT = get_vmbox_count(lsplayer_info) + 1
    LSCONSOLE = lsplayer_info["InstallDir"] + "\\lsconsole.exe"
    LS2CONSOLE = lsplayer_info["InstallDir"] + "\\ls2console.exe"
    logger.info(lsplayer_info)
    LOOP_QUEUE = fill_queue(VM_COUNT)
    logger.info(f"共有 {VM_COUNT} 个,每一批 {start_count} 个")
    logger.success("程序已启动")
    android_loop()
    schedule.every(run_minute).minutes.do(android_loop)
    schedule.every(60).seconds.do(show_ls_states)
    while True:
        schedule.run_pending()
        time.sleep(1)
