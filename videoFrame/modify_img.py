import os
import cv2

old_path = r'C:\PythonProject\lpr\plate_test\crop_plate\\'
new_path = r'C:\PythonProject\lpr\plate_test\pr\\'
f1 = os.listdir(old_path)
f2 = os.listdir(new_path)
print('原文件个数：', len(f1))
print('新文件个数：', len(f2))


def resize():
    for i in f1:
        oldname = old_path + i
        img = cv2.imread(oldname, 1)
        img = cv2.resize(img, (94, 24), interpolation=cv2.INTER_CUBIC)
        newname = new_path + i
        try:
            cv2.imwrite(newname, img)
        except BaseException:
            continue


def split_img():
    f1 = open(
        r'C:\ChromeDownload\VOCdevkit\VOC2007\ImageSets\Main\person_trainval.txt')
    f2 = open(r'C:\ChromeDownload\VOCdevkit\VOC2007\ImageSets\Main\person_test.txt')
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    # print(type(lines1),lines)
    person_list = []
    for line in lines1:
        # print(line,line[-3],line[-2])
        if line[-3] == " " and line[-2] == "1":
            print(line[:6])
            person_list.append(line[:6])
    print(len(person_list), person_list)
    # print(type(line),line[-3])
    f1.close()
    for line in lines2:
        # print(line,line[-3],line[-2])
        if line[-3] == " " and line[-2] == "1":
            print(line[:6])
            person_list.append(line[:6])
    print(len(person_list), person_list)
    f2.close()
    return person_list

# person_list = split_img()
# for person in person_list:
#     oldname = old_path + person + '.xml'
#     newname = new_path + person + '.xml'
#     cmd = 'copy "%s" "%s"' % (oldname, newname)
#     os.system(cmd)


def rewrite_img():
    # i = len(os.listdir(new_path))+1
    # print(i)
    i = 1
    for name in f1:
        oldname = old_path + name
        newname = old_path + '%d.jpg' % i
        # img = cv2.imread(oldname,1)
        # # img = cv2.resize(img, (512,512), interpolation=cv2.INTER_CUBIC)
        # newname = new_path + name.split('.')[0] + '.png'
        # try:
        #     cv2.imwrite(newname,img)
        # except:
        #     continue
        os.rename(oldname, newname)
        print(oldname, '---->', newname)
        i = i + 1

# rewrite_img()


def rename_func():
    i = 1
    for name in f1:
        oldname = old_path + name
        newname = old_path + '%d.jpg' % i
        # img = cv2.imread(oldname,1)
        # # img = cv2.resize(img, (512,512), interpolation=cv2.INTER_CUBIC)
        # newname = new_path + name.split('.')[0] + '.png'
        # try:
        #     cv2.imwrite(newname,img)
        # except:
        #     continue
        os.rename(oldname, newname)
        print(oldname, '---->', newname)
        i = i + 1

# rename_func()
#
#
# name_num = 1


def rotate(angle, center=None, scale=1.0):
    # 获取图像尺寸
    global name_num
    for name in f1:
        old_name = old_path + name
        image = cv2.imread(old_name)
        (h, w) = image.shape[:2]

        # 若未指定旋转中心，则将图像中心设为旋转中心
        if center is None:
            center = (w / 2, h / 2)

        # 执行旋转
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))
        new_name = new_path + str(name_num) + '.png'
        # 写入图像
        name_num = name_num + 1
        cv2.imwrite(new_name, rotated)
        print(old_name, "--->", new_name)
    # 返回旋转后的图像
    # return rotated


resize()
# rotate(0)
# rotate(90)
# rotate(-90)
# rename_func()
