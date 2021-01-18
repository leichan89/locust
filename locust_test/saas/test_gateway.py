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


        ct = t.returnCurrTime()
        d = {"version": "1.0", "appKey": "studyadmin", "timestamp": quote(ct)}
        # query参数
        apiparam = {"method": "zhiyong.study.questionlog.workflowid"}
        param = dict(apiparam, **d)
        sign = t.returnSign("123456", param)
        # 签名后拼接参数
        param['timestamp'] = ct
        param['sign'] = sign
        param['tenantId'] = 1100
        headers = {"Cookie": "gr_user_id=1086bb05-4482-4bfa-9314-ac0ca28aa1b8; grwng_uid=caa7ea03-63fb-4ce8-94cc-dda2b715b47f; t_rtu=bQDWH/fuK39gS9h+UNiN7rHT4qdDEp6AkHNXiK1+nDPN0GmuNpcjRm1vWh+45nAz+FobhAIFASZy7QWeJlDE8/LNQ9Puw1mAHDXUcVH0Lz/0CTc+1lgHrjDkkjb1T548hVBk+bZE/YRyiPeZcsp3wFU7sMS2uMkQLkJpmdgifA2QBlNqfomfsnbtjTngV9r7zNtE++3dOedhRAwOtdX+fXPxYTtJne1+3BLyhU4fthw=; _uid=aSFbHlUvAQTAimF2; t_tenant=o5t4RbXHAnt3f3LK5bYBtQ==; t_session=nyzeM+y+FMfGdBtrrvYO1vA9H1DKaVyf+APpshAN2CE0x0yGPDdtaVEWO5E16LuqwFcU7IG23rsLamYYk9f1PiDcVowijCNJEADrHBuaxKkYFNFmqXoftqfAXb2k81Jc6m7UMFof8HTVSPkkUY+UYFd7TppfgUV6/W70+US2DKRni3kH5q8shg9L+Wi+LY6/Gu+Ri/vEU2DVbFlqC1o+cA==; SESSION=MDMxYmIyMTktMjNlOS00ZTkzLWI1MGUtM2VkZGFjNmY0MjBi",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        url = "/router/rest?" + urlencode(param)

        with self.client.get(url=url, headers=headers, catch_response=True) as response:
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
