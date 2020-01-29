import time
import picamera

class PicameraControl(object):
    def __init__(self):
        self.picx = picamera.PiCamera()

    def preview(self, preview_time):
        self.picx.start_preview()
        time.sleep(preview_time)
        self.picx.stop_preview()
        self.picx.close()

    def take_picture(self, path):
        self.picx.resolution = (2592, 1944)
        self.picx.start_preview()
        time.sleep(3)
        self.picx.capture(path)
        self.picx.stop_preview()
        self.picx.close()

    def start_video(self, video_path, ):
        self.picx.start_preview()
        self.picx.start_recording('mi_video.h264')
        self.picx.wait_recording(20)
        self.picx.stop_recording()
        self.picx.stop_preview()
        self.picx.close()