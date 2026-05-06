#-*-coding: utf-8 -*-
"""
请利用Python内置的hex()函数把一个整数转换成十六进制表示的字符串：
"""
n1 = 255
n2 = 10000
print(hex(n1))
print(hex(n2))
"""
请定义一个函数quadratic(a, b, c)，接收3个参数，返回一元二次方程 
ax^2+bx+c=0 的两个解。
"""
import math

def quadratic(a,b,c):
    if a == 0:
        print('No solution')
        return

    D = b * b - 4 * a * c

    if D < 0:
        print('No solution')
        return
    elif D == 0:
        x = -b / (2 * a)
        return x, x
    else:
        sqrt_D = math.sqrt(D)
        x1 = -b / (2 * a) + sqrt_D  / (2 * a)
        x2 = -b / (2 * a) - sqrt_D  / (2 * a)
        return x1, x2

print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')






