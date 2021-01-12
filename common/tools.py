# -*- coding: utf-8 -*-

import csv
import os
import datetime
import time
import hmac
import random
from urllib.parse import quote, urlencode
import requests

class Tools:

    def __init__(self):
        self.csv_dirname = os.path.dirname(os.path.dirname(__file__)) + os.sep + 'csv' + os.sep

    def get_csv_info(self, filepath):
        info = []
        file_abs_path = self.csv_dirname + filepath
        if os.path.exists(file_abs_path):
            with open(self.csv_dirname + filepath, 'r') as f:
                reader = csv.reader(f)
                # 逐行读取csv文件
                for i in reader:
                    info.append(i)
            if info:
                return info
            else:
                raise Exception("文件数据为空")
        else:
            raise FileNotFoundError

    def get_timestamp(self, year=None, month=None, day=None, hour=None, minute=None, second=None):
        '''
        默认获取当前时间
        :param year: 年
        :param month: 月
        :param day: 日
        :return: 时间戳
        '''
        mytime = datetime.datetime.now()
        if not year:
            year = mytime.year
        if not month:
            month = mytime.month
        if not day:
            day = mytime.day
        if hour is None:
            hour = mytime.hour
        if minute is None:
            minute = mytime.minute
        if second is None:
            second = mytime.second
        if isinstance(year, int) and isinstance(month, int) and isinstance(day, int) and \
                isinstance(hour, int) and isinstance(minute, int) and isinstance(second, int):
            try:
                mytime = datetime.datetime(year, month, day, hour, minute, second)
                timearray = time.strptime(str(mytime), "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(timearray)) * 1000
                return timestamp
            except:
                errmsg = '转换时间戳异常，请检查参数'
        else:
            errmsg = '年月日必须是整数'
        if errmsg:
            print(errmsg)

    def current_year_zerro_hour(self, month, day):
        return self.get_timestamp(year=2020, month=month, day=day, hour=0, minute=0, second=0)


    def returnSign(self, AppSecret, data):
        data_list = []
        for key, value in data.items():
            data_list.append(key + value)
        data_list.sort()
        data_string = "".join(data_list)
        h = hmac.new(AppSecret.encode('utf-8'), data_string.encode('utf-8'), digestmod="MD5").hexdigest()
        return h.upper()

    def returnCurrTime(self):
        # 获取当前时间
        now = int(time.time())
        timeArray = time.localtime(now)
        ct = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return ct

    def getMPHeaders(self):
        coookiList = []
        cookie1 = {"cookie": "_alc=98f7f72de7076648bbe00d637f79f016939b7bd1988a5fa07df55cf0458120a3;_t=jfU3J0x2eu2S1OWgOaWbeAbVHPXlIOaU;t_session=3birZKpoFdsj74ZfjaR4JuQaGI95PRCnQir4GIOPSKYTnjmm1AodEg06zaSTUj77UTEyF5z9I6ORS7hgXskCdS8CZ7shFVF8PKiZmuwePTccYytlglsniASQAbGcu5nq45EuyxZ/vhI/Z9Ws2J62waR22OvwbJzAhaPk5T/dDVv0TUbag+Wp2JR5Wn4ONK28Gu+Ri/vEU2DVbFlqC1o+cA==;t_rtu=Y08Wvv+XfivohEfj0Agft9V1QIMSya8lls9+mMtQrUBmiqxcnXW9A5nxsM+4eeG8ysnNkASLPvkCqZx71c/eObb8Kg6tIVFlUj6jjs3GbiycuqJGIR89T5WyaYI7Ze6lJ6/vPIxonHAO/SQ0yJwOC7OO9Cht8QyTWCfQ2m/DiZe0koem5zY1HSbrYICAYvG5aV/GLa0qf4JUkXhCBr4HXWCdXWMQhrLk63rftDz/pIo=;_uid=KaUWxLy0pUAA9Uab;t_tenant=YqAwBLI0eJqxh8aw/6v2kQ==",
                   "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.02.1910120 MicroMessenger/7.0.4 Language/zh_CN webview/"}
        cookie2 = {"cookie": "_alc=647dac86112e08aea4bfa081e59f8d481b16d63f01784ec176c0589b7d9efe30;_t=3zWzz32gvhC896ChdlN86eYFfTwV9S9u;t_session=HPVVEDHFB4KrUJJi7GEZEa516cSRq1AHu4ZuR4C7e589yr2tnTDPCUKMYtt3TnKJfR3KrDvTO5s6iPTGCOiKr5Qvx7bzFFgor8ajYk2sNeRSHCV9WCeqqty5v9lQpsTJmqso59E0TI8b2zJJ9oQ3G8WECFRjaayGEibxcirQkcnCp/Rpup1tLJh5qJUInJWMGu+Ri/vEU2DVbFlqC1o+cA==;t_rtu=ukM4HWRUix+11MGD6OkGPsIo3pwTAm26UidUtW7JeS4jCniyS01yWiB4bOixVeLeOZWI/CP543Zkvz53ZzB5S3LzXmEBjSvGq9qp0sZ4s/40x9GFpaDw+KMGz0RfIdifZ9lAU5wQ6HvMR3FTzx3DsCEtR4XVr8MXUgDgbWCG+odjVJMxqsMT3rVzU/XyT1KLVTMzZb/05b3wZ5otvgFeZejypt5mpHp97Lax4fRRaxo=;_uid=6PQugAZq2iHrM1e0;t_tenant=e6+3RVqqHSBH8c5Klv8dww==",
                   "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.03.2012120 MicroMessenger/7.0.4 Language/zh_CN webview/"}
        cookie3 = {"cookie": "_t=Y4uTAaiv7r1RyHefwOlgz2xcjwxIHyH7;_alc=717ec5a679b64ea05c7f9f3fdec1aaf5a277540cfb527357d3ed979580b07a65;_uid=5X5vw42AGhBkYdP7;t_rtu=MsNC4UAF130uiQiUu7nLx/iNfrFXUlALgYHVnh6t6+ZZM5v8R4EtHU5VHiImkRpTS5m9g+1AuDlu/bB8Xo505H7QZB8AsSrEfZiJjgjEmRWJTfbcnmPja+hDpuX++0KxO4qeIlXH+oQWivbpOLidllrq/vOj3wr4Nd11CiFAlGLg/L8U0/CCQZgD1tkz6Mp34/51A8igJuLr2kU1bHNZwRpW4cyCc/cOJygAxEicwUw=;t_session=mXsSK+bLDaRgux31FmJuI/HlTMaI+akx80vEcLSZgJ0R0Gm3l9X/J8RYjXfAT4koCTc5P8A/Q3zpbRmpahnZZ7cZirSCuFwc0WdtNZRoQj9QVjp2S4JZT3KW2wX0hTAg+pGmhXTadx3OANAl4sEzwHKD/pP0HeeeIBK0tQCcYeiOpFLgy/cdCt5Gf+aPcPJAGu+Ri/vEU2DVbFlqC1o+cA==;t_tenant=ML0cGrBFL1zfP+yJHoXY42Li8LGb1gX5rCRn2C+a08Y=",
                   "agent": "Mozilla/5.0 (Linux; Android 9; RVL-AL09 Build/HUAWEIRVL-AL09; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2693 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/3907 MicroMessenger/7.0.22.1820(0x2700163B) Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android"}
        cookie4 = {"cookie": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.03.2011120 MicroMessenger/7.0.4 Language/zh_CN webview/",
                   "agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.03.2011120 MicroMessenger/7.0.4 Language/zh_CN webview/"}
        coookiList.append(cookie1)
        coookiList.append(cookie2)
        coookiList.append(cookie3)
        # coookiList.append(cookie4)
        cookie = random.choice(coookiList)

        return {"cookie": cookie["cookie"], "User-Agent": cookie["agent"], "content-type": "application/json"}

    def getPCHeaders(self):
        cookie = "gr_user_id=1086bb05-4482-4bfa-9314-ac0ca28aa1b8; grwng_uid=caa7ea03-63fb-4ce8-94cc-dda2b715b47f; t_rtu=bQDWH/fuK39gS9h+UNiN7rHT4qdDEp6AkHNXiK1+nDPN0GmuNpcjRm1vWh+45nAz+FobhAIFASZy7QWeJlDE8/LNQ9Puw1mAHDXUcVH0Lz/0CTc+1lgHrjDkkjb1T548hVBk+bZE/YRyiPeZcsp3wFU7sMS2uMkQLkJpmdgifA2QBlNqfomfsnbtjTngV9r7zNtE++3dOedhRAwOtdX+fXPxYTtJne1+3BLyhU4fthw=; _uid=aSFbHlUvAQTAimF2; t_tenant=o5t4RbXHAnt3f3LK5bYBtQ==; SESSION=NjMxMzI2YzgtMjZkOC00MTcwLTkyNWYtYTc5OTJhZjhiZDkz; t_session=nyzeM+y+FMfGdBtrrvYO1vA9H1DKaVyf+APpshAN2CE0x0yGPDdtaVEWO5E16LuqwFcU7IG23rsLamYYk9f1PiDcVowijCNJEADrHBuaxKkYFNFmqXoftqfAXb2k81Jc6m7UMFof8HTVSPkkUY+UYFd7TppfgUV6/W70+US2DKRni3kH5q8shg9L+Wi+LY6/Gu+Ri/vEU2DVbFlqC1o+cA=="
        agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        return {"cookie": cookie, "User-Agent": agent, "content-type": "application/json"}

    def getTimeStamp(self, days=0, hours=0, minutes=0, seconds=0):
        '''
        生成指定日期时间戳，可以是之前的或者之后的日期，默认生成当前日期
        :param days: 天数
        :param hours: 小时
        :param minutes: 分钟
        :param seconds: 秒
        :return:
        '''
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        n_days = now + delta
        timeArray = time.strptime(n_days.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        # 转为时间戳
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def toDate(self, timestamp):
        dateArray = datetime.datetime.utcfromtimestamp(timestamp)
        return dateArray.strftime("%Y-%m-%d %H:%M:%S")

    def getWorkFLowId(self):
        # 获取当前时间
        ct = self.returnCurrTime()
        d = {"version": "1.0", "appKey": "studyadmin", "timestamp": quote(ct)}
        # query参数
        apiparam = {"method": "zhiyong.study.questionlog.workflowid"}
        param = dict(apiparam, **d)
        sign = self.returnSign("123456", param)
        # 签名后拼接参数
        param['timestamp'] = ct
        param['sign'] = sign
        param['tenantId'] = 1100
        headers = {"Cookie": "gr_user_id=1086bb05-4482-4bfa-9314-ac0ca28aa1b8; grwng_uid=caa7ea03-63fb-4ce8-94cc-dda2b715b47f; t_rtu=bQDWH/fuK39gS9h+UNiN7rHT4qdDEp6AkHNXiK1+nDPN0GmuNpcjRm1vWh+45nAz+FobhAIFASZy7QWeJlDE8/LNQ9Puw1mAHDXUcVH0Lz/0CTc+1lgHrjDkkjb1T548hVBk+bZE/YRyiPeZcsp3wFU7sMS2uMkQLkJpmdgifA2QBlNqfomfsnbtjTngV9r7zNtE++3dOedhRAwOtdX+fXPxYTtJne1+3BLyhU4fthw=; _uid=aSFbHlUvAQTAimF2; t_tenant=o5t4RbXHAnt3f3LK5bYBtQ==; t_session=nyzeM+y+FMfGdBtrrvYO1vA9H1DKaVyf+APpshAN2CE0x0yGPDdtaVEWO5E16LuqwFcU7IG23rsLamYYk9f1PiDcVowijCNJEADrHBuaxKkYFNFmqXoftqfAXb2k81Jc6m7UMFof8HTVSPkkUY+UYFd7TppfgUV6/W70+US2DKRni3kH5q8shg9L+Wi+LY6/Gu+Ri/vEU2DVbFlqC1o+cA==; SESSION=MDMxYmIyMTktMjNlOS00ZTkzLWI1MGUtM2VkZGFjNmY0MjBi",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        url = "http://open.test.zhiyong.highso.com.cn/router/rest?" + urlencode(param)
        rst = requests.get(url, headers=headers)
        try:
            return rst.json()['data']
        except:
            raise

if __name__ == "__main__":

    t = Tools()
    for i in range(1000):
        with open('/Users/chenlei/python-project/mylocust/csv/workFlowId.csv', 'a') as f:
            f.write(str(t.getWorkFLowId())+'\n')

