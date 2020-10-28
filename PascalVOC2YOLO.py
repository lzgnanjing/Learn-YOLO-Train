"""
@version: 1.0
@author: luzhigang
@copyright: luzhigang
@contact: luzhigang1988@live.com
@site:
@software: PyCharm
@file: PascalVOC2YOLO.py
@time: 2020/10/14 0014 15:17
"""

# this script is used to convert PascalVOC format xml files to YOLO txt format.
# script will generate summary.txt file for summarize per labels count.
# script will also generate files for per labels to indicate which image file\
#     contain this label.
# input parameter1: --classes.\
#                   classes.txt file who contain the labeled labels.per label per line.
# input parameter2: --PascalVOC.\
#                   PascalVOC format xml files folder path
# output parameter: --YOLO.folder path to save YOLO txt files.
#

import os
import xml.etree.ElementTree as ET
import argparse

# Creating argument parser to take paths from command line
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--classes', required=True, help="classes.txt Path")
ap.add_argument('-p', '--PascalVOC', required=True, help="PascalVoc format xml files folder path")
ap.add_argument('-y', '--YOLO', required=True, help='folder to save YOLO format txt files')

args = vars(ap.parse_args())
classes_txt_path = args['classes']
xml_path = args['PascalVOC']
save_dir = args['YOLO']

fid_ctf = open(classes_txt_path)
labels_lst = fid_ctf.readlines()
labels_lst = [x.strip() for x in labels_lst if x.strip() != '']
fid_arr = []
label_count_arr = []
for label in labels_lst:
    fid = open(label + '.txt', 'w')
    fid_arr.append(fid)
    label_count_arr.append(0)

# summarize every label's count
summary_fid = open('summary.txt', 'w')

# create empty folder.
if os.path.exists(save_dir):
    os.rmdir(save_dir)
os.makedirs(save_dir)

for fp in os.listdir(xml_path):
    if fp.endswith('.xml'):
        root = ET.parse(os.path.join(xml_path, fp)).getroot()
        xmin, ymin, xmax, ymax = 0, 0, 0, 0
        sz = root.find('size')
        width = float(sz[0].text)
        height = float(sz[1].text)
        filename = root.find('filename').text
        for child in root.findall('object'):  # 找到图片中的所有框

            sub = child.find('bndbox')  # 找到框的标注值并进行读取
            label = child.find('name').text
            idx = labels_lst.index(label)
            if idx >= 0:
                fid_arr[idx].write(filename + '\n')
                label_count_arr[idx] += 1
            else:
                print('unspoorted label:' + label + '.image file:' + filename)
                continue

            xmin = float(sub[0].text)
            ymin = float(sub[1].text)
            xmax = float(sub[2].text)
            ymax = float(sub[3].text)
            try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
                x_center = (xmin + xmax) / (2 * width)
                x_center = '%.6f' % x_center
                y_center = (ymin + ymax) / (2 * height)
                y_center = '%.6f' % y_center
                w = (xmax - xmin) / width
                w = '%.6f' % w
                h = (ymax - ymin) / height
                h = '%.6f' % h
            except ZeroDivisionError:
                print(filename, '的 width有问题')

            with open(os.path.join(save_dir, fp.split('.xml')[0] + '.txt'), 'a+') as f:
                f.write(' '.join([str(idx), str(x_center), str(y_center), str(w), str(h) + '\n']))
print('convert finished.')

for i in range(len(label_count_arr)):
    summary_fid.write(labels_lst[i] + ':' + str(label_count_arr[i]) + '\n')
summary_fid.close()

# close all label files
for fid in fid_arr:
    fid.close()

