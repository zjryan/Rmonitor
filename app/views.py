from app import app
from .monitor import status
from flask import render_template
from flask import request
from flask import jsonify
from pymongo import DESCENDING


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/serverstatus', methods=['POST'])
def server_status():
    form = request.get_json()
    data_len = form.get('data_len')
    s = list(status.find().sort("created_time", DESCENDING).limit(data_len))
    cpu_min1 = []
    cpu_min5 = []
    cpu_min15 = []
    for i in range(0, data_len):
        elem = s[i]
        cpu = elem['cpu']
        cpu_min1.append(cpu['min1'])
        cpu_min5.append(cpu['min5'])
        cpu_min15.append(cpu['min15'])

    data = dict(
        cpu_min1=cpu_min1,
        cpu_min5=cpu_min5,
        cpu_min15=cpu_min15,
    )
    r = {
        'success': True,
        'data': data,
    }
    return jsonify(r)