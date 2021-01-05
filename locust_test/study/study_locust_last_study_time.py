# -*- coding: utf-8 -*-

import requests
import queue
from locust import HttpUser, task, between, events
from common.tools import Tools
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告


@events.test_start.add_listener
def on_test_start(**kwargs):
    global params, queueData
    params = Tools().get_csv_info('customergoods_split.csv')
    queueData = queue.Queue()

    # 参数放入队列
    for param in params:
        param = {
            "customerId": param[0],
            "gd1": param[1],
            "gd2": param[2],
            "gd3": param[3],
            "gd4": param[4],
            "gd5": param[5]
        }
        queueData.put_nowait(param)

class StudyTest(HttpUser):

    wait_time = between(0.0, 0.1)

    @task
    def get_last_study_time(self):

        # 从队列获取参数
        param = queueData.get()
        # 将获取的参数再放入队列尾部
        queueData.put(param)

        # 查询观看进度达到指定值的资源数
        # 最近一次学习时间:端口32600
        params = {
            "customerId": param['customerId'],
            "goodsIds": f"{param['gd1']},{param['gd2']},{param['gd3']},{param['gd4']},{param['gd5']}"
        }

        url = "/studyResultService/getLastStudyTime"

        with self.client.post(url=url, params=params, catch_response=True) as response:
            if response.status_code == 200:
                rst = response.json()
                if rst['code'] == 200:
                    response.success()
                else:
                    response.failure("返回的code不为200")
            else:
                response.failure("status_code不为200")


if __name__ == "__main__":
    import os
    file = __file__
    os.system(f"locust -f {file} --host=http://192.168.16.216:14935 --web-host=127.0.0.1 --web-port=8001")
