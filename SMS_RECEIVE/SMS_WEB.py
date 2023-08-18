import asyncio
import pathlib
import re
from pathlib import *
from urllib.parse import unquote
import uvicorn
from fastapi import FastAPI, Form
from loguru import logger

app = FastAPI()

log_dir = ""
valid_code = ""

 


def init_conf():
    global log_dir
    log_dir = pathlib.Path('./logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir.joinpath('sms_log_{time:YYYY_MM_DD}.log')
    logger.add(log_file, retention='3 days', encoding='utf-8')
    global valid_code
    valid_code = ""
    logger.success("初始化完成：{}",log_file)


@app.on_event('startup')
def init_data():
    init_conf()


@app.get("/sms/add/{content}")
async def add_data(content:str):
    read_data=unquote(content)
    logger.info(read_data)
    match = re.search(r"\d{6}", read_data)
    if match:
        code = match.group()
        global valid_code
        valid_code=code
        logger.info("验证码是:{}", code)
    else:
        logger.error("无法提取验证码")
    sms={"code":valid_code}
    return sms


@app.get("/sms/get")
async def get_sms():
    global valid_code
    logger.info(valid_code)
    data = {"code": valid_code}
    valid_code = ""
    return data

async def main():
    config = uvicorn.Config("SMS_WEB:app", host="0.0.0.0", port=9763, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

