import requests
from datetime import datetime as dt
import pprint
import json


def to_sec(date):
    return int(dt.timestamp(dt.strptime(date, "%d.%m.%Y")))


def is_between(date, l, r):
    return l <= date <= r


# Эта
# Нужно правую границу указывать +1 не входящую
def parse(nick, date_info):
    if date_info[0]:
        date_info[1] = to_sec(date_info[1])
        date_info[2] = to_sec(date_info[2])
        print(date_info)
    all_tasks = set()
    complexity = dict()
    all = 0
    all_submissions = json.loads(requests.get(f"https://codeforces.com/api/user.status?handle={nick}").text)["result"]
    for submit in all_submissions:
        if submit["verdict"] == "OK" and not (str(submit["problem"]["contestId"]) + submit["problem"]["index"] in all_tasks):
            try:
                if "rating" in submit["problem"].keys():
                    key = submit["problem"]["rating"]
                else:
                    key = "none rating"
                if date_info[0] and not is_between(submit["creationTimeSeconds"], date_info[1], date_info[2]):
                    continue
                all += 1
                complexity[key] = complexity.get(key, 0) + 1
                all_tasks.add(str(submit["problem"]["contestId"]) + submit["problem"]["index"])
            except Exception as err:
                print(err)

    keys = sorted(complexity.keys(), key=lambda x: x if str(type(x)) == "<class 'int'>" else 0)
    for key in keys:
        print(key, ": ", complexity[key])
    print(complexity)
    print(all)

    return [complexity, all]


if __name__ == "__main__":
    #pprint.pprint(json.loads(requests.get(f"https://codeforces.com/api/user.status?handle=vazy1").text)["result"][0])
    #print(dt.fromtimestamp(1663604531))
    parse("Ilya0412", [1, "06.10.2023", "17.10.2023"])
