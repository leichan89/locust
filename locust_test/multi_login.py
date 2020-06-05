# -*- coding: utf-8 -*-
import functools
import requests
from locust import HttpUser, task, between, events
from urllib3.exceptions import InsecureRequestWarning
from common.tools import Tools
from common.login_jjxt import LoginJJXT
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告


@events.test_start.add_listener
def on_test_start(**kwargs):
    global count, params
    # 计数器，作为csv文件的行号
    count = 0
    params = Tools().get_csv_info('jjxt_user_info.csv')

class LoginTest(HttpUser):

    wait_time = between(0.5, 1)

    def on_start(self):
        global count
        # 如果用户数量超过了cvs中配置的用户数，只会在控制台打印异常，web中不会显示，照样跑
        param = params[count]
        username = param[0]
        passwd = param[1]
        count += 1

        # 登陆获取session，登陆失败cookies也是会有数据的
        session = LoginJJXT(username=username, password=passwd).get_session()
        cookies = session.cookies

        # 为每个用户的get请求固定cookies
        self.client.get = functools.partial(self.client.get, cookies=cookies, verify=False)

    @task(1)
    def get_login_user_info(self):
        # 批量登陆
        # 会捕获到异常信息
        with self.client.get(url="/user/loginUser", catch_response=True) as response:
            if response.status_code == 200:
                rst = response.json()
                if rst['code'] == 200:
                    response.success()
                else:
                    response.failure(f"返回的code不为200{rst}")
            else:
                response.failure("status_code不为200")


if __name__ == "__main__":
    import os
    from common.configer import MyConfiger
    file = __file__
    host = MyConfiger().getconf().get('env', 'endpoint')
    os.system(f"locust -f {file} --host={host} --web-host=127.0.0.1 --web-port=8007")