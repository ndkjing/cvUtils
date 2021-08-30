# cvUtils
opencv 工具函数
`dsa`
## 拼接图片
./concateImg/simple_concate.py
图片 1
![avatar](./concateImg/img4.png)
图片 2
![avatar](./concateImg/img5.png)
拼接使用特征点
![avatar](./concateImg/concate4_5.png)
拼接结果
![avatar](./concateImg/concate4_5_result.png)


## 选择图片中目标颜色区域
./selectRoi/select_roi_hsv.py
原始图片
![avatar](./selectRoi/tecent_1.png)

第一步 选择需要分割出湖泊区域

![avatar](./selectRoi/tecent_1_roi.png)

第二步 分析选择区域图片HSV分布
![avatar](./selectRoi/hsv.png)

第三步 调节HSV阈值观察mask区域是否较好分割出目标区域
![avatar](./selectRoi/mask.png)