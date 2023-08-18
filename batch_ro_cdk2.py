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
server_id = 10001002
name_list_str = '慈祥柿子,讲道义签字笔,无敌美少女,果断手链,大力吐司,飘逸牛肉面,刚失恋钥匙,爱跑步紫菜汤,大气香菜,严肃伤疤,鼻子大红薯,谦和咖啡,' \
                '骑白马火车,文雅洋葱,害羞大脸猫,坚韧高山,喝醉警车,英姿勃勃西瓜,精明西装,纯真围巾,失望火腿肠,淡定手套,高大汉堡包,光明磊落显示器,' \
                '绅士水煮肉,刚分手汉堡包,火爆蚂蚁,儒雅汤圆,光明磊落便当,知识渊博拖把,憨厚芒果,没有腹肌灭火器,沉着大熊猫,卖萌机器人,个性花卷,' \
                '从容白开水,温文尔雅火柴,笑点低领带,紧张钱包,心软盒饭,爱吹牛青椒,憨厚打火机,玉树临风马克杯,爱听歌钱包,面冷心慈冰淇淋,留胡子草稿本,' \
                '斯文电脑桌,眉毛粗卡布奇诺,机灵骆驼,气势凌人碗,大方长颈鹿,无聊紫菜,00猫02,要出家乌冬,谦逊番,樱之塔,干练柿,阿稚阿拉,某日某月,奋斗帽,' \
                '风暴舞,苦练叉腰肌,00猫19,只有芸知道,温暖的味道,月光变奏曲,青青大树,遇龙,强悍汽,深深地恋爱,五月的青春,燕归西窗月,深情茶,海吉拉,扛鼎黑,' \
                '00晟06,Fairy兰丸,坚韧小摩,玫瑰与郁金香,体贴西,冷冷烤土,玩手机鞭,亲爱的她,Argon,爱情有点怪,天妖宝录,风姿物语银河,今生只为遇见你,淡定瀑,' \
                '甜甜的家伙,哲仁王后,独步逍遥,00晟05,涅墨西斯丽,肉肉肉,莫里亚蒂娜,来杯咖啡,真爱不迟到,儒雅红,风流茶,mitoo,魔法水果篮,OK光姐妹,高大馒,' \
                '天降萌宝,章鱼小肉丸,小海绵,红色糖果,最后之境,开朗烤红,多米那,恋之酒滴,如影随心,00猫03,夏日小伙伴,纯白之音,过户费87,斧氏集体g,' \
                'shshen20,fgg大观园,ytudr5,斧氏集体ds,斧氏集体Q,浅雪忆,羽族小野,威威大师傅,非国有1,斧氏集体v,斧氏集体x,斧氏集体W,刚好回家3,梵蒂冈28,' \
                '斧氏集体z,斧氏集体b,斧氏集体i,滲透悲傷,少灬轻狂刂,斧氏集体E,蒂法那,斧氏集体c,以后热土5,gfd456,╰★╮花生果,斧氏集体n,太容易6,斧氏集体m,sss13,' \
                'FmoSZNW,Qh6vetk,SypbDVH,OSqVx65,dRj48Uy,vcKAD4a,8epd9Kj,wqgkAF9,qCkOF58,UVoRDEK,SaXLbUt,Oz1ySPE,n4dWcW4,zeKCx9u,3CmDc3Q,' \
                'ioBeNSt,jaYOnS7,xvxdv,pMbQRNA,b5LikG2,stCKHvs,JQckxob,sYVpo3Z,iGXjGNg,694e50y,kf8H7w7,oAUiL1T,002VWxX,K8R7tcG,thIMngv,' \
                'ldwRVI3,iDQ00g4,YQPGHnY,wawivt4,7Wfg1Mz,zLUiZki,4Wvjg8j,W3HCzd0,EmC2Nl8,3OStW9N,AQ8c3ST,CtfC9ET,9vo6UxG,asfasdda,aFpJH8m,' \
                'kkYSEeZ,PTPX8Sq,YhWCCzC,G9bQYXP,u4cVn1u,Iv7CwDs,S7pladu,Uw80ef5,oPkIhvb,wI6XRkS,XYN30sa,dcQTZ9L,aIWFonA,11kebRO,AGEwCDq,' \
                'syEGR37,CtTappz,GUrnyT3,baQo7SZ,tEgstBT,7dzttzB,ChXca8I,NzRmH19,Z8y51JF,a07dYNO,kpBV46G,VOnfq48,A2OH7rA,hTRs94p,G38s4by,' \
                '6xubHXb,9BePOkY,MQgOKX9,3bo7PWA,u5wKqg2,p8e7GIe,7l0jtS3,zSAdg2D,Bz7KSoI,LW4WgeU,3h2wLP7,gGONI6j,LrPm1P7,dggo,oBQIrJM,lK45rxk,' \
                'EysyAU4,SSKYKfj,uzCnXZU,PWs3TuX,YbsV5eu,UL562Id,mJ2pPaP,gsfsgf,cInisRr,ZwAbibm,wAe2VZQ,LQ9wu6k,H0XTfys,mGwpfXn,WnB1Jmn,' \
                'nMZwgKw,qrhPlMt,bPF03XL,tjfjy,sS18RaQ,uP1kC6M,mgjxDB3,NklqfY3,QNOu6CZ,SkKQKnB,96jTZNA,SnStrEQ,4gl82cm,eI4WAKg,mZBWzyO,' \
                'RAlLb5J,PsFcDtO,dWWOOJI,HXFLxwP,oDaNpuL,91CS1Y9,ptvo5Mk,hLkw3ej,42TIwGb,6TrUME1,1YC20sy,dTpPwqI,新政策v,Lye3ZHa,rf4ew7n,' \
                'onr4AOf,frRsh00,uurOa2G,Ah6tO0o,0imAOBW,Bp1ojfL,JojCeGg,WIWfLdH,p6Lr284,aYcegWk,lfYfm3m,E6dL5Lu,TD76VrN,crj04B0,EW7lu82,' \
                'pEbQSkt,PAAq3Yg,Epon7hP,YneOUEW,tyjyrjy,tHFfPtQ,ckzDQ2N,jW0xhsc,mqrTRwG,uYI18tX,hlPr9NF,Nw15TgM,byHBsVy,bTh82iD,WFyVjds,' \
                '3rseTyr,xiX8n5g,XrfvU65,9MyoCYJ,ezXqaaS,e6YHcbF,op516qp,2zuqFcR,a2UrrXQ,0PlBQqv,dw0RQ4F,s7IWHuf,m3nQsLC,KBbaxam,GRVaiD0,' \
                'fsghjfgw,5lYmN34,TxhuTgF,3YEHnbf,GOZjZK5,aLiUtev,N70PTSp,NNHeprZ,48ATHnn,cBSdGJu,TShxOF9,Cf6I3KJ,b1KHgXl,77mq0PS,FQPcNe6,' \
                'aGZVZ0U,qqFmHp0,CGPZnxF,v1tzhjA,yr1YPjz,YbThNwj,SSfeLxO,lFd3m1P,NSZk6IG,lLD8e1C,yfnigQa,ZJvrXea,5k3Babp,wxgGPT6,y1aLCC2,' \
                'jN9ErCW,oreXATa,deXcDrJ,wRoPZCh,ViIs17X,kxafqEt,RhWky3b,SYv1mez,a88EiKU,XDX7ILP,C9lrHwd,oFpufxh,hit,WmKoBw5,pcl4swd,PFRKeBX,' \
                'uko7S6t,0frEgor,ZtweyPb,AG0M1BH,jPNrVrz,6s4BcPH,1xfq61n,zl885Xs,4eUJZCM,6uevv4E,uziAHeP,JvhPE01,qXXxOf1,OkogRHM,sXiwH39,xUTKgDY,' \
                'rDUlUej,Uiz7jwM,p5hBQIz,OZ2btGx,rVQHw2n,sr1PvWx,dNmppEO,pkGAbL5,QTgE1Zd,3eewzi5,rierpPs,2Cs10HU,dIk4sUX,jXqnUV7,RaPLMZA,ar02Mdq,' \
                'VWGII72,EBoCA9v,1cWfCpa,roXACvB,g7HlTPP,7c6Gnfk,zQdeFQg,s0PBOZ4,95ULngN,11fe9tU,gdHigMw,KKJOPNW,1laDkhO,AdAadS6,3EAStrY,2tO2p0p,' \
                'oHaDvke,A97arRm,62x0fx2,mSeZf5d,K81uulb,fafklh,ZS8vQ3k,oG36Vnd,iM3LWGU,ueRVY1X,qOUc5AY,fasasd,KlbKnak,nhq3ZBl,09UDMU2,5mgmaUB,' \
                'yRq4RL4,oNZG7cl,c0o6Aad,bI0B3Ax,5Tlitkg,QKh9m4K,Bv6pioE,CTrcEZb,JQ5lou3,aRlHHJ3,QffWCKQ,fhCpYsw,Qdk5NuG,Z8Jq2Wl,aqB8qHm,sDsku6s,' \
                'NfgCwyZ,oEkWVNy,pStPmEw,ByZN5Dw,FQgnySW,XgS6gXG,vInVG29,1ocv3pF,x9MbCdH,cGJ2W75,kIJ0odu,Pqh8Bwk,nfnAFAR,2lXoD6F,qju84n7,J7IS9AZ,' \
                'dMx2CvV,wNfiBjH,brA7kLO,ngZAEm0,iVdZ4aP,9gqupyW,S0Z0FZL,LIR6nlo,J1tGpfb,UEQI0GD,wdRq9XS,7UpbBGp,u1bPq9i,7LTc6bG,8f1HNxB,VCxgJWn,' \
                'XQ10axt,DFnExcb,GKqvWXd,5Fe3B2B,uIAjkn1,g217APS,87TSNFM,dobdqgU,zwMIZJG,XKmrzPj,CvSOlPm,pWBPbO8,EiVJcRE,gBBwCF9,mUJMSRS,wmbKDHd,' \
                'PQUodiR,iheNNjK,XEZ1jwW,NLDzUDs,xtyjcLV,yrzIw5c,MAT3xfQ,pXsLay4,fhfhdghj,gG07IwU,xXfwtDu,We4T8jX,p05Gr7r,bQTVBjn,5vXehdW,tiLAwTH,' \
                '5x2SuJu,b8YPi9j,0vnD5Sn,61oV7m7,oHtxdHO,xTkbDrk,dfVO8eD,yAop0wi,8DvNDkg,Mh7QVzh,tyanuDe,NbODAST,I421CGE,Q3yMcnr,wZFcqTY,UIArQvC,' \
                'I0NvyfC,FEeJqQX,ojcPGGA,sLtvI2H,vUWnZx3,4xRuyAq,AUxEqNA,WEnJuS1,DYDZcwJ,ut4sxK8,7cFP0Nc,Bd0ATDz,Cx52PEE,Qvo0o4x,FM1S9XI,bOqbzlK,' \
                'lChhUWA,eRqqpIX,Iq320RG,TSLppyo,hHH3Zky,thhg,FVxjs4S,ZVzQrOx,GECloVa,GonKNMC,XyHflpk,yaTkUyu,NwxSNkw,Fa4lOSn,eL7JF1T,Sk6I9hs,svdsfvs,' \
                'LT8HeMO,jG4ID3R,6KXwHOB,2RskqE7,HccemMX,PaNx0dM,bEpKUa6,YikwP72,oWMFsWG,D1ycCQW,tlTdone,lD9l5zD,WLDESG6,dw0RQ4F'

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
