from faker import Faker
from pypinyin import pinyin, lazy_pinyin, Style
import json
import random
import re

with open('adjective.json') as f:
    adjective = json.loads(f.read())

with open('area.json') as f:
    area = json.loads(f.read())

with open('noun.json') as f:
    noun = json.loads(f.read())

with open('cn25w.json') as f:
    cn_names = json.loads(f.read())

with open('r18.json') as f:
    jp_names = json.loads(f.read())

with open('5w.json') as f:
    words4 = json.loads(f.read())

with open('en2w.json') as f:
    en2w = json.loads(f.read())

fake = Faker('en_US')


def gen_suoxie(origin):
    names = pinyin(origin, style=Style.FIRST_LETTER)
    all_str = ''
    for k in names:
        all_str = all_str + k[0]
    return all_str


def gen_name() -> str:
    ntype = random.randrange(0, 14)
    if ntype == 0:
        return random_full_name(adjective) + random_full_name(noun)
    if ntype == 1:
        return random_full_name(en2w) + random_full_name(cn_names)
    if ntype == 3:
        return random_full_name(en2w) + random_full_name(jp_names)[:4]
    if ntype == 4:
        return random_full_name(words4) + random_full_name(noun)
    if ntype == 5:
        return random_full_name(adjective) + random_full_name(jp_names)[:4]
    if ntype == 6:
        return random_full_name(jp_names)[:4] + random_full_name(noun)
    if ntype == 7:
        return random_full_name(words4)
    if ntype == 9:
        return random_full_name(cn_names) + random_full_name(en2w)
    if ntype == 10:
        return random_full_name(jp_names) + random_full_name(en2w)
    if ntype == 11:
        return random_full_name(adjective) + random_full_name(jp_names)[:4]
    if ntype == 12:
        return random_full_name(area) + random_full_name(jp_names)[:4]
    if ntype == 13:
        return random_full_name(area) + random_full_name(cn_names)

    return random_full_name(area) + random_full_name(cn_names)


def random_short_name(names: list):
    return gen_suoxie(names[random.randrange(len(names) - 1)])


def random_full_name(names: list):
    return names[random.randrange(len(names) - 1)]


def gen_account() -> str:
    ntype = random.randrange(0, 14)
    account_str = ""
    if ntype == 0:
        account_str = random_short_name(en2w) + random_short_name(en2w)
    if ntype == 1:
        account_str = random_short_name(cn_names) + f"{fake.pyint(1970, 2010)}" + random_short_name(cn_names)
    if ntype == 3:
        account_str = f"{fake.pyint(1970, 2010)}" + random_short_name(cn_names) + random_short_name(cn_names)
    if ntype == 2:
        account_str = random_full_name(en2w) + f"{fake.pyint(1970, 2010)}"

    if ntype == 4:
        account_str = random_full_name(en2w) + f"{fake.pyint(1, 9999)}"

    if ntype == 5:
        account_str = f"{fake.pyint(1, 9999)}" + random_short_name(jp_names)

    if ntype == 6:
        account_str = random_full_name(en2w) + f"{fake.pyint(1, 9999)}"

    if ntype == 7:
        account_str = random_short_name(words4) + en2w[random.randrange(len(en2w) - 1)]
    if ntype == 8:
        account_str = str(fake.pyint(1311111111, 9999999999))
    if ntype == 9:
        account_str = f"{fake.pyint(1, 9999)}" + random_short_name(adjective)

    if ntype == 10:
        account_str = random_full_name(en2w) + random_short_name(jp_names)

    if ntype == 11:
        account_str = random_full_name(en2w) + random_short_name(cn_names)

    if ntype == 12:
        account_str = random_short_name(area) + random_short_name(jp_names)

    if ntype == 13:
        account_str = random_short_name(area) + random_short_name(cn_names)

    if len(account_str[:20]) < 8:
        account_str = account_str + random_short_name(cn_names)
    return account_str[:16]


phones = [18618618611, 18618618611, 18618618611]
emails = ["qq@sina.com", "qq@qq.com", "qq@foxmail.com", "qq@foxmail.com",
          "qq@qq.com", "qq@qq.com", "qq@qq.com", "qq@qq.com", "qq@outlook.com",
          "qq@qq.com","qq@qq.com"]

profile_info = [
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
    {"realname": "郭启鹏", "realid": "xxxxxxxxxxxxxxxxxx"},
]
index = 0
count = 0


class PtDataGen:
    def __init__(self):
        self.data_dict = {}

    def fake_data(self, seed: int, index: int):
        account = f"{fake.pyint(0000, 9999):04}{fake.name()}".replace(" ", '')
        old_account = "".join(random.sample(account, random.randint(5, 9)))
        self.data_dict['username'] = gen_account()
        password = f"qwe{seed}"
        self.data_dict['password'] = password
        self.data_dict['confirm'] = password
        self.data_dict['gname'] = gen_name()[:8]
        person = random_full_name(profile_info)
        self.data_dict['realname'] = person['realname']
        self.data_dict['realid'] = person['realid']
        self.data_dict['mobile'] = phones[index]
        self.data_dict['email'] = random_full_name(emails)

    def get_data_dict(self):
        return self.data_dict


for i in range(1000, 3000):
    pt_data = PtDataGen()

    if count == 10:
        count = 0
        if index == len(phones) - 1:
            index = 0
        index = index + 1
    count = count + 1
    pt_data.fake_data(i, index)
    print(json.dumps(pt_data.get_data_dict(), ensure_ascii=False))
