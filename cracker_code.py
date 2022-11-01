import time
import requests
import ddddocr
import random as rd
from urllib import parse
import os
import gift_key
import ujson

# 礼包兑换码
gift_code = gift_key.GAFT_CODE
# 服务器列表
#  守护永恒的爱 = 10001
#  梦想天空 = 10001002
#  辉煌领域 = 10001003
server_id = 10001004
file_name = gift_code + "_" + str(server_id) + ".json"
name_list_str = '百花繚亂'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
submit_url = "https://party.xd.com/event/2017jana/ajax_submit"


def read_recived_log():
    received = []
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf8') as f:
            name_str = f.readline()
            received = name_str.split(",")
    return received


ocr = ddddocr.DdddOcr()

exist_names = read_recived_log()

name_arr = set(name_list_str.split(","))
result_dic = {}
role_name = name_arr.pop()
for index in range(132, 888):
    gift_code = f"ROVIP{index}"
    try_times = 0
    while 1:
        captcha_identifier = str(rd.random())
        captcha = "https://party.xd.com/captcha/captcha/" + captcha_identifier
        session = requests.sessions.session()
        pic = session.get(captcha, headers=headers)
        captcha_code = ocr.classification(pic.content)
        form_data = {
            'server_id': server_id,
            'name': role_name,
            'code': gift_code,
            'captcha': captcha_code,
            'captcha_identifier': captcha_identifier
        }
        req_form_data = parse.urlencode(form_data)
        submit_res = session.request(method='POST', url=submit_url, data=req_form_data, headers=headers).json()
        if submit_res['code'] == -4:
            try_times = try_times + 1
            print(f"{role_name} - 领取失败 原因：{submit_res['msg']} 重试:{try_times}")
        else:
            if submit_res['msg'] in result_dic.keys():
                result_dic[submit_res['msg']].append(role_name)
            else:
                result_dic[submit_res['msg']] = [role_name]
                print(f"{role_name} - {submit_res['msg']}--{gift_code}")
            break

if len(result_dic) > 0:
    if '礼包码批次领取数量超过本组限制' in result_dic.keys():
        exist_names.extend(result_dic['礼包码批次领取数量超过本组限制'])

    if '礼包码兑换成功' in result_dic.keys():
        exist_names.extend(result_dic['礼包码兑换成功'])

    exist_names_str = ','.join(exist_names)

    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, mode='a') as filename:
        filename.write(exist_names_str)

    print(ujson.dumps(result_dic, ensure_ascii=False))
else:
    print(f"名单中的{len(exist_names)}人已经都领了")
