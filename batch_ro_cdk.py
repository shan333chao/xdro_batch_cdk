import time
import requests
import ddddocr
import random as rd
from urllib import parse

# 礼包兑换码
gift_code = '1021LZF4DQY'
# 服务器列表
#  守护永恒的爱 = 10001
#  梦想天空 = 10001002
#  辉煌领域 = 10001003
server_id = 10001
name_list_str = '匪帮传奇,小桃子,牛油丶果果,莉莉丝露,龙猫,浮羽派丁,落羽霏霏,芙鈴,猫猫不乖,無限大xun,魅影,绿绿绿绿,喝酸奶的老鼠,最多打两下,调羹SAMA,毒岛莉莉,\
                王者羽毛,暴躁大叔恺,夜大宵,紅人,请叫我壹伍零,波利超人,怪你过分美丽,Chiron,还没睡醒,希小辰,\
                奶酪蛋糕,熊本熊丶,雨落静寂,派大星丶,娜娜酱,可爱大布丁,轰毒了牙拉,拉拉个大脸,何仙姑1984,那个难人,咸豌豆,无心の小圆子, \
                金色,小桃儿素未央,咔车開车咔丁车,yoyoQ,雪染羽,爱睡无罪,甜豌豆,清橙,落萧萧,其实我是一个演员,阿斯兰乔, \
                喵喵胖,是星野阿,Bard,王者羽毛,旺旺碎冰冰,小王快救我,牛油丶果果,灌奶小白,倔强的微笑♬,陈先生·'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
submit_url = "https://party.xd.com/event/2017jana/ajax_submit"


# 保存验证码方法
def save_captcha_pic(img_byte):
    filename = str(time.time()) + '_captcha.jpg'
    with open(filename, mode='wb') as filename:
        filename.write(pic.content)


ocr = ddddocr.DdddOcr()


name_arr = set(name_list_str.split(","))
result_dic = {}
for role_name in name_arr:
    role_name = role_name.strip()
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
        # save_captcha_pic(pic.content)
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

print(result_dic)
