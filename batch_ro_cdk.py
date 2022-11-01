import time
import requests
import ddddocr
import random as rd
from urllib import parse
import os

import ujson

import gift_key

# 礼包兑换码
gift_code = gift_key.GAFT_CODE
# 服务器列表
#  守护永恒的爱 = 10001
#  梦想天空 = 10001002
#  辉煌领域 = 10001003
server_id = 10001002
file_name = gift_code + "_" + str(server_id) + ".json"
name_list_str = '慈祥保温杯,焱爷,讲道义签字笔,老王帮你把家看,榴蓮妹←,浮ˇ,暴躁射射小队贰,皮色,调羹SAMA,普福,桃蛋,失望火腿肠,薛家强,' \
                '啾咪★,笨笨小恶魔,lian丶芯,牛牛电动,六宝,监视你挂机,夜大宵,先开好扔着,憨厚芒果,这个名字真好,刚分手汉堡包,拐角遇见默默,娜娜酱de大徒弟,' \
                '你午睡了吗→_→,Graceee,拉拉个大脸,It_is_me,慈祥柿子,空口吃白刃,阿斯兰乔,咸豌豆,飘逸毛巾,独立日记本,金色,箱子的专用女仆,' \
                '昱下摞你命,那个难人,又双叒叕喝奶茶,暴躁射射小队肆,气宇轩昂葡萄酒,苦恼大熊猫,耀、,小王快救我,文质彬彬便当,喝酒烫头,' \
                '飘逸牛肉面,是星野阿,波利车红人派大金,气势凌人碗,小奶、,莉莉丝露,熊本熊爱徒01,mice02,大力吐司,沉着大熊猫,抹茶糖豆,yoyoQ,偏偏爱上你,长着狐耳の猫,' \
                '忆小姐失眠中,猪汪汪,不喝酒的妹妹,守护永恒的骑士,小小小鬼এ,霞飞路87号,微醺麦片,猫猫不乖,ʚ福福ɞ,留胡子草稿本,無限大xun,娜娜酱,爱热闹消炎药,随机是谁,' \
                '捡碎片卡片的BB,儒雅汤圆,紧张钱包,小桃儿素未央,谢瑾瑜,温文尔雅火柴,调皮啄木鸟,夢瀟湘★,新港西猎人A,叔打一,没有腹肌灭火器,绿绿绿绿,秋雨头微寒,龙猫,暗恋学妹柑橘,' \
                '希小辰,你们全都是NPC,新港西猎人C,不要绿我鸭,皮蛋妞,游手好闲熊本熊丶,派大星丶,idar君落羽,鼻子大红薯,飘逸钥匙扣,快给我泡杯茶茶,闪闪发光d,' \
                '時光丶,陈先生·,从容白开水,果断手链,刚失恋钥匙,满满胖丁,妖刀十六月夜,牛油丶果果,知识渊博拖把,落羽霏霏,贰捌,大哥莫封,依日哆,火焰龙蛇兰,机灵骆驼,' \
                '氵查查查,居尔一拳,花开朵朵,熊本熊爱徒02,骑白马火车,花季ω莫淺憶ღ,纯真围巾,耀丶,彷徨海豚,不敢表白拐杖,一骑,很拉风西瓜,灬羞羞脸灬,文雅洋葱,爱睡无罪,暴躁大叔恺,' \
                '次次次次次都打我,T箱子T,朴实无华的老实人,ʚ糖糖ɞ,莫可与之名,心软盒饭,英姿勃勃西瓜,金色,阿克塞迩,游手好闲熊本熊丶,玉树临风马克杯,魔法少女茵,拐角,波利超人,' \
                '春去花还在,★咪哒,小叽,高大汉堡包,小老鼠mice,あやね,靈魂收割者,乐观台灯,爱吹牛青椒,甜豌豆,灌奶小白,火焰龙舌兰,浪子不回头丶,大气香菜,光明磊落便当,' \
                '七缘红线,严肃伤疤,个性花卷,暴躁射射小队叁,随机是税,随机是水,雨季ω莫懮離ღ,卖萌机器人,百命藏麟,毒岛莉莉, 小老鼠mice,麻煩,火岩龙舌兰,Chiron,' \
                '倔强的微笑♬,害羞大脸猫,不安分的咕咕,QQ~~QQ,霸者横栏,千惊万喜,雪染羽,喵喵胖,ღ顾影自怜丶,xFad,甜心芝士,聪明葡萄酒,倔强的微笑,玫瑰花的葬礼,萌奇D烤粽子,浮、,' \
                '无聊打钱玩,憨厚乌龙茶,喝酸奶的老鼠,洛煌,坏坏韭菜,那玛泽比,近视木瓜,从前的我现在的你,马卡龙发达,小朵朵朵朵,坚韧高山,纯真感冒药,苏苏苏大এ,' \
                '浮羽派丁,帝君痛痛盾盾,捡碎片卡片的BB,二骑,酸豌豆,娜娜酱de小徒儿,阳光领结,任性蚂蚁,夏凉雨落花,凤凰之羽,玫瑰小班,むつおみ,绅士水煮肉,狂野刺猬,水果圆子,无心の小圆子,' \
                '斯文电脑桌,Sour丶酸,你眼里有星星ღ,ʚ李君君ɞ,吹鸡,喝酒撒盐,喝醉警车,阿斯蒂芬07,彩虹丶婲°,可爱大布丁,松花鹌鹑蛋,星夜无尘丶,淡定手套,戒与不戒,星期六下午,艾伦C7,乔宝,' \
                '刷分复活专用,阿阿阿光এ,近视冰棍,暴躁射射小队壹,火爆蚂蚁,冷静甘蔗,精明西装,星期六打补丁,无心z,花落不凋零丶,繁花祭,ALin宝贝,谦和咖啡,清橙,怪你过分美丽,一箭一个蛋蛋,' \
                '眉毛粗卡布奇诺,芙鈴,龙猫ˇ,其实我是一个演员,大哥别封我,江湖人称牛白刃,何仙姑1984,直爽鸵鸟,神经兮兮,最爱喝兽奶,匪帮传奇,憨厚打火机,苓香,秋雨透微寒,刀宝,红薯栗子,' \
                '大方长颈鹿,星期六打球,丘比特,海淀第二狠人林虤,无聊紫菜,面冷心慈冰淇淋,酒量小电梯,沐小西oO,秋雨透胃寒,不羁滑板,不二大侠,冰冰红顺旺,甘缇亚娜,星夜无尘丶,浅墨无痕丶,' \
                '英姿勃勃棒棒糖,光明磊落显示器,云烟缭绕,哒哒里鸭,魅影,笑点低领带,Rocky丶,威武稀饭,爱跑步紫菜汤,星期六打嗝,肯德超,洛克先生,绯色星屑,黄昏十二乐章,打手兔,落萧萧,尐尛奶茶,' \
                '咖喱魚蛋、,i0lz,随机是睡,木纹如水丶,还没睡醒,Bard,爱听歌钱包,新港西猎人B,夏陌,熊本熊爱徒03,祸～祸,风季ω莫嘆惜ღ,艾伦C7,依旧八斤,爆爆猎,锦鲤宝宝,月下雪妖,香酥菇,牛王妹,' \
                'Glow灬,猫在午夜时笑着,是浮生呀,别吧别吧别吧,嗯嗯噢噢对对,溜了溜了溜了,啊这啊这啊这,為所欲为,芝士雪豹,biu动感光波'

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
