import json
from fastapi import FastAPI
import uvicorn
import asyncio
import queue

CONFIG_NAME = "conf.dll"
import os
from loguru import logger
import pathlib

log_dir = pathlib.Path('./logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir.joinpath('runlog_{time: YYYY_MM_DD}.log')
logger.add(log_file, retention='3 days', encoding='utf-8')

app = FastAPI()

# 启动数量
START_COUNT = 15
# 启动时间间隔秒
WAIT_SECONDS = 20
# 运行分钟数
RUN_MINUTE = 45
# 排除不跑的
EXCEPT_INDEX = []
MAX_SERVER_COUNT = 140

q = queue.Queue(maxsize=500)


@app.on_event('startup')
def init_server():
    conf = get_lsplayer_path()
    init_conf(conf)
    logger.info("加载:{}", MAX_SERVER_COUNT)
    for index in range(1, MAX_SERVER_COUNT + 1):
        q.put(index)


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


@app.get("/seq/get")
async def root():
    start_array = []
    for index in range(0, START_COUNT):
        get_index = q.get_nowait()
        start_array.append(get_index)
        q.put(get_index)
    logger.info("process:{}", start_array)
    res = {"data": start_array, "code": 200}
    return res


@app.get("/seq/set/{index}")
async def set_index(index: int):
    if 0 > index > MAX_SERVER_COUNT:
        res = {"code": 0, "data": index, "meg": "invalid index"}
        return res
    for i in range(0, MAX_SERVER_COUNT):
        q.get_nowait()

    init_server()
    for i in range(0, index):
        get_index = q.get_nowait()
        q.put(get_index)

    res = {"code": 200, "data": index}
    logger.info("set index:{}", index)
    return res


async def main():
    config = uvicorn.Config("LD_INDEX_SERVER:app", host="0.0.0.0", port=23333, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
