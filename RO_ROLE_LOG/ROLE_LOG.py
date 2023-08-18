import os
import pathlib
import queue
import time
import glob
from fastapi import FastAPI
import uvicorn
import asyncio
from loguru import logger
from pydantic import BaseModel
from starlette.responses import FileResponse
import xml.etree.ElementTree as ET
import zipfile
from pathlib import *
import datetime
import pytz

app = FastAPI()
down_folder = ""
log_dir = ""
card_map = dict()
zeny_map = dict()
account_map = dict()
card_filter = set()
area_map = dict()
max_account_map = dict()
area_group_map = dict()


class RoleInfo(BaseModel):
    token: str = ""
    zeny: int = 0
    card: str = ""
    area: str = 0
    account: str = ""
    is_bind: int = 0
    idx:int=0
    time:str=""

    def get_identity(self):
        return "-".join([self.token, self.area, self.account])


def init_conf():
    global log_dir
    log_dir = pathlib.Path('./logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir.joinpath('role_log_{time:YYYY_MM_DD}.log')
    logger.add(log_file, retention='3 days', encoding='utf-8')
    global down_folder
    down_folder = pathlib.Path('./dafa_file')
    down_folder.mkdir(exist_ok=True)
    logger.info("init conf log file {} , data_file:{}", log_file, down_folder)


@app.on_event('startup')
def init_data():
    init_conf()
    data_map = dict()
    zeny_map = dict()
    area_group_map = dict()
    account_map = dict()
    max_account_map = dict()
    card_filter.add("哥布林首领卡片")
    card_filter.add("迪文卡片")
    card_filter.add("天地树之种卡片")
    card_filter.add("阿特罗斯卡片")
    card_filter.add("斯佩夏尔卡片")
    card_filter.add("寒冰龙卡片")
    card_filter.add("海神卡片")
    card_filter.add("迪塔勒泰晤勒卡片")
    card_filter.add("圣天使波利卡片")
    card_filter.add("炎之领主卡浩卡片")
    card_filter.add("狼外婆卡片")
    card_filter.add("艾勒梅斯卡片")
    # card_filter.add("狸猫卡片")
    # card_filter.add("摇滚蝗虫卡片")
    # card_filter.add("幽灵波利卡片")
    # card_filter.add("直升机哥布林卡片")
    # card_filter.add("枯树精卡片")
    # card_filter.add("狮鹫鹰卡片")
    # card_filter.add("半龙人卡片")
    # card_filter.add("鹗枭首领卡片")
    # card_filter.add("弑神者卡片")
    # card_filter.add("爱丽丝女仆卡片")
    # card_filter.add("安毕斯卡片")
    # card_filter.add("大本钟卡片")
    # card_filter.add("钟塔守护者卡片")
    # card_filter.add("草精卡片")
    # card_filter.add("魔灵娃娃卡片")
    card_filter.add("炎之小魔女卡片")
    # card_filter.add("银月魔女卡片")
    # card_filter.add("吹笛人卡片")
    card_filter.add("天使波利卡片")
    card_filter.add("黄金虫卡片")
    card_filter.add("塔妮小姐卡片")
    card_filter.add("恶魔波利卡片")
    card_filter.add("海盗之王卡片")
    card_filter.add("蜂后卡片")
    card_filter.add("蚁后卡片")
    card_filter.add("皮里恩卡片")
    card_filter.add("虎王卡片")
    card_filter.add("月夜猫卡片")
    card_filter.add("兽人英雄卡片")
    card_filter.add("犬妖首领卡片")
    card_filter.add("死灵卡片")
    card_filter.add("死灵骑士卡片")
    card_filter.add("凯特琳娜卡片")
    card_filter.add("嗜血怪人卡片")
    card_filter.add("兽人酋长卡片")
    card_filter.add("鹗枭男爵卡片")
    card_filter.add("血腥骑士卡片")
    card_filter.add("巴风特卡片")
    card_filter.add("黑暗之王卡片")
    card_filter.add("时间管理人卡片")
    card_filter.add("冰雹骑士卡片")
    card_filter.add("乌龟将军卡片")
    card_filter.add("希尔队长卡片")
    card_filter.add("蛇妖戈耳卡片")
    card_filter.add("荒境领主卡片")
    card_filter.add("波伊塔塔卡片")
    card_filter.add("欧德姆布拉卡片")
    card_filter.add("灵魂奏者卡片")
    card_filter.add("魔鬼大乌贼卡片")
    card_filter.add("塔奥群卡卡片")
    card_filter.add("迷梦猫妖卡片")
    card_filter.add("意念聚合体卡片")
    card_filter.add("魔剑士达纳托斯卡片")
    card_filter.add("女武神拉斯格瑞丝卡片")
    card_filter.add("奥术魔方卡片")
    card_filter.add("先王棋士团卡片")
    card_filter.add("贞奴比亚卡片")
    card_filter.add("灾厄魔女卡片")
    card_filter.add("索斯卡片")
    card_filter.add("巴尔特卡片")
    card_filter.add("兰特克力斯卡片")
    card_filter.add("卡伦卡片")
    card_filter.add("德古拉伯爵卡片")
    card_filter.add("幽灵梦魇卡片")
    card_filter.add("蓝疯兔卡片")
    card_filter.add("祖尔卡片")
    card_filter.add("元灵卡片")
    card_filter.add("生化巴风特卡片")
    card_filter.add("努卡卡片")
    card_filter.add("幻龙加利厄隆坦卡片")  
    # card_filter.add("波利之王卡片")
    # card_filter.add("巴西里斯克卡片")
    # card_filter.add("蛙王卡片")
    # card_filter.add("龙蝇卡片")
    card_filter.add("流浪之狼卡片")
    # card_filter.add("狮鹫兽卡片")
    # card_filter.add("妖君卡片")
    # card_filter.add("兽人婴儿卡片")
    # card_filter.add("南瓜先生卡片")
    card_filter.add("迷幻之王卡片")
    # card_filter.add("宝箱巨鳄卡片")
    # card_filter.add("塞尼亚卡片")
    # card_filter.add("寒冰雕像卡片")
    # card_filter.add("疯狂鬣狗卡片")
    # card_filter.add("堕落神官希巴姆卡片")
    # card_filter.add("狐仙莱卡翁卡片")
    # card_filter.add("枫树精灵伊斯玛卡片")
    # card_filter.add("银鱼湖主卡片")
    card_filter.add("火焰鸟啾利卡片")
    # card_filter.add("莉姆露卡片")
    # card_filter.add("宝石灵兽卡片")
    # card_filter.add("大脚龙虾卡片")
    # card_filter.add("矿石精卡片")
    # card_filter.add("白鹭女王卡片")
    # card_filter.add("玲珑双翼")
    load_account2()


def load_account2():
    area_index_map = {"area0.txt": 1, "area1.txt": 2,
                      "area2.txt": 3, "area3.txt": 4, "area4.txt": 5}
    global account_queue
    account_queue = queue.Queue(10000)
    current_folder = os.path.dirname(__file__)
    current_folder = str(Path(current_folder, "accounts").absolute())
    list_of_files = sorted(filter(os.path.isfile, glob.glob(
        current_folder + '/**/area*.txt', recursive=True)))

    for account_file in list_of_files:
        all_accounts = set()
        with open(account_file, "r") as accounts:
            all_accounts = set(accounts.readlines())
        global max_account_map
        file_name = account_file[-9:]
        index = area_index_map[file_name]
        max_account_map[index] = len(all_accounts) + 1
        area_map[index] = queue.Queue(len(all_accounts) + 2)
        for account in all_accounts:
            name_pwd = account.rstrip('\n').split('|')
            token = ""
            account_name = name_pwd[0]
            if index in account_map.keys() and account_name in account_map[index].keys():
                token = account_map[index][account_name]
            item = {"name": account_name,
                    "pwd": name_pwd[1], "token": token, "area": index+1}
            area_map[index].put(item)
            # logger.info(item)

        logger.info("area:{} account_num:{}", index, len(all_accounts))


# 重新加载账号数据
@app.get("/account/reset")
async def reset_account_player():
    load_account2()
    return calc_progress()


# 重置大区队伍
@app.get("/area_group/reset/{area}")
async def reset_area_group_player(area: int):
    res = {"code": 0, "data": dict()}
    if area not in area_group_map.keys():
        res["msg"] = "大区不存在"
        return res
    for player_id in area_group_map[area].keys():
        area_group_map[area][player_id] = 0
    res["data"] = area_group_map[area]
    return res


# 显示队伍信息
@app.get("/area_group/list")
async def show_area_group():
    return area_group_map


# 添加打手
@app.get("/area_group/set/{area}/{fight_id}")
async def set_area_group_player(area: int, fight_id: str):
    if area not in area_group_map.keys():
        area_group_map[area] = dict()
    area_group_map[area][fight_id] = 0
    return area_group_map[area]


# 删除打手
@app.get("/area_group/delete/{area}/{fight_id}")
async def delete_area_group_player(area: int, fight_id: str):
    if area not in area_group_map.keys():
        area_group_map[area] = dict()
    if fight_id in area_group_map[area].keys():
        area_group_map[area].pop(fight_id)
    return area_group_map[area]


# 退组
@app.get("/area_group/exit/{area}/{player_id}")
async def exit_area_group_player(area: int, player_id: str):
    res = {"code": 0, "data": dict()}
    if area not in area_group_map.keys():
        area_group_map[area] = dict()
        res["msg"] = "area 不存在"
        return res
    if player_id in area_group_map[area].keys():
        area_group_map[area][player_id] = area_group_map[area][player_id] - 1
        if area_group_map[area][player_id] < 0:
            area_group_map[area][player_id] = 0
    else:
        res["msg"] = "play id 不存在"
        return res
    res["data"] = {"player_id": player_id,
                   "members": area_group_map[area][player_id]}
    return res


# 设置队伍成员数量
@app.get("/area_group/set_count/{player_id}/{count}")
async def set_group_member_count(player_id: str, count: int):
    res = {"code": 0, "data": dict()}
    for area in area_group_map.keys():
        if player_id in area_group_map[area].keys():
            area_group_map[area][player_id] = count
            res["data"] = {player_id: area_group_map[area][player_id]}
            break
    return res


# 获取队长id
@app.get("/area_group/get/{area}")
async def set_area_group_player(area: int):
    player_id = ""
    res = {"code": 0, "data": dict()}
    if area not in area_group_map.keys():
        res["msg"] = "选区不存在"
        return res
    for key, val in area_group_map[area].items():
        if val < 5:
            player_id = key
            area_group_map[area][player_id] = area_group_map[area][player_id] + 1
            break
    if player_id == "":
        return res
    res["data"] = {"player_id": player_id,
                   "member_count": area_group_map[area][player_id]}
    return res


def calc_progress():
    account_stats = dict()
    for index in area_map.keys():
        account_stats[index] = area_map[index].qsize()
    return account_stats


# 查看进度
@app.get("/account/progress")
async def get_account_progress():
    return calc_progress()


@app.get("/account/get/{area}")
async def get_ro_account(area: int):
    res = {"code": 0, "data": dict()}
    if area not in area_map.keys():
        res["msg"] = "大区不存在"
        return res
    if area_map[area].qsize() == 0:
        res["msg"] = "本次跑完了"
        return res
    global max_account_map
    res["seq"] = max_account_map[area] - area_map[area].qsize()
    account = area_map[area].get_nowait()
    account["area"] = int(area) - 1
    res["data"] = account
    return res


@app.post("/data/update")
async def add_data(role_info: RoleInfo):
    logger.info(role_info)
    role_info.area = str(int(role_info.area) + 1)
    if role_info.card in card_filter:
        logger.info(role_info)
        role_info.idx=len(card_map)+1
        # 2. 设置时区为东8区
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.datetime.now(tz)
        role_info.time=now.strftime("%Y-%m-%d %H:%M:%S")
        card_map[role_info.get_identity()] = role_info

    if role_info.zeny > 10000000:
        zeny_map[role_info.get_identity()] = role_info

    if role_info.area not in account_map.keys():
        account_map[role_info.area] = {role_info.account: role_info.token}
    else:
        account_map[role_info.area][role_info.account] = role_info.token
    res = {"code": 0, "data": role_info}
    return res


@app.get("/data/list")
async def getlist():
    array_role = []
    for key, val in card_map.items():
        array_role.append(val)
    zeny_role = []
    for key, val in zeny_map.items():
        zeny_role.append(val)
    res = {"code": 0, "card": array_role, "zeny": zeny_role}
    return res


@app.get("/data/get_unbind")
async def get_unbund():
    res = {"code": -1, "role": None}
    for key, val in card_map.items():
        if val.is_bind == 0:
            res["code"] = 0
            res["role"] = val
            break
    return res

@app.post("/data/bind")
async def add_data(role_info: RoleInfo):
    logger.info("bind {}",role_info)
    need_role_info=card_map[role_info.get_identity()]  
    need_role_info.is_bind=1
    card_map[role_info.get_identity()]=need_role_info
    res = {"code": 0, "data": need_role_info}
    return res


def write_token_xml(token: str, folder_path: str):
    template_xml = pathlib.Path('./tpl_XDUserToken.xml')
    root = ET.parse(template_xml)

    for node in root.findall('.//string[@name="XDToken"]'):
        node.text = token

    xml_path = str(pathlib.Path(folder_path, 'XDUserToken.xml').absolute())
    logger.info(xml_path)
    with open(xml_path, "wb") as out:
        out.write(b"<?xml version='1.0' encoding='utf-8' standalone='yes' ?>\n")
        root.write(out, encoding="utf-8", xml_declaration=False)

    return xml_path


@app.get("/data/file/{type}")
async def get_file(type: str):
    prefix_name = "zeny"
    data_map = dict()
    if type == "card":
        prefix_name = "card"
        data_map = card_map
    elif type == "zeny":
        data_map = zeny_map
        prefix_name = "zeny"

    if len(data_map) == 0:
        return {"code": 0, "msg": "没有数据", "time": time.time()}
    xml_files = []
    folder_name = prefix_name + str(int(time.time()))

    data_dir = pathlib.Path(down_folder, folder_name)
    res = {"code": 0, "data": "没有数据"}
    data_dir.mkdir(exist_ok=True)

    moniqi_index_map = {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1}
    for key, val in data_map.items():
        area_folder = pathlib.Path(data_dir, val.area)
        area_folder.mkdir(exist_ok=True)
        moniqi_folder = pathlib.Path(
            area_folder, f"模拟器{moniqi_index_map[val.area]}")
        moniqi_folder.mkdir(exist_ok=True)
        moniqi = str(moniqi_folder.absolute())
        xml_file = write_token_xml(val.token, moniqi)
        xml_files.append(xml_file)
        moniqi_index_map[val.area] += 1
    if len(xml_files) == 0:
        return res
    zip_file_name = folder_name + ".zip"
    res_zip_file = str(pathlib.Path(data_dir, zip_file_name).absolute())
    logger.info(res_zip_file)
    with zipfile.ZipFile(res_zip_file, 'w', zipfile.ZIP_DEFLATED) as target:
        for item in xml_files:
            target.write(item)

    return FileResponse(res_zip_file, filename=zip_file_name)


@app.get("/data/clear/{type}")
async def data_clear(type: str):
    if type == "card":
        card_map.clear()
    elif type == "zeny":
        zeny_map.clear()

    res = {"code": 0, "card": card_map, "zeny": zeny_map}
    return res


@app.get("/data/filter_add/{name}")
async def map_add(name: str):
    card_filter.add(name)
    logger.info("add card {}", name)
    res = {"code": 0, "data": name}
    return res


async def main():
    config = uvicorn.Config("ROLE_LOG:app", host="0.0.0.0",
                            port=5007, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
