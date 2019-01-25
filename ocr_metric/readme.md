# 1. 使用方法

1. 将标注数据json放在./pre/jsons文件夹（文件名FILE_ID.txt）
2. 将ocr生成txt文件放在./pre/txt文件夹 （文件名FILE_ID.txt）
3. 需保持标注数据和检测结果数据的FILE_ID一致
4. 生成predicted标准数据： python gen_predicted.py
5. 生成group-truth标准数据：python gen_group-truth.py
6. 计算检测精度：python cal_precision.py
7. 查看某一幅图像的评价结果: python plot_fig.py

## 2. precision评估方式

- 采用准确率precision来评估当前业务的文本检测结果
- precision计算方式如下：
  - precision = TP / GT
  - 其中，TP表示预测数据中所有达到检测标准的检测框数量，GT代表真实数据中所有标注框的数量
- 是否达到检测标准的计算方式：
  - 对预测图片的任一预测框，匹配与其IoU值最大的真实框，并记录IoU
  - 比较该IoU与阈值MINOVERLAP的大小，若大于该阈值，则TP+1
- IoU计算方式：
