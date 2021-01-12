# -*- coding: utf-8 -*-

import requests
import json
import queue
import os
from urllib.parse import quote, urlencode
from common.tools import Tools
from locust import HttpUser, task, between, events
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全警告
t = Tools()

@events.test_start.add_listener
def on_test_start(**kwargs):
    global params, queueData
    workFlowIdCsv = '/Users/chenlei/python-project/mylocust/csv/workFlowId.csv'
    os.remove(workFlowIdCsv)
    for i in range(1000):
        with open(workFlowIdCsv, 'a') as f:
            f.write(str(t.getWorkFLowId())+'\n')
    params1 = t.get_csv_info('paper_questionIds.csv')
    params2 = t.get_csv_info('workFlowId.csv')
    queueData = queue.Queue()

    # 参数放入队列
    for pa1 in params1:
        for pa2 in params2:
            param = {
                "questionId": pa1[0],
                "workFlowId": pa2[0]
            }
            queueData.put_nowait(param)

class QuestionSave(HttpUser):

    wait_time = between(0.1, 0.2)

    @task(1)
    def questionSave(self):
        """
        服务：study-question-log-service
        日志：/data/applogs/study-question-log-service
        做题明细保存，一个试卷存在1000个试题
        可能需要重新获取workFlowId
        当前uid=100000154011
        question_record_detail_(SELECT (100000154011) % 128)
        :return:
        """
        # 从队列获取参数
        csvparam = queueData.get()
        # 将获取的参数再放入队列尾部
        queueData.put(csvparam)

        # query参数
        apiparam = {"method": "zhiyong.study.questionlog.save"}

        # body参数
        body = [
                    {
                        "courseType": "2",
                        "courseId": "300000613411",
                        "businessType": "2",
                        "businessId": "300000613411",
                        "__key_": "161034449175510",
                        "paperId": "300000613411",
                        "paperType": "2",
                        "terminalType": "mp",
                        "answer": [
                            "300000566523"
                        ],
                        "questionId": csvparam['questionId'],
                        "workFlowId": csvparam['workFlowId']
                    }
                ]

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
    os.system(f"locust -f {file} --host=http://open.test.zhiyong.highso.com.cn --web-host=127.0.0.1 --web-port=8001")
