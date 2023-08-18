import requests
from selenium import  webdriver 
import time
get_codeUrl="http://61.171.28.103:9763/sms/get"

get_ro_bind="http://61.171.28.103:5007/data/get_unbind"
set_bind="http://61.171.28.103:5007/data/bind"
xd_account_url="https://api-sdk.xd.com/v1/user/get_login_url?access_token="
redirect_url="&redirect=https%3A%2F%2Fwww.xd.com%2Fsecurity%2F"
mobile_veryfy="https://www.xd.com/mobile_verify/"
phone_num=""
pwd=""
def get_unbind():
    res=requests.get(get_ro_bind)
    token=""
    data=res.json()
    if data["code"]==0:
        token=data["role"]["token"]
    return token



def get_open_url(token_str):
    res=requests.get(xd_account_url+token_str)
    data=res.json()
    print(data)
    return data["login_url"]+redirect_url



def get_val_code():
    code=""
    times=0
    while True:
        res=requests.get(get_codeUrl)
        data=res.json()
        code=data["code"]
        if len(code)==6:
            break
        times=times+1
        print(f"等待验证码{times}")
        time.sleep(10)
    return code



token_str=""
print(token_str)
if token_str=="":
    print("未找到需要绑定的账号")
    exit(0)

login_url=get_open_url(token_str)
print(login_url)
if login_url=="":
    print("获取url 为空")
    exit(0)





driver = webdriver.Chrome() 
driver.get(login_url)
time.sleep(10)
driver.get(mobile_veryfy)
time.sleep(10)

phone_num_input = driver.find_element_by_id('phone_num')
phone_num_input.send_keys(phone_num)
time.sleep(3)



pwd_input = driver.find_element_by_id('pwd')
pwd_input.send_keys(pwd)
time.sleep(3)


driver.find_element_by_id("获取验证码").click()
time.sleep(3)
code=get_val_code()

code_input = driver.find_element_by_id('验证码')
code_input.send_keys(code)
driver.close()