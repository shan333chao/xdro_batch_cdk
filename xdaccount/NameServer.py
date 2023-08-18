import json
from fastapi import FastAPI
import uvicorn
import asyncio
from loguru import logger
import requests
all_names = set()

app = FastAPI()

@app.on_event('startup')
def init_names():
    global all_names
    all_names = set()
    with open('names.json', encoding='utf-8') as f:
        items = json.loads(f.read())
        for item in items:
            for i in range(2,8):
                origin_name=item["riddle"].strip()
                name=origin_name[:i]
                if len(name)>0:
                    all_names.add(name)
                name=origin_name[i:]
                if len(name)>0:
                    all_names.add(name)
                name=origin_name[0:i+2]
                if len(name)>0:
                    all_names.add(name)
                name=origin_name[0:i+3]
                if len(name)>0:
                    all_names.add(name)
                name=origin_name[0:i+4]
                if len(name)>0:
                    all_names.add(name)
                
    logger.info("all name count:{}",len(all_names))
        



@app.get("/nickname/get")
async def root():
 
    res = {"name": all_names.pop()}
    logger.info("{},len:{}",res,len(all_names))
    return res



async def main():
    config = uvicorn.Config("NameServer:app", host="0.0.0.0", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())