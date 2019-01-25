#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 16:47
# @Author  : 大螃蟹
# @Site    : 
# @File    : plot_fig.py
# @Software: PyCharm

# 在图片中画出标注框
from PIL import Image
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

from pre.cal_IoU import cal_iou, cal_iot, cal_iop


def draw_boxes(img, boxes, color):
    box_id = 0
    img = img.copy()
    if color == 'r' or color == 'red':
        color = (255, 0, 0)  # red
    elif color == 'g' or color == 'green':
        color = (0, 255, 0)  # green
    else:
        color = (0, 0, 255)
    # text_recs = np.zeros((len(boxes), 8), np.int)
    for box in boxes:
        if np.linalg.norm(box[0] - box[1]) < 5 or np.linalg.norm(box[3] - box[0]) < 5:
            continue



        cv2.line(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
        cv2.line(img, (int(box[0]), int(box[1])), (int(box[4]), int(box[5])), color, 2)
        cv2.line(img, (int(box[6]), int(box[7])), (int(box[2]), int(box[3])), color, 2)
        cv2.line(img, (int(box[4]), int(box[5])), (int(box[6]), int(box[7])), color, 2)

        # for i in range(8):
        #     text_recs[box_id, i] = box[i]
        box_id += 1

    # img = cv2.resize(img, None, None, fx=1.0/0.7, fy=1.0/0.7, interpolation=cv2.INTER_LINEAR)
    return img


if __name__ == '__main__':
    MINOVERLAP = 0.6
    file_id = '1000'
    image_file = './pre/imgs/'+file_id+'.jpeg'
    output_file = './pre/imgs/'+file_id+'_6pnew.jpeg'
    im = Image.open('./pre/imgs/'+file_id+'.jpeg')
    path_pre = './predicted/'+file_id+'.txt'
    path_gt = './ground-truth/'+file_id+'.txt'

    # 绘制标准值 蓝色
    boxes_gt = []
    with open(path_gt) as f:
        content = f.readlines()
    for line in content:
        line = list(map(int, line.split()[1:]))
        # 这里 标准框框需要调整一下坐标位置
        line1 = [line[0],line[1],line[2],line[3],line[6],line[7],line[4],line[5]]
        boxes_gt.append(line1)
    img = np.array(im.convert('RGB'))
    image_gt = draw_boxes(img, boxes_gt, 'b')

    # 绘制预测框中IOU大于阈值 MINOVERLAP 的框
    boxes_right = []
    boxes_wrong = []
    with open(path_pre) as f:
        content = f.readlines()
    for line in content:
        line = list(map(int, line.split()[2:]))
        # 计算IOU
        ovmax = -1
        gt_line = boxes_gt[0]
        # 寻找最大iou 遍历gt_line
        for gt_line in boxes_gt:

            # 如果二者有交集  IoU!=0
            ov = cal_iou(line, gt_line)
            # print(bbpre+bbgt)
            if ov != 0 and ov > ovmax:
                ovmax = ov
                bb_match = gt_line
        if ovmax > MINOVERLAP:
            boxes_right.append(line.copy())

        elif ovmax > 0:
            print(22222222222222222222222)
            io = max(cal_iot(line, bb_match), cal_iop(line, bb_match))
            print(io)
            if io > MINOVERLAP:
                boxes_right.append(line.copy())
            else:
                boxes_wrong.append(line.copy())

        else:
            boxes_wrong.append(line.copy())
    image_pre_right = draw_boxes(image_gt, boxes_right, 'g')
    image_pre_wrong = draw_boxes(image_pre_right, boxes_wrong, 'r')

    Image.fromarray(image_pre_wrong).save(output_file)


