import os
import shutil
import re
import numpy as np

origin_folder = "/Users/a333/Movies/一区挂机吸金90个号"
dest_folder = "/Users/a333/Movies/1区挂机吸金"
group_leader = {
    "1": "4338330524",
    "2": "4337709044",
    "3": "4310158459",
    "4": "4337709469",
    "5": "4337709046",
    "6": "4337709047",
    "7": "4338242470",
    "8": "4305050247",
    "9": "4338242474",
    "10": "4312077187"
}
role_map = {
    "1": "2",
    "2": "2",
    "3": "1",
    "4": "2",
    "5": "2",
    "6": "1",
    "7": "2",
    "8": "2",
    "9": "1",
}

all_dir = []
for topfolder in os.listdir(origin_folder):
    if topfolder != ".DS_Store":
        all_dir.append(topfolder)






for item in all_dir:
    sub_folder_param = item.replace("一区", "").replace("组", "-").split("-")
    sub_folder_path = origin_folder + "/" + item
    token_folders = []
    for moniqi in os.listdir(sub_folder_path):
        if moniqi.startswith("模拟器"):
            monitor_index = re.findall("\d+", moniqi)[0]
            group_index = int(sub_folder_param[0])
            role_group = "_".join([role_map[sub_folder_param[0]], group_leader[monitor_index]]) + ".txt"
            token_xml = sub_folder_path + "/模拟器" + monitor_index
            role_leader_txt = token_xml + "/" + role_group
            if not os.path.exists(role_leader_txt):
                fp = open(role_leader_txt, "w")
                fp.close()
            new_folder_name = (group_index - 1) * 10 + int(monitor_index)
            # new_folder_name=( int(monitor_index)-1)*10+ group_index-1
            dest_folder_fix = dest_folder + "/模拟器" + str(new_folder_name)
            print(token_xml, dest_folder_fix)
            shutil.copytree(token_xml, dest_folder_fix)


