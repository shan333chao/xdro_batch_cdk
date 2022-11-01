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
server_id = 10001002
file_name = "all_" + gift_code + "_" + str(server_id) + ".json"
name_list_1 = '煙熏知濃,红领巾么,gopand,时空陷阱,milciko,双世小仙妻,kojzf24,cnhdy,章鱼小肉丸,quity,剪刀嘟嘟,扒金小分队8,遗忘的美妙时光,最佳损友哇,悄然之星,花好月又圆,' \
              '80多的吧,骊耻收,亞雷克斯·但丁,神之法魔,喵情许愿,自然就分子子,扒金小分队32,十年啦,可一可再吗,yutinc,不能恋爱的秘密,抹茶糯米团子,mitoo,扒金小分队10,王者公孙离,烟雪漩涡,' \
              '扒金小分队23,太玫县,肉肉肉,扒金小分队30,极道宗师,旋律、猪萌,小肥,conceive,绝代小娇,大家目前,夕阳无限好吗,温暖的味道,临时女友,扒金小分队17,基金大师傅撒,扒金小分队7,' \
              'kojzf29,那道傷z,从地球降落,mentalz,kojzf6,扒金小分队12,倾世宠妃,我丢了你的螺母,光倾光倾光倾光,异世界迷宫,人间烟火花小厨,唤唤,扒金小分队16,塔罗式恋爱,夏日幽会,' \
              '锦衣卫之下,阿斯特里克奇,喏vgl,citydfhf,寒蝉辰光,枯树林壹,十荒六梦,头发是白颜色的,来杯咖啡,橙子与阳光,auv卡册02,信仰的光华,扒金小分队19,如影随心,天鹅套索,影子写手,' \
              '扒金小分队24,超小笨笨,吉谢尔,乙女游戏,浮云中的奇葩,阴天快乐耶,lookupo,kojzf26,扒金小分队21,恨恨恨,莫里亚蒂娜,扒金小分队27,auv卡册064,火焰粉,遇龙,扒金小分队29,' \
              '通通通通,纯白之音,神印王心,珠止肝,红色糖果,瓦尼塔斯,你怎么又来了,淘汰左,嚣张的废铁,嘴角的弧來唯美,qutezd,嘘不要说话,小林家的龙女,扒金小分队18,放学别跑呀,碰阳光°伸,cartont,' \
              '草莓超人西瓜蛋,完美的欠,无敌美少女,扒金小分队22,扒金小分队14,爱情转移了,最后的云歌,yougaimi,梦残味过去,情陷聊斋,恶魔恋之歌,刺穿长风的箭,问题一起,霍霍有一天,听、忧听、忧,' \
              '有我你要,yittlz,cookid,天使替你演,风暴舞,良的失心,被十面埋伏,可爱在可爱,逆光下的,绝品王妃,magan,吹个五彩的泡,bzdwa,飞跃地心,受控活活活活,锦心似玉,不羁的腿毛,' \
              '安静静的生活,我就是一个忍者,mintoz,残月夜半撩人,quickyc,小嘉子,央央央yush,你最浮夸,特薦的美美,南哲巢青,再美、也是伤痕,向我的心脏开枪,苦练叉腰肌,auv卡册09,估才瞳,' \
              'fds3321,乖=猪乖=猪,扒金小分队13,远山如黛,昭华缭乱,微的苟眼眼,扒金小分队9,我就是忍者,记忆中的玛妮,克U笔女人,子书灸舞,唯一的开了口,cahuci,狐系恋爱手册,二蝗止,后罗曼史,' \
              '扒金小分队20,独步逍遥,醉酒成熟點,决胜大战衣,煎美丽,王爷是只大脑斧,扒金小分队15,蜜的可,孤勇者阿,独酌亦可,静静的生z,huwaz,我就只尝一小口,花一世忆者,子你cc个哦,climateo,' \
              '扒金小分队11,日常悠哉,熟點患者,biliop,JustOK,扒金小分队31,冰蓝色味过去,看看大家哦,只有芸知道,棺姬嘉卡伊,hetunc,屿暖森森森森,狂神魔尊,理想的征途,钻心的疼依依,' \
              '亏欠寂寂寂,今生只为遇见你,亲爱的她,热血同行,万界独尊,倾心之vf,Argon,ctonyz,扒金小分队25,萌医甜妻,扒金小分队28,哦哦牛,装作不淡夏,山河欲与来,解离妖圣,水蜜桃女孩,大漠硝烟,' \
              '扒金小分队26,用止大,x86xc,含思含思含思,哒哒音草莓,人偶学员,如今旧城归她人,新奇世界物语,蓬莱剑,赚钱小能手41,星辰斗士,首席御灵师,立于色眼眸,tubughd,我真的可以了,阳下锝背bt,' \
              '杰瑞德森,薄荷之夏夜,专业抢坑挂机,三生三世书上枕,放纵情欲的夜晚,再来杯咖啡,兔兔可爱,春有着放眉眼,王者天翼,枪火天灵,海吉拉,我就是壹個忍者,近失iu眠成,大脚皇后,再演痕累累,谁的青春不热血,' \
              '魔幻仙踪,sendcpz,西瓜美小学,时光代理人,尽桃bv,小海绵,女友成双,gomo,我能看到成功率,曾给过,auv卡册05","auv卡册32,auv卡册53,auv卡册22,auv卡册60,' \
              'auv卡册80,auv卡册33,auv卡册35,auv卡册62,auv卡册10,auv卡册38,auv卡册88,auv卡册50,auv卡册55,auv卡册85,auv卡册20,auv卡册81,' \
              'auv卡册29,auv卡册18,auv卡册30,auv卡册63,auv卡册21,auv卡册15,auv卡册36,auv卡册16,auv卡册39,auv卡册65,auv卡册25,auv卡册54,' \
              'auv卡册28,auv卡册68,auv卡册52,auv卡册86,auv卡册13,auv卡册19,auv卡册11,auv卡册58,auv卡册14,auv卡册84,auv卡册12,auv卡册59,' \
              'auv卡册82,auv卡册34,auv卡册31,碎离皆回忆ww,auv卡册04,auv卡册01,深爱你,auv卡册08,auv卡册03,鸢年,auv卡册06,auv卡册71,auv卡册76'

name_list_2='儒雅汤圆,大气香菜,卖萌机器人,留胡子草稿本,爱吹牛青椒,果断手链,刚失恋钥匙,高大汉堡包,玉树临风马克杯,憨厚打火机,火爆蚂蚁,绅士水煮肉,心软盒饭,淡定手套,无聊紫菜,光明磊落显示器,骑白马火车,' \
            '纯真围巾,严肃伤疤,气势凌人碗,爱跑步紫菜汤,害羞大脸猫,知识渊博拖把,坚韧高山,大方长颈鹿,慈祥柿子,英姿勃勃西瓜,机灵骆驼,失望火腿肠,憨厚芒果,面冷心慈冰淇淋,温文尔雅火柴,光明磊落便当,精明西装,' \
            '讲道义签字笔,飘逸牛肉面,谦和咖啡,个性花卷,鼻子大红薯,紧张钱包,没有腹肌灭火器,文雅洋葱,眉毛粗卡布奇诺,喝醉警车,大力吐司,从容白开水,笑点低领带,刚分手汉堡包,爱听歌钱包,斯文电脑桌"，"OK光姐妹,' \
            '最后之境,真爱不迟到,某日某月,扛鼎黑,00猫19,恋之酒滴,淡定瀑,深深地恋爱,爱情有点怪,若流,哲仁王后,强悍汽,体贴西,坚韧小摩,奋斗帽,00晟06,玩手机鞭,00猫02,多米那,开朗烤红,燕归西窗月,' \
            '五月的青春,00晟05,高大馒,涅墨西斯丽,天妖宝录,风流茶,玫瑰与郁金香,甜甜的家伙,魔法水果篮,阿稚阿拉,干练柿,天降萌宝,樱之塔,青青大树,深情茶,谦逊番,月光变奏曲,风姿物语银河,00猫03,' \
            '夏日小伙伴,Fairy兰丸,冷冷烤土,要出家乌冬,儒雅红 '
name_list_str = name_list_2

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
