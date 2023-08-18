import glob
import os
import pathlib
from fastapi import FastAPI
import uvicorn
import asyncio
from loguru import logger
from pydantic import BaseModel
from starlette.responses import FileResponse
import xml.etree.ElementTree as ET
from pathlib import *


app = FastAPI()
down_folder = ""
log_dir = ""


class ShopInfo(BaseModel):
    shopname: str = ""
    company: str = 0
 
 
 


def init_conf():
    global log_dir
    log_dir = pathlib.Path('./logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir.joinpath('shop_log_{time:YYYY_MM_DD}.log')
    logger.add(log_file, retention='30 days', encoding='utf-8')
 


@app.on_event('startup')
def init_data():
    init_conf()

@app.post("/data/add")
async def add_data(role_info: ShopInfo):
    logger.info("{}",role_info)
    res = {"code": 0, "data": role_info}
    return res


@app.get("/data/getkeys")
async def get_keywords():
    current_folder = os.path.dirname(__file__)
    list_of_files = sorted(filter(os.path.isfile, glob.glob(
        current_folder + '/**/*.txt', recursive=True)))
    keyword_file=list_of_files[0]
    all_keys=[]
    with open(keyword_file, "r",encoding="utf8") as allkeys:
        datas =list(allkeys.readlines())
        for key in datas:
            all_keys.append(key.rstrip('\n'))
    res = {"code": 0, "data": all_keys}
    return res



   

async def main():
    config = uvicorn.Config("TAOTE:app", host="0.0.0.0",
                            port=5007, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
