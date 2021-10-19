#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 22:48:32 2021

@author: bring, Maylon
"""

import numpy as np
from fractions import Fraction
import re

file = r'../data/'
map_ = {0: '+', 1: '-', 2: 'x', 3: '/'}


def generate_integer_num(n, high=None):
    """
    输入：n,控制生成题目的个数
        high,最高数值

    输出：array格式的三个数据（以整型的形式返回）
    """

    if high is not None:
        group_b = np.random.randint(0, high, size=(n, 3))
    else:
        group_b = np.random.randint(0, 10, size=(n, 3))

    b_index = np.random.randint(0, group_b.shape[0], size=n)

    chosen_b = group_b[b_index, :]

    return chosen_b.astype('str')


def generate_float_num(n, high=None):
    """
    输入：n,控制生成题目的个数
        high,最高数值

    输出：array格式的三个数据（以浮点型的形式返回）
    """
    group_a = np.random.random((n, 3))
    a_index = np.random.randint(0, group_a.shape[0], size=n)
    chosen_a = np.round(group_a[a_index, :], 2)

    return chosen_a.astype('str')


def generate_operation(n):
    """
    输入：n,控制生成题目的个数
    输出：array格式的两个操作数据
    """
    index = list(np.random.randint(0, 4, size=2 * n))

    return np.array([map_[i] for i in index]).reshape((n, 2))


def float_to_frac_and_answer_gen(list_a):
    for i in list_a:
        pass

    return None


def integer_num_answer_gen(list_a):
    return None


def format_frac(frac):
    """
    格式化输出真分数

    :param frac: 分数
    :return: 以str类型返回格式化后的真分数(eg. 19/8 => 2'3/8)
    """
    numerator = frac.numerator  # 分子
    denominator = frac.denominator  # 分母
    if numerator > denominator:
        temp = divmod(numerator, denominator)   # 获取商和余数
        return str(temp[0]) + '’' + str(temp[1]) + '/' + str(denominator)
    elif numerator == denominator:
        return str(1)
    else:
        return str(frac)


def combined(data, operation):
    """
    输入：array格式的三列数据和array格式的两列操作
    输出：列表存储的一条题目
    """
    list_data = data.tolist()
    list_op = operation.tolist()

    assert len(list_data) == len(list_op)

    len_ = len(list_data)

    for i in range(len_):
        first_op = list_op[i][0]
        second_op = list_op[i][1]

        list_data[i].insert(1, first_op)
        list_data[i].insert(3, second_op)

    return [''.join(i) for i in list_data]


def answer_(extract_):
    """
    用于生成一道题目的答案
    """

    flag = 0

    op1 = extract_[0][1]
    op2 = extract_[1][1]

    if op1 == 'x' or op1 == '/':

        if op1 == 'x':
            mid_ = float(extract_[0][0]) * float(extract_[1][0])
        else:
            if float(extract_[1][0]) == 0:
                flag = 1
                return None, flag
            mid_ = float(extract_[0][0]) / float(extract_[1][0])

        if op2 == 'x' or op1 == '/':

            if op2 == 'x':
                mid_ = mid_ * float(extract_[2][0])
            else:

                if float(extract_[2][0]) == 0:
                    flag = 1
                    return None, flag
                mid_ = mid_ / float(extract_[2][0])

        else:
            if op2 == '+':
                mid_ = mid_ + float(extract_[2][0])
            else:
                mid_ = float(mid_) - float(extract_[2][0])

    elif op2 == 'x' or op2 == '/':

        if op2 == 'x':
            mid_ = float(extract_[1][0]) * float(extract_[2][0])
        else:
            if float(extract_[2][0]) == 0:
                flag = 1
                return None, flag
            mid_ = float(extract_[1][0]) / float(extract_[2][0])

        if op1 == '+':
            mid_ = float(extract_[0][0]) + float(mid_)
        else:
            mid_ = float(extract_[0][0]) - float(mid_)

    else:

        if op1 == '+':
            mid_ = float(extract_[0][0]) + float(extract_[1][0])
        else:
            mid_ = float(extract_[0][0]) - float(extract_[1][0])
        if op2 == '+':
            mid_ = mid_ + float(extract_[2][0])
        else:
            mid_ = mid_ - float(extract_[2][0])

    return mid_, flag


def generate_answer(list_, float_):
    """
    输入：字符串形式存储的题目列表
    返回：字典存储的题目（key）：答案（values）
    """

    pattern = r'([0.]*\d*)([\+\-x\/])?'

    len_ = len(list_)
    answer_dict = {}

    for i in range(len_):

        extract_list = re.findall(pattern, list_[i])
        answer, flag = answer_(extract_list[:3])

        if flag == 1 or answer < 0:
            continue

        answer = np.round(answer, 3)

        if float_:

            a = format_frac(Fraction(extract_list[0][0]).limit_denominator())
            b = format_frac(Fraction(extract_list[1][0]).limit_denominator())
            c = format_frac(Fraction(extract_list[2][0]).limit_denominator())

            equation = str(a) \
                       + str('÷' if extract_list[0][1] == '/' else extract_list[0][1]) \
                       + str(b) + str('÷' if extract_list[1][1] == '/' else extract_list[1][1]) \
                       + str(c)
            # equation = str(a) + extract_list[0][1] + str(b) + extract_list[1][1] + str(c)

            answer_dict[equation] = format_frac(Fraction(answer).limit_denominator())

        else:

            answer_dict[list_[i]] = answer

    return answer_dict


if __name__ == "__main__":
    a = generate_float_num(10)
    b = generate_operation(10)
    c = combined(a, b)
    an = generate_answer(c, 1)
    print(an)


# 获取命令行参数
# import argparse
#
# if __name__ == '__main__':
#     # 获取可选参数：https://www.cnblogs.com/duerbin/p/4193173.html
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-n', type=int)  # 生成题目的个数
#     parser.add_argument('-r', type=int)  # 题目中数字的范围
#     parser.add_argument('-e', type=str)  # 给定题目文件
#     parser.add_argument('-a', type=str)  # 给定答案文件
#     argv_dict = parser.parse_args().__dict__  # 获取字典
#     if argv_dict['r'] is not None:
#         print(argv_dict['r'])
#     if argv_dict['n'] is not None:
#         print((argv_dict['n']))
#     if argv_dict['e'] is not None:
#         print((argv_dict['e']))
#     if argv_dict['a'] is not None:
#         print((argv_dict['a']))
