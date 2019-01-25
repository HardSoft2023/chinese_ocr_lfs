#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 1:18
# @Author  : 大螃蟹
# @Site    : 
# @File    : gen_predicted.py
# @Software: PyCharm

'''
生成predict标准文件
'''
import pickle
import os

# a = pickle.load(open("./pkl_result/2.jpeg.pkl",  "rb"),  encoding='iso-8859-1')
#
# # train = pickle.load(open("2.jpeg.pkl", 'rb'))
# print(a)

def to_txt(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            for i in range(len(line)-1):
                c = str(line[i])+' '
                f.write(c)
            f.write(str(line[-1]))
            f.write('\n')
    f.close()


def get_label(file_name):
    res = []
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        scale = float(lines[-1].split()[0])  # 放缩比
        for i in range(len(lines)-1):
            line = lines[i].split()
            confidence = float(line[-1])
            tmp_list = ['word', confidence]
            locs = list(map(int, line[:8].copy()))

            for num in locs:
                tmp_list.append(int(num/scale))  # 将坐标放大
            res.append(tmp_list)
    return res, scale


if __name__ == '__main__':
    pre_path = './pre/txt/'
    pre_names = os.listdir(pre_path)
    for pre in pre_names:
        print(pre)
        # if '31' not in pre:
        #     continue
        file_name = pre_path+pre
        # tmp = pickle.load(open(file_name, "rb"), encoding='iso-8859-1')

        lines, scale = get_label(file_name)
        #
        txt_name = './predicted/'+pre.replace('.jpeg', '').replace('.jpg','')
        to_txt(txt_name, lines)
