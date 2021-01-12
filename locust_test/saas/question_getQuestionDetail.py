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
    params = t.get_csv_info('questionIds.csv')
    queueData = queue.Queue()

    # 参数放入队列
    for param in params:
        param = {
            "questionId": param[0]
        }
        queueData.put_nowait(param)

class GetQuestionDetail(HttpUser):

    wait_time = between(0.1, 0.2)

    @task(1)
    def getQuestionDetail(self):
        """
        服务：study-question-service
        日志：/data/applogs/study-question-service
        查询习题/材料小题详情的信息（5000个试题）
        :return:
        """
        # 从队列获取参数
        csvparam = queueData.get()
        # 将获取的参数再放入队列尾部
        queueData.put(csvparam)

        # query参数
        apiparam = {"method": "zhiyong.study.question.question.detail"}

        # body参数
        body = {"questionId": str(csvparam['questionId'])}

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
    os.system(f"locust -f {file} --host=http://open.test.zhiyong.highso.com.cn --web-host=127.0.0.1 --web-port=9002")
