import subprocess


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


def result(cmd):
    ret = []
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output_for_line = (line.decode('utf-8') for line in pipe.stdout)
    for o in output_for_line:
        ret.append('{}'.format(o))
    return ret


def free():
    r = result('free')[1]
    full_info = r.split()
    memo_info = dict(
        total=full_info[1],
        used=full_info[2],
        free=full_info[3],
    )
    m = Memory(memo_info)
    return m


def main():
    free()


if __name__ == '__main__':
    main()
