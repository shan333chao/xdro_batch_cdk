import numpy as np
from cnocr import CnOcr
from fastapi import FastAPI
import uvicorn
import asyncio
import queue
import os
from loguru import logger
import pathlib
import glob
import base64
from pydantic import BaseModel
from typing import Any, List, Union
from fastapi import Body, Form, UploadFile
from copy import deepcopy
from typing import List, Dict, Any
from PIL import Image

ocr_model = CnOcr(rec_model_name='densenet_lite_136-fc', det_model_name='db_shufflenet_v2_small',
                  det_more_configs={'rotated_bbox': False})
number_ocr = CnOcr(rec_model_name='densenet_lite_136-fc', det_model_name='naive_det', cand_alphabet='0123456789')
current_folder = os.path.dirname(__file__)
app = FastAPI()

q = queue.Queue(maxsize=5000)
log_dir = pathlib.Path('./logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir.joinpath('ocr_{time: YYYY_MM_DD_hh_mm}.log')
logger.add(log_file, retention='3 days', encoding='utf-8')


class OcrResponse(BaseModel):
    code: int = 200
    data: List[Dict[str, Any]]

    def dict(self, **kwargs):
        the_dict = deepcopy(super().dict())
        return the_dict


@app.post("/ocr_line")
async def ocr(image: UploadFile):
    res = {}
    try:
        image = image.file
        image = Image.open(image).convert('RGB')
        img_fp = np.asarray(image)
        res = ocr_model.ocr_for_single_line(img_fp)
    except Exception as ex:
        res["code"] = 0
        logger.error(ex)
    else:
        logger.info(res)
        res["code"] = 200
    return res


@app.post("/ocr")
async def ocr(image: UploadFile) -> Dict[str, Any]:
    image = image.file
    image = Image.open(image).convert('RGB')
    res = ocr_model.ocr(image)

    for _one in res:
        _one['position'] = _one['position'].tolist()
        _one["point"] = [int(_one['position'][0][0]), int(_one['position'][0][1]),
                         int(_one['position'][2][0]), int(_one['position'][2][1])]
        _one["score"] = float('%.2f' % _one["score"])
        if 'cropped_img' in _one:
            _one.pop('cropped_img')
        _one.pop('position')

    return OcrResponse(data=res).dict()


@app.post("/ocr_number")
async def ocr_number(image: UploadFile):
    res = {}
    try:
        image = image.file
        image = Image.open(image).convert('RGB')
        img_fp = np.asarray(image)
        res = number_ocr.ocr_for_single_line(img_fp)
    except Exception as ex:
        res["code"] = 0
        logger.error(ex)
    else:
        logger.info(res)
        res["code"] = 200
    return res


async def main():
    config = uvicorn.Config("RoTaskNameOcr:app", host="0.0.0.0", port=3090, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
