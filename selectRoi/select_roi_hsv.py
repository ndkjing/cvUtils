import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

# 文件路径
# img_path = '../imgs/lena.png'
img_path = './tecent_1.png'
img_dir, img_name = os.path.split(img_path)[0], os.path.split(img_path)[1]
write_path = os.path.join(
    img_dir,
    img_name.split('.')[0] +
    '_roi.' +
    img_name.split('.')[1])


def select_roi():
    """
    选取ROI区域
    回车或者空格确认选择
    c键 撤销选择
    """

    # 读入图片
    img = cv2.imread(img_path)
    if img is None:
        print("图片读入失败, 请检查图片路径及文件名")
        exit()
    # 创建一个窗口
    cv2.namedWindow("image", flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    cv2.imshow("image", img)
    # 是否显示网格
    showCrosshair = True

    # 如果为Ture的话 , 则鼠标的其实位置就作为了roi的中心
    # False: 从左上角到右下角选中区域
    fromCenter = False
    # Select ROI
    rect = cv2.selectROI("image", img, showCrosshair, fromCenter)

    print("选中矩形区域")
    (x, y, w, h) = rect

    # Crop image
    imCrop = img[y: y + h, x:x + w]

    # Display cropped image
    cv2.imshow("image_roi", imCrop)
    print('write_path',write_path)
    cv2.imwrite(write_path, imCrop)
    cv2.waitKey(0)


'''
绘制彩图在HSV颜色空间下的统计直方图
'''


def analyse_hsv():
    # 读入图片
    img = cv2.imread(write_path)
    if img is None:
        print("图片读入失败, 请检查图片路径及文件名")
        exit()

    # 将图片转换为HSV格式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 创建画布
    fig, ax = plt.subplots()
    # Matplotlib预设的颜色字符
    hsvColor = ('y', 'g', 'k')
    # 统计窗口间隔 , 设置小了锯齿状较为明显 最小为1 最好可以被256整除
    bin_win = 3
    # 设定统计窗口bins的总数
    bin_num = int(256 / bin_win)
    # 控制画布的窗口x坐标的稀疏程度. 最密集就设定xticks_win=1
    xticks_win = 2
    # 设置标题
    ax.set_title('HSV Color Space')
    lines = []
    for cidx, color in enumerate(hsvColor):
        # cidx channel 序号
        # color r / g / b
        cHist = cv2.calcHist([img], [cidx], None, [bin_num], [0, 256])
        # 绘制折线图
        line, = ax.plot(cHist, color=color, linewidth=8)
        lines.append(line)

        # 标签
    labels = [cname + ' Channel' for cname in 'HSV']
    # 添加channel
    plt.legend(lines, labels, loc='upper right')
    # 设定画布的范围
    ax.set_xlim([0, bin_num])
    # 设定x轴方向标注的位置
    ax.set_xticks(np.arange(0, bin_num, xticks_win))
    # 设定x轴方向标注的内容
    ax.set_xticklabels(list(range(0, 256, bin_win * xticks_win)), rotation=45)

    # 显示画面
    plt.show()


'''
    可视化颜色阈值调参软件
    H 100
    S 78
    V 250
'''


# 更新MASK图像，并且刷新windows
def updateMask():
    global img
    global lowerb
    global upperb
    global mask
    # 计算MASK
    mask = cv2.inRange(img_hsv, lowerb, upperb)

    cv2.imshow('mask', mask)


# 更新阈值
def updateThreshold(x):
    global lowerb
    global upperb

    minH = cv2.getTrackbarPos('minH', 'image')
    maxH = cv2.getTrackbarPos('maxH', 'image')
    minS = cv2.getTrackbarPos('minS', 'image')
    maxS = cv2.getTrackbarPos('maxS', 'image')
    minV = cv2.getTrackbarPos('minV', 'image')
    maxV = cv2.getTrackbarPos('maxV', 'image')

    lowerb = np.int32([minH, minS, minV])
    upperb = np.int32([maxH, maxS, maxV])

    print('更新阈值')
    print(lowerb)
    print(upperb)
    updateMask()


def hsv_image_threshold():
    global img_hsv
    global upperb
    global lowerb
    global mask

    img = cv2.imread(img_path)
    if img is None:
        print("Error: 文件路径错误，没有此图片 {}".format(img_path))
        exit(1)
    # 将图片转换为HSV格式
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 颜色阈值 Upper
    upperb = None
    # 颜色阈值 Lower
    lowerb = None

    mask = None

    cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    # cv2.namedWindow('image')
    cv2.imshow('image', img)

    # cv2.namedWindow('mask')
    cv2.namedWindow('mask', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

    # 红色阈值 Bar
    # 红色阈值下界
    cv2.createTrackbar('minH', 'image', 0, 255, updateThreshold)
    # 红色阈值上界
    cv2.createTrackbar('maxH', 'image', 0, 255, updateThreshold)
    # 设定红色阈值上界滑条的值为255
    cv2.setTrackbarPos('maxH', 'image', 255)
    cv2.setTrackbarPos('minH', 'image', 0)
    # 绿色阈值 Bar
    cv2.createTrackbar('minS', 'image', 0, 255, updateThreshold)
    cv2.createTrackbar('maxS', 'image', 0, 255, updateThreshold)
    cv2.setTrackbarPos('maxS', 'image', 255)
    cv2.setTrackbarPos('minS', 'image', 0)
    # 蓝色阈值 Bar
    cv2.createTrackbar('minV', 'image', 0, 255, updateThreshold)
    cv2.createTrackbar('maxV', 'image', 0, 255, updateThreshold)
    cv2.setTrackbarPos('maxV', 'image', 255)
    cv2.setTrackbarPos('minV', 'image', 0)

    # 首次初始化窗口的色块
    # 后面的更新 都是由getTrackbarPos产生变化而触发
    updateThreshold(None)

    print("调试棋子的颜色阈值, 键盘摁e退出程序")
    while cv2.waitKey(0) != ord('e'):
        continue

    cv2.imwrite('tmp_bin.png', mask)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 1 选择目标区域
    # select_roi()
    # 2 分析hsv值
    # analyse_hsv()
    # 3 调节分割阈值
    hsv_image_threshold()
