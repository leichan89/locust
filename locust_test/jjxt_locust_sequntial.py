# -*- coding: utf-8 -*-

import requests
import random
from locust import SequentialTaskSet, task, between, events, HttpUser
from urllib3.exceptions import InsecureRequestWarning
import functools
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告


@events.test_start.add_listener
def on_test_start(**kwargs):
    from common.login_jjxt import LoginJJXT
    global cookies
    session = LoginJJXT().get_session()
    cookies = session.cookies


class JJXTTestSeq1(SequentialTaskSet):

    def on_start(self):
        self.client.get = functools.partial(self.client.get, cookies=cookies, catch_response=True, verify=False)
        self.client.post = functools.partial(self.client.post, cookies=cookies, catch_response=True, verify=False)

    @task(1)
    def create_folder(self):
        """
        因为文件数量有20的限制，所以会存在可能某一时间点，文件夹的数量会超过20（同时创建删除时，可能会存在），导致后续接口请求失败
        这种请求只适合，这个实务没有数量限制的情况
        :return:
        """
        name = "my" + str(random.randint(1, 1000))
        params = {"folderName": f"{name}", "clazzId": 11383, "parentId": -1}
        with self.client.post(url="/diligent/folder/create", json=params) as response:
            if response.status_code == 200:
                folderid = response.json()['data']
                if folderid:
                    params = {"clazzId": 11383, "folderIds": [folderid], "folderName": name}
                    with self.client.post(url="/diligent/folder/delete", json=params) as response2:
                        if response2.status_code == 200:
                            rst2 = response2.json()
                            if rst2['code'] == 200:
                                response.success()
                        else:
                            response.failure("删除文件的status_code不为200")
                else:
                    response.failure(f"创建文件夹返回文件夹id失败{response.json()}")
            else:
                response.failure("创建文件status_code不为200")


class JJXTTestSeq2(SequentialTaskSet):

    def on_start(self):
        self.client.get = functools.partial(self.client.get, cookies=cookies, catch_response=True, verify=False)

    @task(1)
    def get_login_user_info(self):
        # 批量登陆
        # 会捕获到异常信息
        with self.client.get(url="/user/loginUser") as response:
            if response.status_code == 200:
                rst = response.json()
                if rst['code'] == 200:
                    response.success()
                else:
                    response.failure(f"返回的code不为200{rst}")
            else:
                response.failure("status_code不为200")


class StartTest(HttpUser):
    wait_time = between(0.5, 1.5)
    tasks = {JJXTTestSeq1: 1, JJXTTestSeq2: 10}



if __name__ == "__main__":
    import os
    from common.configer import MyConfiger
    file = __file__
    host = MyConfiger().getconf().get('env', 'endpoint')
    os.system(f"locust -f {file} --host={host} --web-host=127.0.0.1 --web-port=8000")