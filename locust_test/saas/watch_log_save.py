# -*- coding: utf-8 -*-

import requests
import json
from random import randint
import queue
from urllib.parse import quote, urlencode
from common.tools import Tools
from locust import HttpUser, task, between, events
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告
t = Tools()

"""
使用17318689978账号看的视频，在watch_log_record_0表，customer_id=100000097003
"""

class WatchLogSave(HttpUser):

    wait_time = between(0.1, 0.2)

    @task(1)
    def watchLogSave(self):
        """
        服务：study-watchlog-service
        日志：/data/applogs/study-watchlog-service
        上报观看记录
        当前uid=100000154011
        watch_log_record_(SELECT (100000154011) % 128)
        :return:
        """

        # query参数
        apiparam = {"method": "zhiyong.study.watchlog.save"}

        et = t.getTimeStamp()
        st = t.getTimeStamp(seconds=-100)
        rid = f"5c77bd3519a26c{str(randint(1000000000, 9999999999))}_00"

        # body参数
        body = [
                  {
                    "appId": 100,
                    "channel": 100,
                    "courseId": 100000123006,
                    "coursePackageId": 300000004201,
                    "device": "HUAWEI ELE-AL00",
                    "ep": 100,
                    "et": t.toDate(et),
                    "ip": "192.168.63.98",
                    "mediaId": 300000002808,
                    "mediaItemId": -1,
                    "mediaType": 2,
                    "platform": "android",
                    "resolved1": "",
                    "rid": rid,
                    "sp": 0,
                    "sr": 1,
                    "st": t.toDate(st),
                    "tt": 100,
                    "watchDuration": 100
                  }
                ]
        # 获取当前时间
        ct = t.returnCurrTime()

        # query基础参数
        data = {"version": "1.0", "appKey": "studyadmin", "timestamp": quote(ct)}
        param = dict(apiparam, **data)
        sign = t.returnSign("123456", param)

        # 签名后拼接参数
        param['timestamp'] = ct
        param['sign'] = sign

        # 编码url
        url = "/router/rest?" + urlencode(param)
        headers = t.getMPHeaders()
        with self.client.post(url=url, headers=headers, json=body, catch_response=True) as response:
            try:
                if response.status_code == 200:
                    rst = response.json()
                    # print(rst)
                    if rst['code'] == 200:
                        response.success()
                    else:
                        response.failure(json.dumps(response.json()).encode('utf-8').decode('unicode_escape'))
                else:
                    response.failure(json.dumps(response.json()).encode('utf-8').decode('unicode_escape'))
            except Exception as e:
                print(response)
                print(e)
                response.failure("未知错误")



if __name__ == "__main__":
    import os
    file = __file__
    os.system(f"locust -f {file} --host=http://open.test.zhiyong.highso.com.cn --web-host=127.0.0.1 --web-port=8005")
