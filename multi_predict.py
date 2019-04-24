#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import argparse
import os
import pickle
import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob
import json
image_files = glob('./test_images/*.*')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--detect_method', '-m', default='AdvancedEAST')
    parser.add_argument('--rec_text_path', '-p', default="/other/demo")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    result_dir = './test_result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)
    if args.detect_method == "AdvancedEAST":
        for txt_f in glob(os.path.join(args.rec_text_path, '*.txt')):
            # 获取到所有的东西。
            image_file = txt_f[:-4]
            print("current processing image is %s", (image_file))
            image = np.array(Image.open(image_file).convert('RGB'))
            t = time.time()
            # 在这里添加给边框赋值
            with open(txt_f) as f:
                tmp_box_list = [str(e).strip().split(",") for e in f.readlines()]
            text_recs = np.zeros((len(tmp_box_list), 8), np.int)
            for i_row, rec_line in enumerate(tmp_box_list):
                rec_line = [float(m) for m in rec_line]
                # ctpn返回的既不是顺时针也不是逆时针，而是自上而下，自左而右。二行二列。
                # 调整为[(),()]
                text_points = []
                for i in range(8):
                    if i % 2 == 1:
                        text_points.append((rec_line[i - 1], rec_line[i]))
                top_l_r = [text_points[0]] + [text_points[3]]
                bottom_l_r = [text_points[1]] + [text_points[2]]
                new_points = top_l_r + bottom_l_r
                rec_line = new_points
                new_points = [ee for e in new_points for ee in e]
                # ctpn返回的既不是顺时针也不是逆时针，而是自上而下，自左而右。二行二列。
                for j_col, ele in enumerate(new_points):
                    text_recs[i_row, j_col] = ele
            result = ocr.advanced_model(image, os.path.basename(image_file), text_recs)
            output_file = os.path.join(result_dir, image_file.split('/')[-1])
            print("Mission complete, it took {:.3f}s".format(time.time() - t))
            print("\nRecognition Result:\n")
            with open(output_file + ".pkl", "wb") as fp, open(output_file + "_result.json", "w") as rf:
                pickle.dump(result, fp, protocol=pickle.HIGHEST_PROTOCOL)
                json.dump(result, rf)
                for key in result:
                    # 结果写入文件
                    # rf.write("%s\n", (str(result[key][1]).strip()))
                    print(str(result[key][1]))
