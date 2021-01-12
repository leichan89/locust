# -*- coding: utf-8 -*-

import requests
import json
from urllib.parse import quote, urlencode
from common.tools import Tools
from locust import HttpUser, task, between
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告
t = Tools()

class MyCourse(HttpUser):

    wait_time = between(0.1, 0.2)

    @task(1)
    def myCourse(self):
        """
        服务： study-course-service
        日志：/data/applog/study-course-service
        前台-列表获取我的课程
        :return:
        """
        # query参数
        apiparam = {"method": "zhiyong.study.userCourse.myCourse"}

        # body参数
        body = {"completedState": 0, "courseType": [0, 2], "pageSize": 10, "currentPage": 1}

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
    os.system(f"locust -f {file} --host=http://open.test.zhiyong.highso.com.cn --web-host=127.0.0.1 --web-port=8004")
