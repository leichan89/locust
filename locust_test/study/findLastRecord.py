# -*- coding: utf-8 -*-

import requests
import queue
import copy
from common.tools import Tools
from locust import HttpUser, task, between, events
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告


@events.test_start.add_listener
def on_test_start(**kwargs):
    global params, queueData
    params = Tools().get_csv_info('recordTop1000.csv')
    queueData = queue.Queue()

    # 参数放入队列
    for param in params:
        param = {
            "customerId": param[0]
        }
        queueData.put_nowait(param)

class StudyTest(HttpUser):

    wait_time = between(0.0, 0.1)

    @task(1)
    def get_watched_media_count(self):

        # 从队列获取参数
        param = queueData.get()
        # 将获取的参数再放入队列尾部
        queueData.put(param)

        params = {
            "customerId": param['customerId']
        }

        url = "/questionRecordApi/findLastRecord"


        with self.client.post(url=url, params=params, catch_response=True) as response:
            print(response.json())
            if response.status_code == 200:
                rst = response.json()
                if rst:
                    try:
                        if str(rst['customerId']) == params['customerId']:
                            response.success()
                        else:
                            response.failure("返回结果中customerId错误")
                    except:
                        response.failure("返回结果中无customerId")
                else:
                    response.failure("返回结果为空")
            else:
                response.failure("status_code不为200")



if __name__ == "__main__":
    import os
    file = __file__
    os.system(f"locust -f {file} --host=http://192.168.16.216:33000 --web-host=127.0.0.1 --web-port=8002")
    # 阶梯式加压
    # os.system(f"locust -f {file} --host=http://192.168.16.216:38000 --web-host=127.0.0.1 --web-port=8002 --step-load")
