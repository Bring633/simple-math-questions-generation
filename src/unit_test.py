#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon, Bring"

import random
import unittest
import os
import main


class Test(unittest.TestCase):

    # 测试生成10000道题目
    def test1(self):
        os.system('python main.py -n 10000 -r 100')

    # 测试参数异常
    def test2(self):
        os.system('python main.py -n 10000')

    def test3(self):
        os.system('python main.py -r 100')

    def test4(self):
        os.system('python main.py -n 10000 -e Exercises.txt')

    def test5(self):
        os.system('python main.py -n 10000 -r 100 -e Exercises.txt')

    def test6(self):
        os.system('python main.py -n 10000 -r 100 -e Exercises.txt -a change_answer.txt')

    # 测试答案校验
    def test7(self):
        # 读取答案文件存储到列表
        an_list = []
        for line in open('Answer.txt', 'r', encoding='utf-8-sig'):
            an_list.append(line)
        # 改变数据的位置
        pos_list = random.sample(range(1000), 40)
        for pos in pos_list:
            an_list[pos] = an_list[pos] + '0'
        # 转为str类型
        an_str = ""
        for an in an_list:
            an_str += an
        # 写入新文件
        with open('change_answer.txt', 'w', encoding='utf-8-sig') as f:
            f.write(an_str)
            f.close()
        # 答案校验
        os.system('python main.py -e Exercises.txt -a change_answer.txt')


if __name__ == '__main__':
    unittest.main()
