# 心动网络 仙境传说.守护永恒的爱手游 cdk奖品批量自动领取

### 仙境传说手游二区 - 梦想天空服 [星尘] gvg公会 招人 
##### 猛男会长微信号: yifeiyyt   

## 原始页面
![image](ro_xd_cdk.png)

### 功能如下
1. 验证码自动识别和重试
2. 按角色名单列表全批量领取

## 使用方法 修改 batch_ro_cdk.py  
            安装依赖  Python环境 ≥python3.6
            pip3 install -r requirements.txt

1. 更改新的礼包兑换码 gift_key.py

            GIFT_CODE = '1021LZF4DQY'

2. 更改要领取账号所在的服务器的编号

            server_id = 10001002

            #### 服务器列表
            . 1服-守护永恒的爱 [server_id = 10001]

            . 2服-梦想天空  [server_id = 10001002]

            . 3服-辉煌领域 [server_id =10001003] 


3. 更改 名单列表 （ro 游戏角色名）逗号隔开 


            name_list_str = '浮羽派丁,落羽霏霏,可爱大布丁'

4. 运行脚本 开始批量领取 

            python3 batch_ro_cdk.py  

            运行结果：

            {
                '礼包码兑换成功': ['怪你过分美丽', 'yoyoQ', '还没睡醒', .....], 
                '角色名不存在': ['灌奶小白', '拉拉个大脸', '无心の小圆子',.....]
            }

   




