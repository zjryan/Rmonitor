import subprocess
import time


class Monitor(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = (u'\t{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return u'\n<\n{0}:\n  {1}\n>'.format(class_name, '\n    '.join(properties))


class Memory(Monitor):
    def __init__(self, memo_info):
        super(Memory, self).__init__()
        self.total = memo_info['total']
        self.used = memo_info['used']
        self.free = memo_info['free']


class CPU(Monitor):
    def __init__(self, cpu_info):
        super(CPU, self).__init__()
        self.min1 = cpu_info['min1']
        self.min5 = cpu_info['min5']
        self.min15 = cpu_info['min15']


class Disk(Monitor):
    def __init__(self, disk_info):
        super(Disk, self).__init__()
        self.tps = disk_info['tps']
        self.read = disk_info['read']
        self.write = disk_info['write']


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
    m = Memory(memo_info)
    return m


def uptime():
    r = cmd_result('uptime')[0]
    full_info = r.split()
    cpu_info = dict(
        min1=full_info[7],
        min5=full_info[8],
        min15=full_info[9],
    )
    cpu = CPU(cpu_info)
    return cpu


def iostat():
    r = cmd_result('iostat -d')[3]
    full_info = r.split()
    disk_info = dict(
        tps=full_info[1],
        read=full_info[2],
        write=full_info[3]
    )
    d = Disk(disk_info)
    return d


def current_status():
    memory = free()
    disk = iostat()
    cpu = uptime()
    data = dict(
        memory=memory,
        disk=disk,
        cpu=cpu,
    )
    print(data)


def main():
    current_status()


def monitor():
    while True:
        current_status()
        time.sleep(2)


if __name__ == '__main__':
    # main()
    monitor()