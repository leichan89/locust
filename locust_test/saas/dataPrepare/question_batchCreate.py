# -*- coding: utf-8 -*-

import requests
import json
import time
from urllib.parse import quote, urlencode
from common.tools import Tools
from locust import HttpUser, task, between
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告
t = Tools()

class BatchCreate(HttpUser):

    wait_time = between(0.1, 0.2)

    @task(1)
    def batchCreate(self):

        # query参数
        apiparam = {"method": "zhiyong.study.question.question.batchCreate"}

        # body参数
        body = {"questions":[{"categoryId":-1,"type":"0","title":f"<p>测试{str(time.time())}</p>","analysis":"<p>答对</p>","answers":[{"correctStatus":1,"answerContent":"<p>大大大</p>"},{"correctStatus":0,"answerContent":"<p>的</p>"},{"correctStatus":0,"answerContent":"<p>答对</p>"},{"correctStatus":0,"answerContent":"<p>大多数</p>"}]}]}

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
        headers = t.getPCHeaders()
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
    os.system(f"locust -f {file} --host=http://open.stage.zhiyong.highso.com.cn --web-host=127.0.0.1 --web-port=8011")
