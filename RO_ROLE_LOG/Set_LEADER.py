import requests
from loguru import logger

leader_map = {"1": ["4313475916", "4331520664", "4310574162", "4316925492", "4315153083", "4294994609"],
              "2": ["4318370055", "4317796149", "4326432449", "4328534815", "4337670644", "4317740980"],
              "3": ["4337232442", "4335998224", "4337232391", "4336005482", "4336010970", "4336011788"],
              "4": ["4338384728", "4338362843", "4338380529", "4338465066", "4338380528", "4338361467"]

              }

for key, val in leader_map.items():
    for leader_id in val:
        if len(leader_id) == 0:
            continue
        remove_url = f"http://0.0.0.0:5007/area_group/delete/{key}/{leader_id}"
        res = requests.get(remove_url)
        logger.info("{}   {}", remove_url, res.json())
        set_leader_url = f"http://0.0.0.0:5007/area_group/set/{key}/{leader_id}"
        res = requests.get(set_leader_url)
        logger.info("{}   {}", set_leader_url, res.json())
