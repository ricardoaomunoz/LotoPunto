import sys
sys.path.insert(0, '../src/')
from src.services.camera_service import PicameraControl

cam = PicameraControl()
cam.preview(120)