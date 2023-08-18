import glob
from fastapi import FastAPI
import queue
import os
from loguru import logger
import xml.etree.ElementTree as ET
import pathlib
from pathlib import *

log_dir = pathlib.Path('./logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir.joinpath('runlog_{time: YYYY_MM_DD_hh_mm}.log')
logger.add(log_file, retention='3 days', encoding='utf-8')

checker = set()


def init_accounts():
    current_folder = os.path.dirname(__file__)
    current_folder = str(Path(current_folder, "accounts").absolute())
    list_of_files = sorted(filter(os.path.isdir, glob.glob(current_folder + '/**/模拟器*', recursive=True)))
    for index in range(0, len(list_of_files)):
        xml_file = list_of_files[index]
        if len(os.listdir(xml_file)) == 0:
            logger.info(xml_file)

        # with open(xml_file, "r") as file:
        #     elem_root = ET.parse(file).getroot()
        #     elem = elem_root.find('.//string[@name="XDToken"]')
        #     if elem.text is None:
        #         logger.error("token error {}", xml_file)
        #         continue
        #
        #     token_str = elem.text.partition('\n')[0]
        #     if len(token_str) == 32:
        #         moniqi = list(Path(xml_file).parts)[-3:-1]
        #         if token_str not in checker:
        #             checker.add(token_str)
        #         else:
        #             item = {"tag": "-".join(moniqi), "data": token_str, "seq": index + 1}
        #             logger.info("{},{}", xml_file, item)
        #     else:
        #         logger.info("empty:{}", xml_file)

    logger.info("total:{}", len(checker))


if __name__ == "__main__":
    init_accounts()
