def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue
"""
需要安装pip install --upgrade onvif_zeep
"""

from onvif import ONVIFCamera
import zeep
import time
import requests
from requests.auth import HTTPDigestAuth



def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue


class Onvif_hik(object):
    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password
        zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue
        self.save_path = "./{}T{}.jpg".format(self.ip, str(time.time()))  # 截图保存路径

    def content_cam(self):
        """
        链接相机地址
        :return:
        """
        try:
            self.mycam = ONVIFCamera(self.ip, 80, self.username, self.password)
            self.media = self.mycam.create_media_service()  # 创建媒体服务
            self.media_profile = self.media.GetProfiles()[0]  # 获取配置信息
            self.ptz = self.mycam.create_ptz_service()  # 创建控制台服务
            return True
        except Exception as e:
            return False

    def Snapshot(self):
        """
        截图
        :return:
        """
        res = self.media.GetSnapshotUri({'ProfileToken': self.media_profile.token})

        response = requests.get(res.Uri, auth=HTTPDigestAuth(self.username, self.password))
        # 保存截图
        with open(self.save_path, 'wb') as f:
            f.write(response.content)

    def get_presets(self):
        """
        获取预置点列表
        :return:预置点列表--所有的预置点
        """
        # 获取所有预置点,返回值：list
        presets = self.ptz.GetPresets({'ProfileToken': self.media_profile.token})
        return presets

    def goto_preset(self, presets_token: int):
        """
        移动到指定预置点
        :param presets_token: 目的位置的token，获取预置点返回值中
        :return:
        """
        try:
            self.ptz.GotoPreset(
                {'ProfileToken': self.media_profile.token, "PresetToken": presets_token})  # 移动到指定预置点位置
        except Exception as e:
            print({'error':e})

    def zoom(self, zoom: str, timeout: float = 0.1):
        """
        变焦
        :param zoom: 拉近或远离
        :param timeout: 生效时间
        :return:
        """
        request = self.ptz.create_type('ContinuousMove')
        request.ProfileToken = self.media_profile.token
        request.Velocity = {"Zoom": zoom}
        self.ptz.ContinuousMove(request)
        time.sleep(timeout)
        self.ptz.Stop({'ProfileToken': request.ProfileToken})

    def get_rtsp(self):
        obj = self.media.create_type('GetStreamUri')
        obj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
        obj.ProfileToken = self.media_profile.token
        res_uri = self.media.GetStreamUri(obj)['Uri']
        return res_uri


#获取当前位置信息
def getStatus():
    zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue
    mycam = ONVIFCamera("192.168.8.237", 80, "admin", "xxl123456")
    media = mycam.create_media_service()
    ptz = mycam.create_ptz_service()
    params = ptz.create_type('GetStatus')
    media_profile = media.GetProfiles()[0]  # 获取配置信息
    print(media_profile.token)
    params.ProfileToken = media_profile.token
    res = ptz.GetStatus(params)
    print(res)


if __name__ == '__main__':
    # absolute_move()
    # snap()
    # gotoPreset()
    getStatus()
    obj = Onvif_hik("192.168.8.237", "admin", "xxl123")
    obj.content_cam()
    print(obj.get_rtsp())
    # obj.zoom("1",timeout=0.5)
    # obj.Snapshot()