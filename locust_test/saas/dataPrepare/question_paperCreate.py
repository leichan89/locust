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

class PaperCreate(HttpUser):

    wait_time = between(0.1, 0.2)

    @task(1)
    def paperCreate(self):

        # query参数
        apiparam = {"method": "zhiyong.study.question.paper.create"}

        # body参数
        # test环境
        # body = {"categoryId":-1,"title":f"测试{str(time.time())}","suggestAnswerTime":10800,"paperCatalogs":[{"catalogTypeId":0,"questionCount":1,"score":0,"scoreRule":0,"paperCatalogQuestions":[{"createdByName":"陈磊","updatedBy":100000097003,"questionId":300000148432,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-04T08:30:22.000+0000","type":0,"title":"<p>测试1609749021.3578959</p>","createdDate":"2021-01-04T08:30:22.000+0000","sourceType":0,"createdBy":100000097003,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":300000148432,"sortId":1,"score":10},{"createdByName":"陈磊","updatedBy":100000097003,"questionId":300000148437,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-04T08:30:22.000+0000","type":0,"title":"<p>测试1609749021.356732</p>","createdDate":"2021-01-04T08:30:22.000+0000","sourceType":0,"createdBy":100000097003,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":300000148437,"sortId":2,"score":10},{"createdByName":"陈磊","updatedBy":100000097003,"questionId":300000148452,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-04T08:30:22.000+0000","type":0,"title":"<p>测试1609749021.31872</p>","createdDate":"2021-01-04T08:30:22.000+0000","sourceType":0,"createdBy":100000097003,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":300000148452,"sortId":3,"score":10},{"createdByName":"陈磊","updatedBy":100000097003,"questionId":300000148457,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-04T08:30:22.000+0000","type":0,"title":"<p>测试1609749021.292222</p>","createdDate":"2021-01-04T08:30:22.000+0000","sourceType":0,"createdBy":100000097003,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":300000148457,"sortId":4,"score":10},{"createdByName":"陈磊","updatedBy":100000097003,"questionId":300000148458,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-04T08:30:22.000+0000","type":0,"title":"<p>测试1609749021.2721238</p>","createdDate":"2021-01-04T08:30:22.000+0000","sourceType":0,"createdBy":100000097003,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":300000148458,"sortId":5,"score":10}],"key":0,"sortId":1,"typeName":"单项选择题","ruleName":"按题计分，作错不得分"}]}
        # stage环境
        body = {"categoryId":-1,"title":"测试","suggestAnswerTime":10800,"paperCatalogs":[{"catalogTypeId":0,"questionCount":1,"score":0,"scoreRule":0,"paperCatalogQuestions":[{"createdByName":"陈磊","updatedBy":100000002004,"questionId":100000009151,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-08T03:19:35.000+0000","type":0,"title":"<p>测试1610075974.821481</p>","createdDate":"2021-01-08T03:19:35.000+0000","sourceType":0,"createdBy":100000002004,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":100000009151,"sortId":1,"score":10},{"createdByName":"陈磊","updatedBy":100000002004,"questionId":100000009146,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-08T03:19:35.000+0000","type":0,"title":"<p>测试1610075974.805038</p>","createdDate":"2021-01-08T03:19:35.000+0000","sourceType":0,"createdBy":100000002004,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":100000009146,"sortId":2,"score":10},{"createdByName":"陈磊","updatedBy":100000002004,"questionId":100000009137,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-08T03:19:35.000+0000","type":0,"title":"<p>测试1610075974.7898612</p>","createdDate":"2021-01-08T03:19:35.000+0000","sourceType":0,"createdBy":100000002004,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":100000009137,"sortId":3,"score":10},{"createdByName":"陈磊","updatedBy":100000002004,"questionId":100000009136,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-08T03:19:35.000+0000","type":0,"title":"<p>测试1610075974.788796</p>","createdDate":"2021-01-08T03:19:35.000+0000","sourceType":0,"createdBy":100000002004,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":100000009136,"sortId":4,"score":10},{"createdByName":"陈磊","updatedBy":100000002004,"questionId":100000009131,"updatedByName":"陈磊","subQuestions":None,"updatedDate":"2021-01-08T03:19:35.000+0000","type":0,"title":"<p>测试1610075974.791998</p>","createdDate":"2021-01-08T03:19:35.000+0000","sourceType":0,"createdBy":100000002004,"referenceCount":None,"class":"com.zhiyong.study.question.facade.response.paper.PaperSearchQuestionResp","selected":False,"categoryId":-1,"key":100000009131,"sortId":5,"score":10}],"key":0,"sortId":1,"typeName":"单项选择题","ruleName":"按题计分，作错不得分"}]}

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
    os.system(f"locust -f {file} --host=http://open.stage.zhiyong.highso.com.cn --web-host=127.0.0.1 --web-port=8012")
