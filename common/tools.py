# -*- coding: utf-8 -*-

import csv
import os
import datetime
import time
import hmac
import hashlib

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
        cookie = "_alc=Q8XUBdcIYILRF63xoMzMi98Uje7jc24sMxHB6RV3CIlkwYMdBlJQ85xg1x09aMD7;_t=Zhd0bo9bXkcOlYMTR76Q3EksjNJp6i6F;t_session=ia/lm4k2RkdasgOOB8m3ZAmpOGyvAQdUT5dOtS+3hzLfTZxKoRHkFR8n1oLjgD1Ac5Klje0VBF5Ia9f8nLf7JTc9C6IMkzizjJqfSgYMJjBWYNeQvaXvVIkGxh1Fm3AeEh0ANryTs8RMuFkBbkgIhMtYXenijoX4v6PLa0lxv04/Y9e6NgCjTLJuBBL1TPFYGu+Ri/vEU2DVbFlqC1o+cA==;t_rtu=BC5txJyKzEid2qwUcWyieapBYG+WXrfXPGVi/fcxxn5zr4sSCU3Xt2U4K9r3d9LRy/2VXlppFe8RHp/4sQnP3tzucfUkvGoaOV+2dAQfEFxwRVt3hopIWcI9dPPd62qEQa90TKpkwT/p6CVt3LjdBp64Hz5TmNaYYnbCXjS1BTcDsM9dXFwxPFhXhqPB136wuqy0TL6UmPnWORnGUSOKIv1sD40mH0K90DSx/U5ODvw=;_uid=8dPKXz9bxRsnJHkw;t_tenant=StKWrkhNHpjJ4TgcYS+trg=="
        agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.03.2011120 MicroMessenger/7.0.4 Language/zh_CN webview/"
        return {"cookie": cookie, "User-Agent": agent, "content-type": "application/json"}

    def getPCHeaders(self):
        cookie = "gr_user_id=1086bb05-4482-4bfa-9314-ac0ca28aa1b8; grwng_uid=caa7ea03-63fb-4ce8-94cc-dda2b715b47f; t_session=udWDzubD9Z/rzmh0qBDh1IraulZeXjXylqYYQgEGWZ1Od15VQ+N54+lp/SPlN6hs4Z80/vIvedTuAeZ8znxj2qR5ZpmJ6mHjK2wWdns2a0xQWLKiMBLmQctDaWKZ05fdrGOISDBx/od79c9CC++4M3x/epySFcUuCTmTol5O4VAIZoJRdyMx1pDCQRrXIjG7Gu+Ri/vEU2DVbFlqC1o+cA==; t_rtu=bjFrrsa4lDErZ9Xzk8UwHaD8jxw+Go9InYycebDUrMbOoFyiz3dBpGQx3FmplecClE/KepVs8nKeaG543I3/BLI3VLvGJF6QY4o59wrYbJblgs9AQazVMAmOB8lqHLWC0GEv2N4B8qKQsRsJ1lit2tT0ZSNKp7GivznnPA6IWYG+hGKwrxib/jIb42VRyd0Ur8bGKr3Qm1Q5Bnqr5XRjzR1IZ+i2JfNVDAB/npHgmFk=; _uid=btaICeoVAjtRd9n1; t_tenant=Nkde3avgJd2BJ6L7o7rtAg==; SESSION=NzJmNTExZGQtYWJmOC00ZjY4LThlZDAtZTI1MGE4MTcxOWUw"
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

if __name__ == "__main__":

    t = Tools()
    s = t.get_csv_info('recordDetailTop1000.csv')
    print(s)
