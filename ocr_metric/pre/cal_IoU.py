#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 12:26
# @Author  : 大螃蟹
# @Site    : 
# @File    : cal_IoU.py
# @Software: PyCharm

'''
计算IoU
'''

import numpy as np
import shapely
from shapely.geometry import Polygon, MultiPoint  # 多边形


# 转换坐标  左上  右上  右下  左下  =》  左上 左下  右下 右上
# def rotate(line1, line2):
#     new_line1 = [line1[0], line1[1], line1[6], line1[7], line1[4], line1[5], line1[2], line1[3]]
#     new_line2 = [line2[0], line2[1], line2[6], line2[7], line2[4], line2[5], line2[2], line2[3]]
#     return new_line1, new_line2

# pre, gt
def cal_iou(line1, line2):

    # line1, line2 = rotate(line1,line2)
    # line1 = [0, 3, 0, 1, 2, 1, 2, 3]  # 四边形四个点坐标的一维数组表示，[x,y,x,y....]
    a = np.array(line1).reshape(4, 2)  # 四边形二维坐标表示
    poly1 = Polygon(a).convex_hull  # python四边形对象，会自动计算四个点，最后四个点顺序为：左上 左下  右下 右上 左上
    # print(Polygon(a).convex_hull)  # 可以打印看看是不是这样子
    # print(poly1.area)

    # line2 = [1, 2, 1, 0, 3, 0, 3, 2]
    b = np.array(line2).reshape(4, 2)
    poly2 = Polygon(b).convex_hull
    # print(Polygon(b).convex_hull)
    # print(poly2.area)
    union_poly = np.concatenate((a, b))  # 合并两个box坐标，变为8*2
    # print(union_poly)
    # print(MultiPoint(union_poly).convex_hull)  # 包含两四边形最小的多边形点
    if not poly1.intersects(poly2):  # 如果两四边形不相交
        iou = 0
        return iou
    else:
        try:
            inter_area = poly1.intersection(poly2).area  # 相交面积
            # print(inter_area)
            # 计算两个四边形面积和
            sum_area = poly1.area + poly2.area
            union_area = sum_area - inter_area
            # union_area = poly1.area + poly2.area - inter_area
            # union_area = MultiPoint(union_poly).convex_hull.area

            # print(union_area)
            if union_area == 0:
                iou = 0
            # iou = float(inter_area) / (union_area-inter_area)  # 错了
            iou = float(inter_area) / union_area
            # iou=float(inter_area) /(poly1.area+poly2.area-inter_area)
            # 源码中给出了两种IOU计算方式，第一种计算的是: 交集部分/包含两个四边形最小多边形的面积
            # 第二种： 交集 / 并集（常见矩形框IOU计算方式）
        except shapely.geos.TopologicalError:
            print('shapely.geos.TopologicalError occured, iou set to 0')
            iou = 0
    return iou

'''
iot = inter area / true area 
'''
# pre, gt
def cal_iot(line1, line2):
    a = np.array(line1).reshape(4, 2)  # 四边形二维坐标表示
    poly1 = Polygon(a).convex_hull  # python四边形对象，会自动计算四个点，最后四个点顺序为：左上 左下  右下 右上 左上

    b = np.array(line2).reshape(4, 2)
    poly2 = Polygon(b).convex_hull
    union_poly = np.concatenate((a, b))  # 合并两个box坐标，变为8*2
    if not poly1.intersects(poly2):  # 如果两四边形不相交
        iou = 0
        return iou
    else:
        inter_area = poly1.intersection(poly2).area  # 相交面积
        # print(inter_area)
        # 计算两个四边形面积和

        # iou = float(inter_area) / (union_area-inter_area)  # 错了
        iot = float(inter_area) / poly2.area
    return iot


def cal_iop(line1, line2):
    a = np.array(line1).reshape(4, 2)  # 四边形二维坐标表示
    poly1 = Polygon(a).convex_hull  # python四边形对象，会自动计算四个点，最后四个点顺序为：左上 左下  右下 右上 左上

    b = np.array(line2).reshape(4, 2)
    poly2 = Polygon(b).convex_hull
    union_poly = np.concatenate((a, b))  # 合并两个box坐标，变为8*2
    if not poly1.intersects(poly2):  # 如果两四边形不相交
        iou = 0
        return iou
    else:
        inter_area = poly1.intersection(poly2).area  # 相交面积
        # print(inter_area)
        # 计算两个四边形面积和

        # iou = float(inter_area) / (union_area-inter_area)  # 错了
        iop = float(inter_area) / poly1.area
    return iop

