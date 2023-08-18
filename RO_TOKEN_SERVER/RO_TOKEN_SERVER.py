import glob
from fastapi import FastAPI
import uvicorn
import asyncio
import queue
import os
from loguru import logger
import xml.etree.ElementTree as ET
import pathlib
from pathlib import *

app = FastAPI()

q = queue.Queue(maxsize=5000)
log_dir = pathlib.Path('./logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir.joinpath('runlog_{time: YYYY_MM_DD_hh_mm}.log')
logger.add(log_file, retention='3 days', encoding='utf-8')

@app.on_event('startup')
def init_accounts():
    current_folder = os.path.dirname(__file__)
    current_folder = str(Path(current_folder, "accounts").absolute())
    list_of_files = sorted(filter(os.path.isfile, glob.glob(current_folder + '/**/*.xml', recursive=True)))
    for index in range(0, len(list_of_files)):
        xml_file = list_of_files[index]
        with open(xml_file, "r") as file:
            elem_root = ET.parse(file).getroot()
            elem = elem_root.find('.//string[@name="XDToken"]')
            if elem.text is None:
                logger.error("token error {}", xml_file)
                continue
            token_str = elem.text.partition('\n')[0]
            if len(token_str) == 32:
                logger.info(xml_file)
                moniqi = list(Path(xml_file).parts)[-3:-1]
                item = {"tag": "-".join(moniqi), "data": token_str, "seq": index+1}
                q.put(item)


@app.get("/account/get")
async def root():
    if q.qsize() == 0:
        init_accounts()
        logger.info("加载配置完成！一共{}个号", q.qsize())
    token_item = q.get_nowait()
    q.put(token_item)
    token_item["code"] = 0

    logger.info("({}/{}) {}  : {}", token_item["seq"], q.qsize(), token_item["tag"], token_item["data"])
    return token_item


@app.get("/account/set/{index}")
async def set_index(index: int):
    if index > 0:
        for i in range(0, q.qsize()):
            q.get_nowait()
        init_accounts()
        for i in range(0, index + 1):
            q.put(q.get_nowait())
    res = {"code": 0, "data": index}
    return res


async def main():
    config = uvicorn.Config("RO_TOKEN_SERVER:app", host="0.0.0.0", port=5003, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
