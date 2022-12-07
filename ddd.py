# Python Downloader
# pip install internetdownloadmanager
import internetdownloadmanager as idm
def Downloader(url, output):
    pydownloader = idm.Downloader(worker=20,
                                  part_size=1024*1024*10,
                                  resumable=True,)

    pydownloader .download(url, output)
Downloader("http://ww1.sinaimg.cn/crop.0.0.640.640.640/549d0121tw1egm1kjly3jj20hs0hsq4f.jpg", "image.jpg")
# Downloader("Link url", "video.mp4")
