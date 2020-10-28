# Learn-YOLO-Train

本工程致力于分享用YOLO做目标检测所需要用到的知识、工具脚本。 \
希望对大家有帮助。 \
PascalVOC2YOLO.py：将LabelImg标注生成的PascalVOC的xml文件转换为YOLO的txt文件。 
>输入：用户提供含有labels名的classes.txt文件。\
  输入：含有xml文件夹路径。 
  输入：转换后生成的txt文件存储路径。 \
  输出：当前脚本目录下每个label生成一个txt文件，记录含有该label的图片名。 \
  输出：当前脚本目录下生成summary.txt，记录每个label的标签数。
