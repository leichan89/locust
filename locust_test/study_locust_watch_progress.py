# -*- coding: utf-8 -*-

import requests
from locust import HttpUser, task, between
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告


class StudyTest(HttpUser):

    wait_time = between(0.0, 0.1)

    @task(1)
    def generate_watch_progress(self):
        # 观看记录汇总数据生成接口
        url="/watchProgress/generateWatchProgress?customerId=12223223&mediaType=1&mediaId=48895"
        with self.client.post(url=url, catch_response=True) as response:
            if response.status_code == 200:
                rst = response.json()
                if rst['code'] == 200:
                    response.success()
                else:
                    response.failure("code不为200")
            else:
                response.failure("status_code不为200")



if __name__ == "__main__":
    import os
    file = __file__
    os.system(f"locust -f {file} --host=http://192.168.16.216:38000 --web-host=127.0.0.1 --web-port=8003")