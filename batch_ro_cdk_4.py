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
name_list_str = 'VLKつ沫沫,VLKつ小妹,VLKつ猫猫,VLKつ囡囡,VLKつ琪琪,VLKつ伊依,小小小微微,小小小依依,小小小兔兔,小小小舞舞,小小小月月,小小小讨厌,' \
                '小小小影舞,紫若雪,夜冷月,依Yi,为剖覅还,别开枪是我,超级幸福,真的爱你,真的和睦,真的友情,滴滴,三国恋,三国杀,三国志,四大皆空法律分,' \
                '四大皆空法律我,四大皆空法律啊,四大皆空法律公会,四大皆空法律发,闪电法为,福娃发生,福娃五的方式,的房间号发还,四大皆空法,四大皆空法律,' \
                '离开了还,iOS大哦哦,亿熊安抚你,我就放假啊在,加上胜多负少的,了科技开发,代理商福克斯,大飞机扣搞好,欧五哦啊在,你下次即可,我一而佛吉还,' \
                '二铺还奥开发,士大夫人人网,为剖覅还,真的口嗨,真的愉快,真的勤快,真的认真,真的小巧,真的健康,真的干净,超级开心,三国恋,三国杀,三国志,' \
                '四大皆空法律分,四大皆空法律我,四大皆空法律啊,四大皆空法律公会,四大皆空法律发,闪电法为,福娃发生,福娃五的方式,的房间号发还,四大皆空法,' \
                '四大皆空法律,iOS大哦哦,亿熊安抚你,我就放假啊在,加上胜多负少的,了科技开发,代理商福克斯,大飞机扣搞好,欧五哦啊在,你下次即可,我一而佛吉还,百花繚亂'


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
