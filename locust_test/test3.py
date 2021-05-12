# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 下午2:54
# @Author  : OG·chen
# @File    : test3.py


def test(*args, **kwargs):
    for i in args:
        print(i)
    print(kwargs)


a = [1, 2, 3, 4]
b = {"aa": "aa", "nb": "aa"}

test(*a, **b)



mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
def fun(x):
    return x*x
#注意使用了list转换类型
maplist = list(map(fun,mylist))
print('map的使用',maplist,'\n','-'*30)
