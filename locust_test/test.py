import hmac
import hashlib
import time
from urllib.parse import quote, urlencode
import sys
import json

def signurl(appKey, appSecret, method, params=None):
    now = int(time.time())
    timeArray = time.localtime(now)
    ct = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    currtime = quote(ct)
    data = {"version": "1.0", "appKey": appKey, "method": method, "timestamp": currtime}
    if params:
        json.loads(params)
        data = dict(data, **params)
    data_list = []
    for key, value in data.items():
        data_list.append(key+value)
    data_list.sort()
    data_string = "".join(data_list)
    h = hmac.new(appSecret.encode('utf-8'), data_string.encode('utf-8'), hashlib.md5).hexdigest()
    data['sign'] = str(h.upper())
    data['timestamp'] = ct
    gate_url = urlencode(data)
    print(gate_url)

if __name__ == "__main__":
    appKey = sys.argv[1]
    appSecret = sys.argv[2]
    method = sys.argv[3]
    try:
        params = sys.argv[4]
    except:
        params = None
    if not params:
        signurl(appKey, appSecret, method)
    else:
        signurl(appKey, appSecret, method, params)
