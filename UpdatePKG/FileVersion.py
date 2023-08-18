import time
from fastapi import FastAPI
import uvicorn
import asyncio
import pathlib
from loguru import logger

app = FastAPI()

log_dir = pathlib.Path('./logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir.joinpath('pkglog_{time: YYYY_MM_DD_hh_mm}.log')
logger.add(log_file, retention='3 days', encoding='utf-8')
file_map = dict()


@app.on_event('startup')
def init_data():
    file_map["test"] = {"url": "", "ver": 6}


@app.get("/pkg/get/{file_key}")
async def getfile(file_key: str):
    if file_key in file_map.keys():
        data = file_map.get(file_key)
        logger.info(data)
        return data
    data = {"url": "", "ver": -1}
    logger.info(data)
    return data


@app.get("/pkg/put/{file_key}/{url}")
async def putfile(file_key: str, url: str):
    if file_key in file_map.keys():
        file_map.get(file_key)["url"] = url
        file_map.get(file_key)["ver"] = file_map.get(file_key)["ver"] + 1
        file_map.get(file_key)["seq"] = time.time()
    else:
        file_map[file_key] = {"url": url, "seq": time.time(), "ver": 1}
    data = file_map[file_key]
    logger.info(data)
    return data

@app.get("/pkg/del/{file_key}")
async def del_file(file_key: str):
    if file_key in file_map.keys():
        file_map.pop(file_key)
    logger.info("DEL {}",file_key)
    return file_key

async def main():
    config = uvicorn.Config("FileVersion:app", host="0.0.0.0", port=5053, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
