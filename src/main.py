#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 22:48:32 2021

@author: bring, Maylon
"""

import numpy as np
from fractions import Fraction
import re
import argparse

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
    numerator = np.random.randint(1,high,size = (n,6)).astype('float32')
    denominator = np.random.randint(1,high,size =(n,6)).astype('float32')

    chosen_a = np.round(np.divide(numerator,denominator),2)

    return chosen_a.astype('str')



def generate_operation(n):
    """
    输入：n,控制生成题目的个数
    输出：array格式的两个操作数据
    """
    index = list(np.random.randint(0, 4, size=2 * n))

    return np.array([map_[i] for i in index]).reshape((n, 2))


def format_frac(frac):
    """
    格式化输出真分数

    :param frac: 分数
    :return: 以str类型返回格式化后的真分数(eg. 19/8 => 2'3/8)
    """
    numerator = frac.numerator  # 分子
    denominator = frac.denominator  # 分母
    if numerator > denominator:
        temp = divmod(numerator, denominator)  # 获取商和余数
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
                print("minus")
                flag = 1
                return extract_, None, flag
            mid_ = float(extract_[0][0]) / float(extract_[1][0])

        if op2 == 'x' or op1 == '/':

            if op2 == 'x':
                mid_ = mid_ * float(extract_[2][0])
            else:

                if float(extract_[2][0]) == 0:
                    print("minus")
                    flag = 1
                    return extract_, None, flag
                mid_ = mid_ / float(extract_[2][0])

        else:
            if op2 == '+':
                mid_ = mid_ + float(extract_[2][0])
            else:   # op2 == '-'
                mid_ = float(mid_) - float(extract_[2][0])
                if mid_ < 0:
                    mid_ = -mid_
                    temp = extract_[1][0]
                    extract_[1][0] = extract_[2][0]
                    extract_[2][0] = temp

    elif op2 == 'x' or op2 == '/':

        if op2 == 'x':
            mid_ = float(extract_[1][0]) * float(extract_[2][0])
        else:
            if float(extract_[2][0]) == 0:
                print("minus")
                flag = 1
                return extract_, None, flag
            mid_ = float(extract_[1][0]) / float(extract_[2][0])

        if op1 == '+':
            mid_ = float(extract_[0][0]) + float(mid_)
        else:   # op1 == '-'
            mid_ = float(extract_[0][0]) - float(mid_)
            if mid_ < 0:
                mid_ = -mid_
                temp = extract_[0][0]
                extract_[0][0] = extract_[1][0]
                extract_[1][0] = temp

    else:

        if op1 == '+':
            mid_ = float(extract_[0][0]) + float(extract_[1][0])
        else:
            mid_ = float(extract_[0][0]) - float(extract_[1][0])
            if mid_ < 0:
                mid_ = -mid_
                temp = extract_[0][0]
                extract_[0][0] = extract_[1][0]
                extract_[1][0] = temp
        if op2 == '+':
            mid_ = mid_ + float(extract_[2][0])
        else:
            mid_ = mid_ - float(extract_[2][0])
            if mid_ < 0:
                mid_ = -mid_
                temp = extract_[1][0]
                extract_[1][0] = extract_[2][0]
                extract_[2][0] = temp

    return extract_, mid_, flag


def generate_answer(list_, float_):
    """
    输入：字符串形式存储的题目列表
    返回：字典存储的题目（key）：答案（values）
    """

    pattern = r'([0.]*\d*)([\+\-x\/])?'

    len_ = len(list_)
    answer_dict = {}
    for i in range(len_):

        extract_list = list(re.findall(pattern, list_[i]))
        # 对extract_list进行处理
        temp = []
        for extract in extract_list:
            temp.append(list(extract))
        extract_list = temp
        extract_list, answer, flag = answer_(extract_list[:3])

        if flag == 1 or answer < 0:
            continue

        answer = np.round(answer, 3)

        if float_:

            a = format_frac(Fraction(extract_list[0][0]).limit_denominator())
            b = format_frac(Fraction(extract_list[1][0]).limit_denominator())
            c = format_frac(Fraction(extract_list[2][0]).limit_denominator())

            equation = str(a) \
                       + str('÷' if extract_list[0][1] == '/' else extract_list[0][1]) \
                       + str(b) \
                       + str('÷' if extract_list[1][1] == '/' else extract_list[1][1]) \
                       + str(c)

            answer_dict[equation] = format_frac(Fraction(answer).limit_denominator())

        else:

            a = (extract_list[0][0])
            b = (extract_list[1][0])
            c = (extract_list[2][0])

            equation = str(a) \
                       + str('÷' if extract_list[0][1] == '/' else extract_list[0][1]) \
                       + str(b) \
                       + str('÷' if extract_list[1][1] == '/' else extract_list[1][1]) \
                       + str(c)

            answer_dict[equation] = answer_check(answer)

    return answer_dict


def answer_check(answer):
    """
    判断数据是整数还是小数
    :param answer:
    :return:
    """
    answer_str = str(answer).split('.')  # 转为str类型，获取小数点后的数据
    if float(answer_str[1]) == 0:  # 判断小数点后是否为0
        return str(int(answer))
    else:  # 若是小数则进行真分数格式化
        return format_frac(Fraction(answer).limit_denominator())


def write_result(answer_dict):
    """
    将题目和答案写入txt文件

    :param answer_dict: 生成的题目字典
    :return: None
    """
    # 清空文件
    with open('Exercises.txt', 'w') as f:
        f.truncate()
        f.close()
    with open('Answer.txt', 'w') as f:
        f.truncate()
        f.close()
    # 写入文件
    i = 1
    for key, value in answer_dict.items():
        with open('Exercises.txt', 'a', encoding='utf-8-sig') as f:
            f.write(str(i) + '.' + key + '\n')
            f.close()
        with open('Answer.txt', 'a', encoding='utf-8-sig') as f:
            f.write(str(i) + '.' + value + '\n')
            f.close()
        i += 1


def judge_answer(input_file, answer_file='Answer.txt'):
    """
    统计答案文件的结果

    :param input_file: 用户给定的答案文件
    :param answer_file: 正确答案文件
    :return: None
    """
    # 读取两个文件
    correct_answer = []
    for line in open(answer_file, 'r', encoding='utf8'):
        correct_answer.append(line)
    input_answer = []
    for line in open(input_file, 'r', encoding='utf8'):
        input_answer.append(line)
    # 对答案进行统计
    correct_list = []
    wrong_list = []
    for i in range(len(correct_answer)):
        if correct_answer[i] == input_answer[i]:
            correct_list.append(i + 1)
        else:
            wrong_list.append(i + 1)
    # 将结果写入文件
    with open('Grade.txt', 'w', encoding='utf8') as f:
        f.write('Correct: ' + str(len(correct_list)) + ' ' + str(tuple(correct_list)) + '\n')
        f.write('Wrong: ' + str(len(wrong_list)) + ' ' + str(tuple(wrong_list)))
        f.close()

"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int)  # 生成题目的个数
    parser.add_argument('-r', type=int)  # 题目中数字的范围
    parser.add_argument('-e', type=str)  # 给定题目文件
    parser.add_argument('-a', type=str)  # 给定答案文件
    argv_dict = parser.parse_args().__dict__  # 获取字典
    if argv_dict['e'] is None and argv_dict['a'] is None:  # 生成题目
        if argv_dict['n'] is None:
            raise ValueError("-n参数必须给出，用于控制生成题目的数量")
        if argv_dict['r'] is None:
            raise ValueError("-r参数必须给出，用于控制题目中数值的范围")

        n = argv_dict['n']
        r = argv_dict['r']

        answer_float,answer_integer = generate_questions(n,r)
        len_ = len(answer_integer)+len(answer_float)
         
        while(len_<n):
             
            midval_float,midval_integer = generate_questions(n,r)
            len_midval = len(midval_float)+len(midval_integer)
             
            answer_float = dict(answer_float,**midval_float)
            answer_integer = dict(answer_integer,**midval_integer)

            if len_midval+len_ <= n:             
                continue
            else:
                 
                index_float = np.random.choice(range(len(answer_float)),(n//2,),False)
                index_integer = np.random.choice(range(len(answer_integer)),(n-n//2,),False)
                 
                keys_float = list(answer_float.keys())
                keys_integer = list(answer_integer.keys())
                 
                index_float_mask = [keys_float[i] for i in index_float]
                index_integer_mask = [keys_integer[i] for i in index_integer]
                 
                answer_float = {i:answer_float[i] for i in index_float_mask}
                answer_integer = {i:answer_integer[i] for i in index_integer_mask}
            
            len_ = len(answer_integer)+len(answer_float)
            
        res_dict = {**answer_integer, **answer_float}
        write_result(res_dict)

        print('Completed.')

    elif argv_dict['n'] is None and argv_dict['r'] is None:  # 答案校验
        if argv_dict['e'] is None:
            raise ValueError("-e参数必须给出，表示题目文件")
        if argv_dict['a'] is None:
            raise ValueError("-a参数必须给出，表示答案文件")

        e = argv_dict['e']
        a = argv_dict['a']

        if e != 'Exercises.txt':
            raise FileNotFoundError("找不到文件：" + e)
        judge_answer(a)

        print('Completed.')
    else:
        raise ValueError("参数搭配错误，生成题目使用参数-n -r，答案校验使用参数-e -a")

    # if argv_dict['e'] is not None:
    #     print((argv_dict['e']))
    # if argv_dict['a'] is not None:
    #     print((argv_dict['a']))
"""

def generate_questions(n,r):
    n_float = n // 2
    n_integer = n - n_float

    num_float = generate_float_num(n_float, r)
    num_integer = generate_integer_num(n_integer, r)

    float_op = generate_operation(n_float)
    integer_op = generate_operation(n_integer)

    answer_integer = generate_answer(combined(num_integer, integer_op), 0)
    answer_float = generate_answer(combined(num_float, float_op), 1)
         
    return answer_float,answer_integer
        
    

def main():
     mode = input('please input mode you would like to choose(1 denotes generation, 2 denotes answer check)')

     while mode not in ['2', '1']:
         print("wrong input\n")
         mode = input('please input mode you would like to choose(1 denotes generation, 2 denotes answer check)')

     if mode == '1':
         """
         补充参数部分
         """

         n = 100
         r = 20
         e = None
         a = None

         answer_float,answer_integer = generate_questions(n,r)
         len_ = len(answer_integer)+len(answer_float)
         
         while(len_<n):
             
             midval_float,midval_integer = generate_questions(n,r)
             len_midval = len(midval_float)+len(midval_integer)
             
             answer_float = dict(answer_float,**midval_float)
             answer_integer = dict(answer_integer,**midval_integer)

             if len_midval+len_ <= n:             
                 continue
             else:
                 
                 index_float = np.random.choice(range(len(answer_float)),(n//2,),False)
                 index_integer = np.random.choice(range(len(answer_integer)),(n-n//2,),False)
                 
                 keys_float = list(answer_float.keys())
                 keys_integer = list(answer_integer.keys())
                 
                 index_float_mask = [keys_float[i] for i in index_float]
                 index_integer_mask = [keys_integer[i] for i in index_integer]
                 
                 answer_float = {i:answer_float[i] for i in index_float_mask}
                 answer_integer = {i:answer_integer[i] for i in index_integer_mask}
            
             len_ = len(answer_integer)+len(answer_float)
            
         res_dict = {**answer_integer, **answer_float}
         write_result(res_dict)

     else:
         """
         补充参数部分
         """
         input_file = "Answer.txt"
         judge_answer(input_file)

     print('complete')

     return None


if __name__ == "__main__":
    """
    a = generate_float_num(10)
    b = generate_operation(10)
    c = combined(a, b)
    an = generate_answer(c, 1)
    # print(an)
    write_result(an)

    judge_answer(input_file='Answer.txt')
"""
    main()
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
