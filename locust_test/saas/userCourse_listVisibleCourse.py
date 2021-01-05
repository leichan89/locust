# -*- coding: utf-8 -*-

import requests
import json
import queue
from urllib.parse import quote, urlencode
from common.tools import Tools
from locust import HttpUser, task, between, events
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告
t = Tools()

@events.test_start.add_listener
def on_test_start(**kwargs):
    global params, queueData
    params = Tools().get_csv_info('listVisibleCourse.csv')
    queueData = queue.Queue()

    # 参数放入队列
    for param in params:
        param = {
            "categoryId": param[0]
        }
        queueData.put_nowait(param)

class ListVisibleCourse(HttpUser):

    wait_time = between(0.1, 0.2)

    @task(1)
    def listVisibleCourse(self):

        # 从队列获取参数
        csvparam = queueData.get()
        # 将获取的参数再放入队列尾部
        queueData.put(csvparam)

        # query参数
        apiparam = {"method": "zhiyong.study.userCourse.listVisibleCourse"}

        # body参数
        body = {"currentPage": 1, "pageSize": 20, "categoryId": int(csvparam['categoryId'])}

        # 获取当前时间
        ct = t.returnCurrTime()

        # query基础参数
        data = {"version": "1.0", "appKey": "userCenter", "timestamp": quote(ct)}
        param = dict(apiparam, **data)
        sign = t.returnSign("userCenter8888", param)

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
                    if rst['code'] == 200:
                        response.success()
                    else:
                        response.failure(json.dumps(response.json()).encode('utf-8').decode('unicode_escape'))
                else:
                    response.failure(json.dumps(response.json()).encode('utf-8').decode('unicode_escape'))
            except:
                response.failure("未知错误")



if __name__ == "__main__":
    import os
    file = __file__
    os.system(f"locust -f {file} --host=http://open.test.zhiyong.highso.com.cn --web-host=127.0.0.1 --web-port=8005")
