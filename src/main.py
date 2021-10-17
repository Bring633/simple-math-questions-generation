#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 22:48:32 2021

@author: bring
"""

import numpy as np
from fractions import Fraction
import re

file = r'../data/'
map_ = {0:'+',1:'-',2:'x',3:'/'}


def generate_integer_num(n,high=None):
    """
    输入：n,控制生成题目的个数
        high,最高数值
    
    输出：array格式的三个数据（以整型的形式返回）
    """
    
    if high != None:
        group_b = np.random.randint(0,high,size = (n,3))
    else:
        group_b = np.random.randint(0,10,size =(n,3))
    
    b_index = np.random.randint(0,group_b.shape[0],size = n)

    chosen_b = group_b[b_index,:]
    
    return chosen_b.astype('str')

def generate_float_num(n,high=None):
    """
    输入：n,控制生成题目的个数
        high,最高数值
    
    输出：array格式的三个数据（以浮点型的形式返回）
    """
    group_a = np.random.random((n,3))
    a_index = np.random.randint(0,group_a.shape[0],size = n)
    chosen_a = np.round(group_a[a_index,:],2)
    
    return chosen_a.astype('str')

def generate_operation(n):
    """
    输入：n,控制生成题目的个数
    输出：array格式的两个操作数据
    """
    index = np.random.randint(0,4,size = 2*n).tolist()
 
    return np.array([map_[i] for i in index]).reshape((n,2))

def float_to_frac_and_answer_gen(list_a):
    
    for i in list_a:
        
        pass
    
    return None

def integer_num_answer_gen(list_a):
    
    return None

def combined(data,operation):
    """
    输入：array格式的三列数据和array格式的两列操作
    输出：列表存储的一条题目
    """
    list_data = data.tolist()   
    list_op = operation.tolist()    

    assert len(list_data)==len(list_op)
    
    len_ = len(list_data)
    
    for i in range(len_):
        
        first_op = list_op[i][0]
        second_op = list_op[i][1] 
        
        list_data[i].insert(1,first_op)
        list_data[i].insert(3,second_op)
        
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
            mid_ = float(extract_[0][0])*float(extract_[1][0])
        else:
            if float(extract_[1][0]) == 0:
                flag = 1
                return None,flag
            mid_ = float(extract_[0][0])/float(extract_[1][0])
        
        if op2 == 'x' or op1 == '/':
            
            if op2 == 'x':
                mid_ = mid_*float(extract_[2][0])
            else:
                
                if float(extract_[2][0]) ==0:
                    flag = 1
                    return None,flag
                mid_ = mid_/float(extract_[2][0])
            
        else:
            if op2 == '+':
                mid_ = mid_+float(extract_[2][0]);
            else:
                mid_ = float(mid_)-float(extract_[2][0]);

    elif op2=='x' or op2 == '/':
        
        if op2 == 'x':
            mid_ = float(extract_[1][0])*float(extract_[2][0])
        else:
            if float(extract_[2][0]) ==0:
                flag = 1
                return None,flag
            mid_ = float(extract_[1][0])/float(extract_[2][0])
        
        if op1 == '+':
            mid_ = float(extract_[0][0])+float(mid_);
        else:
            mid_ = float(extract_[0][0])-float(mid_)
    
    else:
        
        if op1 == '+':
            mid_ = float(extract_[0][0])+float(extract_[1][0])
        else:
            mid_ = float(extract_[0][0])-float(extract_[1][0])
        if op2 == '+':
            mid_ = mid_ + float(extract_[2][0])
        else:
            mid_ = mid_ - float(extract_[2][0])
            
    return mid_,flag
        

def generate_answer(list_,float_):
    """
    输入：字符串形式存储的题目列表
    返回：字典存储的题目（key）：答案（values）
    """
    
    pattern = '([0.]*\d*)([\+\-x\/])?'
    
    len_ = len(list_)
    answer_dict = {}
    
    for i in range(len_):
        
        extract_list = re.findall(pattern,list_[i])
        answer,flag = answer_(extract_list[:3]) 
        
        if flag ==1 or answer<0 :
            continue
        
        answer = np.round(answer,3)
        
        if float_:
            
            a = Fraction(extract_list[0][0]).limit_denominator()
            b = Fraction(extract_list[1][0]).limit_denominator()
            c = Fraction(extract_list[1][0]).limit_denominator()
            
            equation = str(a)+extract_list[0][1]+str(b)+extract_list[1][1]+str(c)
  
            answer_dict[equation] = str(Fraction(answer).limit_denominator())

        else:

            answer_dict[list_[i]] = answer
        
    return answer_dict


    
    
    
if __name__ == "__main__":
    
    a = generate_float_num(10)
    b = generate_operation(10)
    c = combined(a,b)
    answer = generate_answer(c,1)





























