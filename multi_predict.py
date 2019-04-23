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
                tmp_box_list = [str(e).strip() for e in f.readlines()]
            text_recs = np.zeros((len(tmp_box_list), 8), np.int)
            for i, rec_line in zip(range(len(tmp_box_list)), tmp_box_list):
                rec_line = [float(m) for m in rec_line.split(",")]
                # 把逆时针调整为顺时针，这个地方是关键。
                text_points = rec_line

                left_top_p = [text_points[0]]
                # 对剩余的三个点就行倒置
                remaing_p = text_points[1:]
                remaing_p.reverse()
                new_points = left_top_p + remaing_p

                rec_line = new_points
                # 把逆时针调整为顺时针，这个地方是关键。
                for j, ele in zip(range(8), rec_line):
                    text_recs[i][j] = ele
            result = ocr.advanced_model(image, os.path.basename(image_file), text_recs)
            output_file = os.path.join(result_dir, image_file.split('/')[-1])
            print("Mission complete, it took {:.3f}s".format(time.time() - t))
            print("\nRecognition Result:\n")
            with open(output_file + ".pkl", "wb") as fp, open(output_file + "_result.txt", "w") as rf:
                pickle.dump(result, fp, protocol=pickle.HIGHEST_PROTOCOL)
                for key in result:
                    # 结果写入文件
                    rf.write("%s\n", (str(result[key][1]).strip()))
                    print(str(result[key][1]))
