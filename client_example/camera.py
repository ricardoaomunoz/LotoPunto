import sys
sys.path.insert(0, '../src/services/')
from camera_service import PicameraControl

cam = PicameraControl()
cam.preview(120)
