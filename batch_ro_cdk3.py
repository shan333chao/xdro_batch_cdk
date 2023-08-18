import time
import requests
import ddddocr
import random as rd
from urllib import parse
import os

import ujson

import gift_key

# 礼包兑换码
gift_codes =gift_key.GAFT_CODE
# 服务器列表
#  守护永恒的爱 = 10001
#  梦想天空 = 10001002
#  辉煌领域 = 10001003
server_id = 10001003
name_list_str = '来杯咖啡,机灵骆驼,王者马可波罗,独步逍遥,远山如黛,肉肉肉,兔兔可爱,儒雅汤圆,没有腹肌灭火器,打狗棒法,光明磊落显示器,失望火腿肠,' \
                '嘘不要说话,可爱二多笨笨,高大汉堡包,可爱二多笨山,大气香菜,我就是忍者,mitoo,沉着大熊猫,渺鲨,打猫棒法,可爱二多笨贰,可爱二多笨亿,' \
                '可爱二多笨无,打蛇棒法,知识渊博拖把,老臣黄汉升,坚韧高山,憨厚芒果,最后之境,坑货李元芳,害羞大脸猫,时光代理人,哲仁王后,纯真围巾,' \
                '王者铁木真,淡定手套,个性花卷,最强王者伽罗,菜鸟百里守约,小海绵,可爱二多笨肆,无敌美少女,奥德赛降临,首席御灵师,章鱼小肉丸,阴天快乐耶,' \
                '飘逸艾琳,最佳损友哇,爱听歌钱包,王者公孙离,苦练叉腰肌,月光变奏曲,人来人往勿失勿忘,喝什么,猜什么,大弦嘈嘈如急雨,王者虞姬,吃什么,' \
                '似诉平生不得志,低眉信手续续弹,卡妙,王者孙尚香,鲁班7号,轻拢慢捻抹复挑,冰泉冷涩玄凝绝,弦弦掩抑声声思,间关莺语花底滑,焖猪耳朵,红烧猪耳朵,' \
                '瞬瞬,想什么,欧巴思密达,做什么,千古善废柴,童虎,嘈嘈切切错杂弹,炸猪耳朵,大珠小珠落玉盘,小弦切切如丝语,星矢,千古爱废柴,喜马拉雅山,王者后羿,' \
                '幽咽泉流冰下难,逛什么,念什么,baby金刚娃,辉辉,初为霓裳后六幺,未成曲调先有情,说尽心中无限事,烤猪耳朵,' \
                '九级心震,美美子,你的眼,教之道A,静待-花开,姐是霸气范,清风配酒,单纯の爱,共灯一盏,落笔映惆帐,青丝绕,巧力菇,再无第二,望竹怀柔,' \
                '烟尘花锁眉,动感光波bibi,执扇琅珠,人情薄如纸,删了回忆录,我宠n,鹭落霜洲,不讨蘑,墨染卿程,习相远A,骑着蜗牛闯红灯,桔桔子,断机A,' \
                '性相近A,马尾衬衫九分裤,南巷七秒鱼,性本善A,唱过阡陌,Lank蓝琪梦莎,共我西窗夜话,嘴角残存的微笑,呗范,鎖碎,嗨翻天哦,荒城旧日,男配角,' \
                '暴躁尤物,惊线辉砍月,陌念念,另一个天堂,木瓜粉,春日桃绘,逆光夏花,拒绝一切,限量版的青春,恋恋百合,教五子A,花醉染、墨瞳,霓虹溢彩街头,' \
                '顾虑,择邻处A,异域之巅,洗尘衫,动了弦,蓝調,粉蝶のlove,秋雨涩,谭玥紫肠,清醇茉莉,耗尽余生,我叫倍儿坚强,玩偶亦墨,伤感若影,茶山的鹿,' \
                '快播少年,冷晓汐,强颜欢笑,我最在手呢,叶璃溪,毁心葬情,温婉娇俏,窦燕山A,有义方A,性乃迁A,人比烟花寂寞,穿一席整裙,妹子wo17岁,昔孟母A,' \
                '晴昼烟雨长,你若离去后会无期,如梦初醒,苏仙小可爱,承★诺迷No黎,花花小朵朵,子不学A,幸幸子,沙哑情歌'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
submit_url = "https://party.xd.com/event/2017jana/ajax_submit"


def read_recived_log(file_name):
    received = []
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf8') as f:
            name_str = f.readline()
            received = name_str.split(",")
    return received


ocr = ddddocr.DdddOcr()


name_arr = set(name_list_str.split(","))


for gift_code in gift_codes:

    file_name=gift_code + "_" + str(server_id) + ".json"
    exist_names = read_recived_log(file_name)
    result_dic = {}
    for role_name in name_arr:
        role_name = role_name.strip()
        if role_name in exist_names:
            continue
        if len(role_name)==0:
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
        with open(file_name, mode='a',encoding='utf8') as filename:
            filename.write(exist_names_str)

        print(ujson.dumps(result_dic, ensure_ascii=False))
    else:
        print(f"名单中的{len(exist_names)}人已经都领了")
