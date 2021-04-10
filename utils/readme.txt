ffmpeg.exe -re -i .\ffmpeg_test.flv -vcodec libx264 -acodec aac -f flv rtmp://192.168.8.5:1935/live/home

nginx.exe -c conf\nginx-win.conf