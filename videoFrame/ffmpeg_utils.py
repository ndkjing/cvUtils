import queue
import threading
import cv2 as cv
import subprocess as sp


class Live(object):
    def __init__(self,camera_path,rtmp_url):
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        self.rtmpUrl = rtmp_url
        self.camera_path = camera_path

    def read_frame(self):
        print("开启推流")
        cap = cv.VideoCapture(self.camera_path)

        # Get video information
        fps = int(cap.get(cv.CAP_PROP_FPS))
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        # ffmpeg command
        self.command = [r'F:\downloads\nginx_ffmpeg\ffmpeg\bin\ffmpeg.exe',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(25),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmpUrl]

        # read webcamera
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                print("Opening camera is failed")
                # 说实话这里的break应该替换为：
                # cap = cv.VideoCapture(self.camera_path)
                # 因为我这俩天遇到的项目里出现断流的毛病
                # 特别是拉取rtmp流的时候！！！！
                break

            # put frame into queue
            self.frame_queue.put(frame)

    def push_frame(self):
        # 防止多线程时 command 未被设置
        print('p')
        while True:
            print(len(self.command))
            if len(self.command) > 0:
                # 管道配置
                p = sp.Popen(self.command, stdin=sp.PIPE)
                print(p)
                break

        while True:
            if self.frame_queue.empty() != True:
                frame = self.frame_queue.get()
                print(frame.shape)
                # process frame
                # 你处理图片的代码
                # write to pipe
                p.stdin.write(frame.tostring())

    def run(self):
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,))
        ]
        [thread.setDaemon(True) for thread in threads]
        [thread.start() for thread in threads]
        [thread.join(True) for thread in threads]


if __name__ == '__main__':
    live_obj = Live(camera_path=r'F:\datasets\ffmpeg_test.flv',rtmp_url='rtmp://47.97.183.24:1935/stream/test')
    live_obj.run()