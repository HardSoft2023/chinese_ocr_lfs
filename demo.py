#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import pickle
import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob
image_files = glob('./test_images/*.*')


if __name__ == '__main__':
    result_dir = './test_result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)

    for image_file in sorted(image_files):
        image = np.array(Image.open(image_file).convert('RGB'))
        t = time.time()
        result, image_framed = ocr.model(image, os.path.basename(image_file))
        output_file = os.path.join(result_dir, image_file.split('/')[-1])
        Image.fromarray(image_framed).save(output_file)
        print("Mission complete, it took {:.3f}s".format(time.time() - t))
        print("\nRecognition Result:\n")
	    #print("---type--", result)
	    #print("---filenamne is ----", image_file.split('/')[-1])
        with open(output_file + ".pkl", "wb") as fp:
            pickle.dump(result, fp, protocol=pickle.HIGHEST_PROTOCOL)
            for key in result:
                print(str(result[key][1]))

