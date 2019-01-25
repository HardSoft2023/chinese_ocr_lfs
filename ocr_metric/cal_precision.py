#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 15:15
# @Author  : 大螃蟹
# @Site    : 
# @File    : cal_precision.py
# @Software: PyCharm

'''
计算OCR算法中检测算法的评价指标
precison = TP / gt_counter_per_class
'''
import glob
import glob
import json
import os
import sys
from pre.cal_IoU import *

def error(msg):
    print(msg)
    sys.exit(0)

def file_lines_to_list(path):
    # open txt file lines to a list
    with open(path) as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content


MINOVERLAP = 0.9  # IoU阈值  default value (defined in the PASCAL  VOC2012 challenge)

if __name__ == '__main__':
    TP = 0
    FP = 0
    gt_counter_per_class = {}
    pred_counter_per_class = {}
    gt_boxes_dic = {}
    pre_boxes_list = []
    # 读取预测文件
    predicted_files_list = glob.glob('./predicted/*.txt')
    predicted_files_list.sort()

    # 读取label文件
    ground_truth_files_list = glob.glob('ground-truth/*.txt')
    if len(ground_truth_files_list) == 0:
        error("Error: No ground-truth files found!")
    ground_truth_files_list.sort()

    for txt_file in ground_truth_files_list:
        # print(txt_file)
        file_id = txt_file.split(".txt", 1)[0]
        file_id = os.path.basename(os.path.normpath(file_id))
        # check if there is a correspondent predicted objects file
        if not os.path.exists('predicted/' + file_id + ".txt"):
            error_msg = "Error. File not found: predicted/" + file_id + ".txt\n"
            error_msg += "(You can avoid this error message by running extra/intersect-gt-and-pred.py)"
            error(error_msg)
        lines_list = file_lines_to_list(txt_file)
        # create ground-truth dictionary
        gt_boxes = []
        for line in lines_list:
            try:
                class_name, x1, y1, x2, y2, x3, y3, x4, y4 = line.split()

            except ValueError:
                error_msg = "Error: File " + txt_file + " in the wrong format.\n"
                error_msg += " Expected: <class_name> <left> <top> <right> <bottom> ['difficult']\n"
                error_msg += " Received: " + line
                error_msg += "\n\nIf you have a <class_name> with spaces between words you should remove them\n"
                error_msg += "by running the script \"remove_space.py\" or \"rename_class.py\" in the \"extra/\" folder."
                error(error_msg)

            # bbox = left + " " + top + " " + right + " " +bottom
            bbox = x1 + ' ' + y1 + ' ' + x2 + ' ' + y2 + ' ' + x3 + ' ' + y3 + ' ' + x4 + ' ' + y4

            gt_boxes.append({"class_name": class_name, "bbox": bbox, "used": False})
            # count that object
            if class_name in gt_counter_per_class:
                gt_counter_per_class[class_name] += 1
            else:
                # if class didn't exist yet
                gt_counter_per_class[class_name] = 1
        gt_boxes_dic[file_id] = gt_boxes


    predicted_files_list = glob.glob('predicted/*.txt')
    predicted_files_list.sort()
    for class_index, class_name in enumerate(gt_counter_per_class):
        for txt_file in predicted_files_list:
            bounding_boxes_pre = []
            # print(txt_file)
            # the first time it checks if all the corresponding ground-truth files exist
            file_id = txt_file.split(".txt", 1)[0]
            file_id = os.path.basename(os.path.normpath(file_id))
            if class_index == 0:
                if not os.path.exists('ground-truth/' + file_id + ".txt"):
                    error_msg = "Error. File not found: ground-truth/" + file_id + ".txt\n"
                    error_msg += "(You can avoid this error message by running extra/intersect-gt-and-pred.py)"
                    error(error_msg)
            lines = file_lines_to_list(txt_file)
            for line in lines:
                tmp_class_name, confidence, x1, y1, x2, y2, x3, y3, x4, y4 = line.split()
                if tmp_class_name == class_name:
                    # print("match")
                    bbox_pre = x1 + ' ' + y1 + ' ' + x2 + ' ' + y2 + ' ' + x3 + ' ' + y3 + ' ' + x4 + ' ' + y4
                    # print(bbox_pre)
                    bounding_boxes_pre.append({"confidence": confidence, "file_id": file_id, "bbox": bbox_pre})
                    # print(bounding_boxes)
            print('file_id:' + str(file_id))
            # 计算IoU，统计TP
            gt_boxes = gt_boxes_dic[file_id]
            bb_match = gt_boxes[0]

            # bb是预测框
            # bb = [float(x) for x in obj_pre["bbox"].split()]
            for obj_pre in bounding_boxes_pre:
                ovmax = -1
                bbpre = list(map(int, obj_pre['bbox'].split()))

                # 寻找最大iou
                for obj_gt in gt_boxes:
                    # gt_boxes是真实检测框
                    bbgt = list(map(int, obj_gt['bbox'].split()))
                    # 如果二者有交集  IoU!=0
                    ov = cal_iou(bbpre, bbgt)
                    # print(bbpre+bbgt)
                    if ov != 0 and ov > ovmax:
                        ovmax = ov
                        bb_match = bbgt
                # 判断是否是TP
                print('ovmax:' + str(ovmax))
                if ovmax > MINOVERLAP:
                    TP += 1
                elif ovmax > 0:
                    print(22222222222222222222222)
                    io = max(cal_iot(bbpre, bb_match), cal_iop(bbpre, bb_match))
                    # if cal_iop(bbpre, bb_match) > 0.6 and cal_iot(bbpre, bb_match) < 0.6:
                    #     print(file_id)
                    print(io)
                    if io > MINOVERLAP:
                        TP += 1
                    else:
                        FP += 1
                else:
                    FP += 1

        # 计算该图片的
    print('MINOVERLAP:'+str(MINOVERLAP))
    for class_name in gt_counter_per_class.keys():
        print(class_name + ' Average Precision:')
        print(TP/gt_counter_per_class[class_name])



