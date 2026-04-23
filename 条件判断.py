"""
小明身高1.75，体重80.5kg。
请根据BMI公式（体重除以身高的平方）帮小明计算他的BMI指数，并根据BMI指数：
低于18.5：过轻
18.5-25：正常
25-28：过重
28-32：肥胖
高于32：严重肥胖
用if-elif判断并打印结果：
"""
#-*- coding: utf-8 -*-
M = 80.5
H = 1.75
bmi = M/H**2
if bmi < 18.5:
    print('他的bmi是：%.2f,过轻' %bmi)
elif bmi < 25:
    print('他的bmi是：%.2f,正常' %bmi)
elif bmi < 28:
    print('他的bmi是：%.2f,过重' %bmi)
elif bmi < 32:
    print('他的bmi是：%.2f,肥胖' %bmi)
else:
    print('他的bmi是：%.2f,严重肥胖' %bmi)