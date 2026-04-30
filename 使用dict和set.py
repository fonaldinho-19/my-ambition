#-*-coding: UTF-8 -*-

d = {'Michal':95,'Bob':75,'Tracy':85}
print(d['Michal'])
d['Adam'] = 67
print(d['Adam'])
d.pop('Bob')
print(d)

s1 = {1,2,3}
s2 = {2,3,4}
print(s1 & s2)
print(s1 | s2)

"""
tuple虽然是不变对象，
但试试把(1, 2, 3)和(1, [2, 3])放入dict或set中，并解释结果。

s = {(1,2,3),(1,[2,3])}
print(s)
'''
结果是TypeError
因为set中第二个元素内含有列表，属于可变对象，不可哈希
"""

