from app import app
from .monitor import status
from flask import render_template
from flask import request
from flask import jsonify
from pymongo import DESCENDING


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/status', methods=['POST'])
def server_status():
    form = request.get_json()
    data_len = form.get('data_len')
    s = list(status.find().sort("created_time", DESCENDING).limit(data_len))
    s.reverse()
    cpu_min1 = []
    cpu_min5 = []
    cpu_min15 = []
    disk_tps = []
    disk_read = []
    disk_write = []
    memory_used = []
    for i in range(0, data_len):
        elem = s[i]
        cpu = elem['cpu']
        cpu_min1.append(cpu['min1'])
        cpu_min5.append(cpu['min5'])
        cpu_min15.append(cpu['min15'])
        disk = elem['disk']
        disk_tps.append(disk['tps'])
        disk_read.append(disk['read'])
        disk_write.append(disk['write'])
        memory = elem['memory']
        memo_used_data = int(memory['used']) / 1000 / 1000
        memory_used.append(memo_used_data)
        ct = elem['created_time']

    data = dict(
        cpu_min1=cpu_min1,
        cpu_min5=cpu_min5,
        cpu_min15=cpu_min15,
        disk_tps=disk_tps,
        memory_used=memory_used,
    )
    r = {
        'success': True,
        'data': data,
    }
    return jsonify(r)
