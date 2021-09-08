"""
扩展卡尔曼滤波
GPS 与imu数据融合
"""
import math

import com_data
import ekf
import get_imu_data
import lng_lat_calculate
from collections import deque
import threading
import copy
import time
import numpy as np
import matplotlib.pyplot as plt

# 读取gps
# 读取imu 速度 角速度
# 输入到扩展卡尔曼滤波获取结果
# 每十秒计算误差


xEst = np.zeros((4, 1))
PEst = np.eye(4)
xDR = np.zeros((4, 1))  # Dead reckoning

# history
hxEst = np.zeros((4, 1))
hxDR = np.zeros((4, 1))
hz = np.zeros((2, 1))
pre_x = np.zeros((4, 1))

init_gps = None
current_gps = None  # 当前位置相对于起始位置漂移
z = [None, None, None, None]
sum_ekf_error = 0  # 卡尔曼滤波合计误差


class IsUpdate:
    def __init__(self):
        self.is_update_imu = False
        self.is_update_gps = False


def get_gps_data(is_update_obj,gps_config):
    global init_gps
    global current_gps
    global sum_ekf_error
    serial_obj1 = com_data.ComData(gps_config[0],
                                   gps_config[1],
                                   timeout=1,
                                   )
    pre_lng_lat = None
    error_list = deque(maxlen=50)
    while True:
        data1 = serial_obj1.readline()
        # print('data1',data1)
        str_data1 = bytes(data1).decode('ascii')
        if str_data1.startswith('$GNGGA'):
            data_list1 = str_data1.split(',')
            # print(data_list1)
            lng1, lat1 = float(data_list1[4][:3]) + float(data_list1[4][3:]) / 60, float(data_list1[2][:2]) + float(
                data_list1[2][2:]) / 60
            # print('经纬度1', lng1, lat1)
            # print('误差1', data_list1[8])
            if lng1 > 1 and lat1 > 1:
                if init_gps is None:
                    init_gps = [lng1, lat1]
                current_lng_lat = [lng1, lat1]
                current_gps = lng_lat_calculate.get_x_y_distance(init_gps, current_lng_lat)
            else:
                continue
            is_update_obj.is_update_gps = True
            if pre_lng_lat is not None:
                error = lng_lat_calculate.distanceFromCoordinate(current_lng_lat[0], current_lng_lat[1], pre_lng_lat[0],
                                                                 pre_lng_lat[1])
                # print('error',error)
                error_list.append(error)
                if len(error_list) >= 50:
                    print('gps error', sum(error_list))
                    print('sum_ekf_error error', sum_ekf_error)
                    error_list.clear()
                    sum_ekf_error = 0
            if current_lng_lat is not None:
                pre_lng_lat = copy.deepcopy(current_lng_lat)
        time.sleep(0.2)


def ekf_data(v, yawrate, z, pre_x):
    global PEst
    global sum_ekf_error
    # State Vector [x y yaw v]'
    u = np.array([[v], [yawrate]])
    # 真实值 观测值 预测值 带误差控制量 = （真实值，预测值，控制量）
    # xTrue, z, xDR, ud = ekf.observation(xTrue, xDR, u)
    ud = u
    xDR = ekf.motion_model(pre_x, u)
    t_dr = xDR
    # 估计值  状态协方差
    z = np.array([[z[0]], [z[1]]])
    xEst, PEst = ekf.ekf_estimation(pre_x, PEst, z, ud)
    # print('xEst',xEst)
    sum_ekf_error += math.sqrt(xEst[0] ** 2 + xEst[1] ** 2)
    return xDR, xEst


def main():
    global xEst
    global PEst
    global hxEst
    global hxDR
    global hxTrue
    global hz
    global pre_x
    is_update_obj = IsUpdate()
    imu_config = ['com13', 115200]
    gps_config = ['com11', 115200]
    imu_obj = get_imu_data.GetImuData(port=imu_config[0], baud=imu_config[1])
    # 打印数据
    t1 = threading.Thread(target=imu_obj.get_data, args=(is_update_obj,))
    t2 = threading.Thread(target=get_gps_data, args=(is_update_obj,gps_config))
    t1.setDaemon(True)
    t2.setDaemon(True)

    t1.start()
    t2.start()
    # 打开交互模式
    plt.ion()
    # t1.join()
    # t2.join()
    while True:
        time.sleep(0.001)
        # 初始化GPS后才开始计算
        if init_gps is None:
            continue
        # 判断接受到了新数据
        if is_update_obj.is_update_imu:
            is_update_obj.is_update_imu = False
            xDR, xEst = ekf_data(imu_obj.v, imu_obj.yaw_rate_z,
                                 [current_gps[0], current_gps[1], imu_obj.v, imu_obj.yaw_rate_z], pre_x)
            pre_x = copy.deepcopy(xEst)
            # 滤波值
            hxEst = np.hstack((hxEst, xEst))
            # 预测值
            hxDR = np.hstack((hxDR, xDR))
        if is_update_obj.is_update_gps:
            is_update_obj.is_update_gps = False
            xDR, xEst = ekf_data(imu_obj.v, imu_obj.yaw_rate_z,
                                 [current_gps[0], current_gps[1], imu_obj.v, imu_obj.yaw_rate_z], xEst)
            # store data history
            # 观测值
            hz = np.hstack((hz, np.asarray(current_gps).reshape(2, 1)))
            print(hz.shape, hxEst.shape, hxDR.shape)
        if hxEst.shape[1] % 2 == 0:
            # 清除原有图像
            plt.cla()
            plt.plot(hz[0, :], hz[1, :], ".g")
            # plt.plot(hxTrue[0, :].flatten(),
            #          hxTrue[1, :].flatten(), "-b")
            plt.plot(hxDR[0, :].flatten(),
                     hxDR[1, :].flatten(), "-k")
            plt.plot(hxEst[0, :].flatten(),
                     hxEst[1, :].flatten(), "-r")
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.01)
        plt.show()


if __name__ == '__main__':
    main()
    # get_gps_data()
