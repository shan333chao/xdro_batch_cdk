import base64

from loguru import logger
import requests

RO_RENZHE_1 = ""
RO_BIG_1=""
RO_100 = ""
RO_60 = ""
RO_CHUSHI_1 = "https://dl-uf-zb.pds.uc.cn/BQkZTvPm/4084393060/647ebfbf740364ba34bd43afa746f620a9eac79c/647ebfbfb805833cac5b4c60af225c7bd7f0f344?Expires=1686039031&OSSAccessKeyId=LTAIyYfxTqY7YZsg&Signature=xfGvojF89O0vtMy%2FDZuq6Fn6LcE%3D&x-oss-traffic-limit=503316480&response-content-disposition=attachment%3B%20filename%3Dcreate_account-V_1.0.0-2023%E5%B9%B46%E6%9C%886%E6%97%A513%E6%97%B68%E5%88%8651%E7%A7%92-%E7%B2%BE%E7%AE%80%E7%89%88.apk&u5=2b608b9ead88715ae86c700dd35acd4d&callback=eyJjYWxsYmFja0JvZHlUeXBlIjoiYXBwbGljYXRpb24vanNvbiIsImNhbGxiYWNrU3RhZ2UiOiJiZWZvcmUtZXhlY3V0ZSIsImNhbGxiYWNrRmFpbHVyZUFjdGlvbiI6Imlnbm9yZSIsImNhbGxiYWNrVXJsIjoiaHR0cHM6Ly9hdXRoLWNkbi51Yy5jbi9vdXRlci9vc3MvY2hlY2twbGF5IiwiY2FsbGJhY2tCb2R5Ijoie1wiaG9zdFwiOiR7aHR0cEhlYWRlci5ob3N0fSxcInNpemVcIjoke3NpemV9LFwicmFuZ2VcIjoke2h0dHBIZWFkZXIucmFuZ2V9LFwicmVmZXJlclwiOiR7aHR0cEhlYWRlci5yZWZlcmVyfSxcImNvb2tpZVwiOiR7aHR0cEhlYWRlci5jb29raWV9LFwibWV0aG9kXCI6JHtodHRwSGVhZGVyLm1ldGhvZH0sXCJpcFwiOiR7Y2xpZW50SXB9LFwib2JqZWN0XCI6JHtvYmplY3R9LFwic3BcIjoke3g6c3B9LFwidG9rZW5cIjoke3g6dG9rZW59LFwidHRsXCI6JHt4OnR0bH0sXCJjbGllbnRfdG9rZW5cIjoke3F1ZXJ5U3RyaW5nLmNsaWVudF90b2tlbn19In0%3D&callback-var=eyJ4OnNwIjoiMzc4IiwieDp0b2tlbiI6IjItMmI2MDhiOWVhZDg4NzE1YWU4NmM3MDBkZDM1YWNkNGQtMC03LTYxNDQwLWYyMTY5ODFmZjc0OTRmNzI4MTM5NGJkZjIxYTQ3YmM2LTkxMzhlNGVhNmE5Y2RkMTUwMWZlYmM1YThlYmMzNDkwIiwieDp0dGwiOiIxMDgwMCJ9"

package_map = {
    "RO_100_1": RO_100,
    "RO_60_1": RO_60,
    "RO_RENZHE_1": RO_RENZHE_1,
    "RO_RENZHE_2": RO_RENZHE_1,
    "RO_RENZHE_3": RO_RENZHE_1,
    "RO_RENZHE_4": "",
    "RO_RENZHE_5": "",
    "RO_RENZHE_6": RO_RENZHE_1,

    "RO_CHUSHI_1_1": RO_CHUSHI_1,
    "RO_CHUSHI_1_2": RO_CHUSHI_1,

    "RO_CHUSHI_2_1": RO_CHUSHI_1,
    "RO_CHUSHI_2_2": RO_CHUSHI_1,

    "RO_CHUSHI_3_1": RO_CHUSHI_1,
    "RO_CHUSHI_3_2": RO_CHUSHI_1,

    "RO_CHUSHI_4_1": RO_CHUSHI_1,
    "RO_CHUSHI_4_2": RO_CHUSHI_1,

    "RO_BIG_1":RO_BIG_1
}
PKG_API = "http://0.0.0.0:5053/pkg"
for key, val in package_map.items():
    if len(val) > 0:
        b32str = base64.b32encode(val.encode()).decode()
        res = requests.get(f"{PKG_API}/put/{key}/{b32str}").json()
        if res["url"] == b32str:
            logger.success("更新成功")
        logger.info("{}", res)
        logger.info("update {},{}", key, b32str)
    else:
        res = requests.get(f"{PKG_API}/del/{key}").json()
        logger.info("{}", res)