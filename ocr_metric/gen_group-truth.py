#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 1:18
# @Author  : 大螃蟹
# @Site    : 
# @File    : gen_group-truth.py
# @Software: PyCharm
'''
生成gp标准文件
'''
import pickle
import os
import json
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


def flace(points):
    res = []
    for point in points:
        res += point.copy()
    return res

def get_label(file_path):

    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        json_val = json.load(file)
        for item in json_val['shapes']:
            label = item['label'].split('^')
            loc = item['points']
            line = ['word'] + flace(loc)
            lines.append(line)
    return lines



if __name__ == '__main__':
    json_path = './pre/jsons/'
    json_names = os.listdir(json_path)
    for json_name in json_names:
        print(json_name)
        if json_name != '200.json':
            continue
        file_name = json_path+json_name

        lines = get_label(file_name)
        txt_name = './ground-truth/'+json_name.replace('.json', '.txt')
        to_txt(txt_name, lines)
''''

200 406 914 有问题
'''