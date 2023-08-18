import os
from pathlib import *
import re

current_folder = os.path.dirname(__file__)
current_folder = str(Path(current_folder, "accounts").absolute())

orginal_file = str(Path(current_folder, "reault.txt06").absolute())


area1_log = str(Path(current_folder, "area0.txt").absolute())
area2_log = str(Path(current_folder, "area1.txt").absolute())
area3_log = str(Path(current_folder, "area2.txt").absolute())
area4_log = str(Path(current_folder, "area3.txt").absolute())

pattern = r"account='(\w+)'"
need_filter_arr=[area1_log,area2_log,area3_log,area4_log]

origin_accounts = set()
with open(orginal_file, "r") as ori_accounts:
    origin_accounts = origin_accounts | set(ori_accounts.readlines())

origin_account_set = set()
for account in origin_accounts:
    name_pwd = account.rstrip('\n').split('|')[0].strip("\n")
    # print(name_pwd)
    origin_account_set.add(name_pwd.strip("\n"))

for log_file in need_filter_arr:
    need_filter_account = set()
    with open(log_file, "r", encoding='utf-8') as area_lines:
        data = area_lines.readlines()
        for item in data:
            match = re.search(pattern, item)
            if match:
                account = match.group(1)
                need_filter_account.add(account)
            else:
                print("Account not found.")
            
    print(f"{log_file} need file_len:{len(need_filter_account)}")


    unused_accounts=origin_account_set-need_filter_account
    


    fixed_unused=set()
    for unused_account in unused_accounts:
        fixed_name=unused_account+"|a123456\n"
        fixed_unused.add(fixed_name)
    need_file= log_file[:-4]+"_need.txt"
    print(need_file)
    with open(need_file,"w") as f:
        f.writelines(fixed_unused)

    print(len(fixed_unused))