#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Bring, Maylon"

import argparse

if __name__ == '__main__':
    # 获取可选参数：https://www.cnblogs.com/duerbin/p/4193173.html
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int)  # 生成题目的个数
    parser.add_argument('-r', type=int)  # 题目中数字的范围
    parser.add_argument('-e', type=str)  # 给定题目文件
    parser.add_argument('-a', type=str)  # 给定答案文件
    argv_dict = parser.parse_args().__dict__  # 获取字典
    if argv_dict['r'] is not None:
        print(argv_dict['r'])
    if argv_dict['n'] is not None:
        print((argv_dict['n']))
    if argv_dict['e'] is not None:
        print((argv_dict['e']))
    if argv_dict['a'] is not None:
        print((argv_dict['a']))
