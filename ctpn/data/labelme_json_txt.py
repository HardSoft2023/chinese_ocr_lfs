import os
import json
from functools import reduce
import shutil
def convert(dir_path):
    for f in os.listdir(dir_path):
        if "json" in f:
            stem = f.split(".")[0]
            with open(os.path.join(dir_path, f), encoding="utf-8") as jf, open(os.path.join(dir_path, 'gt_' + stem + '.txt'), "w", encoding="utf-8") as gf:
                label_data = json.load(jf)
                # print(label_data)
                for i in label_data["shapes"]:
                    label_txt = i['label']
                    # 这里得把二维的list拍平
                    x = reduce(lambda x,y: x +y, i['points'])
                    coordinates = ",".join([str(e) for e in x])
                    # print(coordinates)
                    gf.write(f"{coordinates},{label_txt}\n")



# convert("VOC-TAXNOTE")
def repair(dir_p, out_suffix="_fine"):
    new_dir = dir_p + out_suffix
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.makedirs(new_dir)
    for f in os.listdir(dir_p):
        if ".jpg" in f:
            stem = f.split(".")[0]
            if os.path.exists(f"{dir_p}/{stem}.txt"):
                new_stem = stem.replace("(","_").replace(")","_")
                # 需要做的有两件事，一个是图片重命名，一个是文本，重命名
                shutil.copy2(os.path.join(dir_p, f), os.path.join(new_dir,f"{new_stem}.jpg"))
                shutil.copy2(os.path.join(dir_p, f"{stem}.txt"), os.path.join(new_dir,f"gt_{new_stem}.txt"))
repair("SROIE2019")