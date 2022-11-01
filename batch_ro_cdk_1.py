import time
import requests
import ddddocr
import random as rd
from urllib import parse
import os
import gift_key


# 礼包兑换码
gift_codes = [gift_key.GAFT_CODE]

# 服务器列表
#  守护永恒的爱 = 10001
#  梦想天空 = 10001002
#  辉煌领域 = 10001003
server_id = 10001

name_list_str = '不倒翁娘娘,Angke丶初心,拉布拉多么坑爹,尐尛糖,auv卡册0,auv卡册1,auv卡册2,auv卡册3,auv卡册4,auv卡册5,auv卡册6,auv卡册7,auv卡册8,auv卡册9,' \
                'auv卡册10,auv卡册11,auv卡册12,auv卡册13,auv卡册14,auv卡册15,auv卡册16,auv卡册17,auv卡册18,auv卡册19,auv卡册20,auv卡册21,' \
                'auv卡册22,auv卡册23,auv卡册24,auv卡册25,auv卡册26,auv卡册27,auv卡册28,auv卡册29,auv卡册30,auv卡册31,auv卡册32,auv卡册33,' \
                'auv卡册34,auv卡册35,auv卡册36,auv卡册37,auv卡册38,auv卡册39,auv卡册40,auv卡册41,auv卡册42,auv卡册43,auv卡册44,auv卡册45,' \
                'auv卡册46,auv卡册47,auv卡册48,auv卡册49,auv卡册50,auv卡册51,auv卡册52,auv卡册53,auv卡册54,auv卡册55,auv卡册56,auv卡册57,' \
                'auv卡册58,auv卡册59,auv卡册60,auv卡册61,auv卡册62,auv卡册63,auv卡册64,auv卡册65,auv卡册66,auv卡册67,auv卡册68,auv卡册69,' \
                'auv卡册70,auv卡册71,auv卡册72,auv卡册73,auv卡册74,auv卡册75,auv卡册76,auv卡册77,auv卡册78,auv卡册79,auv卡册80,auv卡册81,' \
                'auv卡册82,auv卡册83,auv卡册84,auv卡册85,auv卡册86,auv卡册87,auv卡册88,auv卡册89,auv卡册90,auv卡册91,auv卡册92,auv卡册93,' \
                'auv卡册94,auv卡册95,auv卡册96,auv卡册97,auv卡册98,auv卡册99,auv卡册100,auv卡册101,auv卡册102,auv卡册103,auv卡册104,' \
                'auv卡册105,auv卡册106,auv卡册107,auv卡册108,auv卡册109,auv卡册110,auv卡册111,auv卡册112,auv卡册113,auv卡册114,auv卡册115,' \
                'auv卡册116,auv卡册117,auv卡册118,auv卡册119,auv卡册120,auv卡册121,auv卡册122,auv卡册123,auv卡册124,auv卡册125,auv卡册126,' \
                'auv卡册127,auv卡册128,auv卡册129,auv卡册130,auv卡册131,auv卡册132,auv卡册133,auv卡册134,auv卡册135,auv卡册136,auv卡册137,' \
                'auv卡册138,auv卡册139,auv卡册140,auv卡册141,auv卡册142,auv卡册143,auv卡册144,auv卡册145,auv卡册146,auv卡册147,auv卡册148,' \
                'auv卡册149,auv卡册150,auv卡册151,auv卡册152,auv卡册153,auv卡册154,auv卡册155,auv卡册156,auv卡册157,auv卡册158,auv卡册159,' \
                'auv卡册160,auv卡册161,auv卡册162,auv卡册163,auv卡册164,auv卡册165,auv卡册166,auv卡册167,auv卡册168,auv卡册169,auv卡册170,' \
                'auv卡册171,auv卡册172,auv卡册173,auv卡册174,auv卡册175,auv卡册176,auv卡册177,auv卡册178,auv卡册179,auv卡册180,auv卡册181,' \
                'auv卡册182,auv卡册183,auv卡册184,auv卡册185,auv卡册186,auv卡册187,auv卡册188,auv卡册189,auv卡册190,auv卡册191,auv卡册192,' \
                'auv卡册193,auv卡册194,auv卡册195,auv卡册196,auv卡册197,auv卡册198,auv卡册199'





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



name_arr = set(name_list_str.split(","))
result_dic = {}
for gift_code in gift_codes:
    file_name = gift_code + "_" + str(server_id) + ".json"
    exist_names = read_recived_log()
    for role_name in name_arr:
        role_name = role_name.strip()
        if role_name in exist_names:
            continue

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
                print(f"{role_name} - {submit_res['msg']}-{gift_code}")
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

    print(result_dic)
else:
    print(f"名单中的{len(exist_names)}人已经都领了")
