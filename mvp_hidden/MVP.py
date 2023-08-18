import json
from fastapi import FastAPI
import uvicorn
import asyncio
from loguru import logger
import pathlib
from pathlib import *

all_mvps = dict()
mvp_name_map=dict()
app = FastAPI()

log_dir = pathlib.Path('./mvplogs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir.joinpath('mvplog_{time: YYYY_MM_DD_hh_mm}.log')
logger.add(log_file, retention='3 days', encoding='utf-8')


@app.on_event('startup')
def init_names():
    global all_mvps    
    global mvp_name_map
    mvp_name_map[1]="卡伦"
    mvp_name_map[2]="迪文"
    mvp_name_map[3]="凯特琳娜"
    mvp_name_map[4]="狼外婆"
    mvp_name_map[5]="嗜血怪人"
    mvp_name_map[6]="死灵骑士"
    mvp_name_map[7]="幽灵梦魇"          
    logger.info("all mvps count:{}",len(all_mvps))
        



@app.get("/mvp/get")
async def get_mvp():
    data={"code":0,"data":set( all_mvps.keys())}
    all_mvps.clear()
 
    return data


@app.get("/mvp/set/{mvp_type}")
async def set_mvp(mvp_type:int):
    global all_mvps     
    logger.info("MVP [{}] 出现",mvp_name_map[mvp_type])
    all_mvps[mvp_type]=1
    data={"code":0}
    return data


async def main():
    config = uvicorn.Config("MVP:app", host="0.0.0.0", port=9491, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())