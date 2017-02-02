import json
import os
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

devices = {}

@app.route('/devices', methods=['GET'])
def get_devices():
    all_devices = { "devices" : devices.values()}
    resp = make_response(json.dumps(all_devices), 200)
    return resp

@app.route('/devices', methods=['POST'])
def create_device():

    device_id = ""
    device_data = {}

    if request.mimetype == 'application/x-www-form-urlencoded':
        device_data = request.form
    elif request.mimetype == 'application/json':
        device_data = json.loads(request.data)

    if 'device-id' not in device_data.keys():
        resp = make_response('missing device-id', 400)
        return resp
    device_id = device_data['device-id']

    if request.method == 'POST':
        if device_id in devices.keys():
            resp = make_response('device already registered', 400)
            return resp;

    devices[device_id] = device_data
    return make_response('ok', 201)


@app.route('/devices/<deviceid>', methods=['GET', 'DELETE'])
def get_device(deviceid):
    global devices
    resp = make_response('ok', 200)
    # Device must be already registered
    if deviceid not in devices.keys():
        resp = make_response('not found', 404)
        return resp;

    if request.method == 'GET':
        resp = make_response(json.dumps(devices[deviceid]), 200)
    elif request.method == 'DELETE':
        # Remove from devices map
        devices = { key:devices[key] for key in devices if key != deviceid }
        # Remove icon
        if os.path.isfile('./icons/{}.svg'.format(deviceid)):
            os.remove('./icons/{}.svg'.format(deviceid))
    return resp


@app.route('/devices/<deviceid>', methods=['PUT'])
def update_device(deviceid):
    resp = make_response('ok', 200)
    # Device must be already registered
    if deviceid not in devices.keys():
        resp = make_response('not found', 404)
        return resp;

    if request.mimetype == 'application/x-www-form-urlencoded':
        device_data = request.form
    elif request.mimetype == 'application/json':
        device_data = json.loads(request.data)

    devices[deviceid] = device_data
    return make_response('ok', 200)

if __name__ == '__main__':
    app.run()
