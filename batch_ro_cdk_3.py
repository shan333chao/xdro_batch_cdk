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
server_id = 10001003
file_name = gift_code + "_" + str(server_id) + ".json"
name_list_str = '所罗门的噩梦,'\
                'Mars酱,cheng,玖伍贰柒,烤猪耳朵,vv仔,瞬瞬,辉辉,星矢,卡妙,童虎,降龙十八掌,降龙十七掌,降龙十六掌,降龙十五掌,' \
                '降龙十四掌,降龙十二掌,降龙十一掌,鲁班7号,王者狄仁杰,王者虞姬,王者后羿,王者孙尚香,人来人往勿失勿忘,' \
                'baby金刚娃,红烧猪耳朵,焖猪耳朵,炸猪耳朵,四月裂帛,火星情报局,火星航班员,水星情报员,星宵,欧巴思密达,' \
                '喜马拉雅山,打蛇棒法,打狗棒法,打猫棒法,超级犀利,超级欧气,超级潇洒,超级义气,超级先锋,超级好玩,超级开心,' \
                '超级快乐,超级好笑,超级搞笑,兔兔可爱,超级轩昂,超级不凡,超级悠然,超级豁达,超级高雅,最强王者伽罗,王者马可波罗,' \
                '王者铁木真,王者公孙离,菜鸟百里守约,飘逸艾琳,坑货李元芳,老臣黄汉升,渣渣蒙犽,想什么,猜什么,做什么,吃什么,念什么,逛什么,喝什么,'\
                '滴滴,奥德赛降临,蓝蓝子,小朵朵朵朵朵,蓝蓝蓝蓝朵,朵朵子,'\
                '框框,暮城雪,陌小柒,巫女有只猫,本小姐很嚣张,云绾宁,胖豆包,瘦豆包,粘豆包,甜豆包,咸豆包,胖豆包,海绵抱抱,海绵包包,海绵饱饱,海绵豹豹,' \
                '海绵堡堡,神射传说,射就行了,凌络依,GT荣耀王者,猫行天下,无限诗人,肉骨头,无敌小恩,心动丶波利,無人料理屋,cheng,Mars酱,vv仔'


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
            print(f"{role_name} - {submit_res['msg']}")
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
