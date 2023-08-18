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
server_id = 10001
name_list_str = '今生只为遇见你,cnhdy,静静的生z,立于色眼眸,扒金小分队10,人偶学员,被十面埋伏,尽桃bv,撒撒立正躺,完美的欠,可爱在可爱,霍霍有一天,' \
                '剪刀嘟嘟,记忆中的玛妮,飞跃地心,残月夜半撩人,auv卡册39,狐系恋爱手册,倾心之vf,auv卡册10,auv卡册37,问题一起,塔罗式恋爱,我就只尝一小口,' \
                '不能恋爱的秘密,climateo,放纵情欲的夜晚,十荒六梦,影子写手,quity,醉酒成熟點,我就是一个忍者,刺穿长风的箭,gomo,扒金小分队15,草莓超人西瓜蛋,' \
                'hetunc,理想的征途,乖=猪乖=猪,auv卡册06,临时女友,auv卡册55,杰瑞德森,近失iu眠成,auv卡册73,auv卡册14,大家目前,首席御灵师,亏欠寂寂寂,mitoo,' \
                '天使替你演,auv卡册064,mintoz,扒金小分队16,auv卡册50,谁的青春不热血,锦衣卫之下,大脚皇后,远山如黛,mentalz,章鱼小肉丸,信仰的光华,装作不淡夏,' \
                '萌医甜妻,吹个五彩的泡,狂神魔尊,熟點患者,温暖的味道,auv卡册02,auv卡册65,决胜大战衣,向我的心脏开枪,kojzf29,小林家的龙女,曾给过,auv卡册66,扒金小分队21,' \
                '扒金小分队14,auv卡册16,绝品王妃,再演痕累累,蓬莱剑,你怎么又来了,我就是壹個忍者,auv卡册11,天星晶晶晶晶,如影随心,恶魔恋之歌,苦练叉腰肌,唤唤,auv卡册71,扒金小分队8,' \
                '屿暖森森森森,扒金小分队11,三生三世书上枕,auv卡册32,auv卡册58,懂柠檬的懂柠檬,auv卡册28,后罗曼史,崇拜,安静静的生活,无敌美少女,我不是购物狂,薄荷之夏夜,曾遇见比相爱更,' \
                '扒金小分队23,昭华缭乱,sendcpz,那道傷z,auv卡册57,扒金小分队26,日常悠哉,莫里亚蒂娜,少年末路?,扒金小分队29,淘汰左,阿斯特里克奇,绝代小娇,人间烟火花小厨,auv卡册36,' \
                'auv卡册70,嘘不要说话,kojzf6,扒金小分队17,唯一的开了口,阴天快乐耶,auv卡册20,小海绵,烟雪漩涡,扒金小分队25,auv卡册22,二蝗止,乙女游戏,嘴角的弧來唯美,阳下锝背bt,' \
                'tubughd,夏日幽会,哒哒音草莓,auv卡册51,auv卡册03,旋律、猪萌,扒金小分队9,auv卡册74,JustOK,爱情转移了,auv卡册12,估才瞳,锦心似玉,抹茶糯米团子,※零時差,神印王心,' \
                '肉肉肉,x86xc,异世界迷宫,扒金小分队12,biliop,我能看到成功率,bzdwa,auv卡册21,auv卡册76,auv卡册15,auv卡册31,春风云朵耳,auv卡册19,安放的小情,珠止肝,听、忧听、忧,' \
                '悄然之星,auv卡册61,kojzf26,浮云中的奇葩,橙子与阳光,登录,魔幻仙踪,80多的吧,扒金小分队32,auv卡册38,情陷聊斋,你最浮夸,yittlz,王爷是只大脑斧,枪火天灵,auv卡册33,' \
                '扒金小分队31,含思含思含思,auv卡册63,天鹅套索,水蜜桃女孩,auv卡册60,山河欲与来,扒金小分队20,时空陷阱,扒金小分队30,遗忘的美妙时光,专业抢坑挂机,auv卡册69,热血同行,' \
                '孤勇者阿,初透陌e天使,纯白之音,遇龙,自然就分子子,gopand,放学别跑呀,不羁的腿毛,时光代理人,最佳损友哇,扒金小分队7,极道宗师,conceive,独步逍遥,可一可再吗,auv卡册53,' \
                '再美、也是伤痕,auv卡册72,kojzf24,处安放的小情,风暴舞,煎美丽,海吉拉,harvest,夕阳无限好吗,auv卡册08,亲爱的她,auv卡册07,看看大家哦,citydfhf,扒金小分队28,哦哦牛,' \
                'auv卡册29,独酌亦可,万界独尊,auv卡册56,倾世宠妃,yutinc,auv卡册75,milciko,我真的可以了,南哲巢青,特薦的美美,auv卡册52,煙熏知濃,扒金小分队13,西瓜美小学,auv卡册68,' \
                '扒金小分队24,喵情许愿,处安放的xx,冰蓝色味过去,京酱肉斯,花好月又圆,auv卡册34,auv卡册01,蜜的可,auv卡册09,央央央yush,auv卡册24,光倾光倾光倾光,梦残味过去,恨恨恨,碰阳光°伸,' \
                '再来杯咖啡,骊耻收,auv卡册54,auv卡册62,女友成双,相许?笔画,棺姬嘉卡伊,新奇世界物语,柠檬的酸妖妖,超小笨笨,望天福乐明,auv卡册05,春有着放眉眼,太玫县,润桔润桔润桔,auv卡册67,' \
                'auv卡册59,微的苟眼眼,ctonyz,auv卡册30,柔的废话作F,花一世忆者,十年啦,有我你要,吉谢尔,来杯咖啡,良的失心,lookupo,auv卡册27,只有芸知道,扒金小分队19,星辰斗士,auv卡册18,' \
                '从地球降落,克U笔女人,我丢了你的螺母,用止大,qutezd,Argon,auv卡册25,最后的云歌,嚣张的废铁,火焰粉,quickyc,受控活活活活,双世小仙妻,扒金小分队27,yougaimi,瓦尼塔斯,钻心的疼依依,' \
                'auv卡册35,通通通通,magan,auv卡册26,头发是白颜色的,cartont,auv卡册04,gcvi,兔兔可爱,如今旧城归她人,喏vgl,扒金小分队22,作False,红领巾么,子你cc个哦,cahuci,王者公孙离,' \
                '逆光下的,红色糖果,cookid,auv卡册13,我就是忍者,扒金小分队18,城城灵魂灵魂,寒蝉辰光,auv卡册17,huwaz,解离妖圣,auv卡册81,吃兔子的糖,wejsike8,艰卫入,四件哥F,壹拾捌a,是H大家,' \
                '外圣贰贰,8s520y8,5s249y5,二么,肆拾,fgvs123,姝寒冰冰,我心依旧81,死党单飞,auv卡册82,笔旧五,hn845u0,赚钱小能手41,Onion丶,小鲨·,对那渐,doqer4,紫珺紫珺紫珺,四件哥X,叁拾捌a,' \
                'deuqi9,11111日期,法夫与,夏天de小P,处旧剖,神之法魔,剑痕,工作工作唉,cuyyt,幽灵灵猫,真爱在隔壁,上海目前,垢玉瞳,城下玷,大刀阔斧的,无大碍,A3托耶夫斯基,大了也是,红烧肉肉肉,doqer0,' \
                '曾经心动,Gone,萌萌哒的小羊羊,le082o3,Tony空空空空,珠诉用,饿通天塔人,心之悦,壹拾玖,auv卡册80,sa409y5,桃井五月,8s743y8,skyion,流龙城,无双绫魂,卓嘎珠,怀下二,牛发过剑,my243w7,' \
                '今日可将可,auv卡册78,凤鸣路,1s380y1,需要而,景科主,7s162y7,TuTu愛你,deuqi4,森林不,娃哈哈娱乐,昨就吕,抗压吧务团队5,小悠小丝光,doqer2,deuqi3,冰天龙神,zdcde,王者天翼,战利景,' \
                'tx409n5,一下与,贤小樱,克拉克森了,甜的兮草莓草莓,肆柒壹,实丐二,垢让暗,deuqi10,基金大师傅撒,auv卡册77,致无聊的开始,胞磷胆碱,13321358,神神罂,auv卡册86,上暗折,黄蓉,0s635y0,' \
                '有机会按,蝇让阳,小肥,auv卡册84,夏之力萌萌,ty店、店长阿飞,寺寺三,邱桌上,大漠硝烟,deuqi7,宝宝籽,哎哟喂12345,小嘉子,葬v无情,咖啡女,希潴儿,胡原妈,小小米波,段四元,e期盼上海,漫山遍野菊花香,orange橙,Jaje,' \
                '胡三参,睡觉觉说你呢,与天天材,发呆发呆22,梦红墨成花,喵咕喵咕喵咕咕,小飞侠kobe,auv卡册88,大家来打,小铁匠人生,伟儿,睡搞的,上天可以,胡寺屯,doqer5,天天乐乐小雅,叁拾玖a,枯树林壹,量扩和,' \
                '会计小忧,Ekko,auv卡册85,47962244,给电饭锅的,doqer5,9s376y9,亞雷克斯·但丁,袭人者桃桃,ho106w8,阿诺_小喇叭,哦呼CC,fds3321,隔壁小哆哆,于人于己,贰拾,柳小仙,8s275y8,doqer8,' \
                'LOtwo,玫垢夺,doqer7,8s439y8,BiuBoom,谎話先生°,子书灸舞,wejsike9,罂与樱,65565,阿祺,auv卡册79,7s496y7,查一下王,睡旧则,我们不屑一顾,doqer9,一眼上海,躲猫猫射怪兽嘻嘻,炒菜目的,浊量中,' \
                '9s278y9,doqer1,deuqi8,精炼15武器,吴应聘,auv卡册87,deuqi6,霜凝寒羽,都快肥,g奇木,外圣壹贰,员上寺,yutic,特困户发货,6s241y6,doqer10,doqer0,doqer11,doqer5,wejsie10,' \
                '震腾藤,LK轮戈,小P之家,红色柳丁,载震荡,模压田,啊械另,莎煲拳,劳田要工,LK轮遥,灰机露,行走带风,Knight灬丶,火红火绿C,521枯黄4,苛国肿,苦过dede,呃O呃,LK轮式,萌萌哒小奶牛,LK轮工,ycck,' \
                'YEMMZE,521枯黄5,Muisaius,工嘿耍花,借助本原,南夕鱼儿,?椿糠云,回旋木马,周子翼,千年眼神'

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
        with open(file_name, mode='a', encoding='utf8') as filename:
            filename.write(exist_names_str)

        print(ujson.dumps(result_dic, ensure_ascii=False))
    else:
        print(f"名单中的{len(exist_names)}人已经都领了")
