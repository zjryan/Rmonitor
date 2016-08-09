import subprocess
import time
import gevent
from pymongo import MongoClient


# seconds - mongodb 数据库服务器性能数据存在时长 (单位：秒)
STATUS_EXITS_TIME = 60*60


client = MongoClient()
db = client.monitor
# collection
status = db.status


def cmd_result(cmd):
    ret = []
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output_for_line = (line.decode('utf-8') for line in pipe.stdout)
    for o in output_for_line:
        l = '{}'.format(o)
        l = l.replace('\n', '').replace(',', '')
        ret.append(l)
    return ret


def free():
    r = cmd_result('free')[1]
    full_info = r.split()
    memo_info = dict(
        total=full_info[1],
        used=full_info[2],
        free=full_info[3],
    )
    return memo_info


def uptime():
    r = cmd_result('uptime')[0]
    full_info = r.split()
    cpu_info = dict(
        min1=full_info[-3],
        min5=full_info[-2],
        min15=full_info[-1],
    )
    return cpu_info


def iostat():
    r = cmd_result('iostat -d')[3]
    full_info = r.split()
    disk_info = dict(
        tps=full_info[1],
        read=full_info[2],
        write=full_info[3]
    )
    return disk_info


def current_status():
    while True:
        memory = free()
        disk = iostat()
        cpu = uptime()
        data = dict(
            memory=memory,
            disk=disk,
            cpu=cpu,
            created_time=time.time()
        )
        yield data


def save_mongo(data):
    status.insert_one(data)


def remove_outdated_mongo(s):
    while True:
        current_time = time.time()
        limit_time = current_time - s
        status.remove({'created_time': {'$lt': limit_time}})
        gevent.sleep(s)


def monitor():
    gen = current_status()
    while True:
        d = gen.__next__()
        save_mongo(d)
        gevent.sleep(2)


gevent.spawn(monitor)
gevent.spawn(remove_outdated_mongo, STATUS_EXITS_TIME)

