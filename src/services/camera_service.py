
''' This service is the responsable of the camera control '''
import time
import picamera
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

''' PicameraControl class has one argument that is the camera controller
and a few methods '''
class PicameraControl(object):
    def __init__(self):
        self.picx = picamera.PiCamera()

    def preview(self, preview_time):
        try:
            self.picx.start_preview()
            time.sleep(preview_time)
            self.picx.stop_preview()
            return 1
            # self.picx.close()
        except Exception as Err:
            print(f"### Error ### {Err}")
            return 0

    def take_picture(self, path):
        try:
            self.picx.resolution = (2592, 1944)
            self.picx.start_preview()
            time.sleep(3)
            self.picx.capture(path)
            self.picx.stop_preview()
            self.picx.close()
        except Exception as Err:
            print(f"### Error ### {Err}")
            return 0

    def start_video(self, video_path):
        try:
            self.picx.start_preview()
            self.picx.start_recording(video_path)
            self.picx.wait_recording()
            return 1
        except Exception as Err:
            print(f"### Error ### {Err}")
            return 0

    def stop_recordingvideo(self):
        try:
            self.picx.stop_recording()
            self.picx.stop_preview()
            self.picx.close()
            return 1
        except Exception as Err:
            print(f"### Error ### {Err}")
            return 0

    def close(self):
        try:
            self.picx.close()
            return 1
        except Exception as Err:
            print(f"### Error ### {Err}")
            return 0

    def read_code(self):
        timeToread=0
        read_ready = True
        print("[INFO] starting video stream...")
        # vs = VideoStream(src=0).start()
        try:
            vs = VideoStream(usePiCamera=True).start()
            time.sleep(2.0)
            while read_ready:
                # grab the frame from the threaded video stream and resize it to
                # have a maximum width of 400 pixels
                frame = vs.read()
                frame = imutils.resize(frame, width=400)

                # find the barcodes in the frame and decode each of the barcodes
                barcodes = pyzbar.decode(frame)

                if len(barcodes) > 1:
                    print("More than 1 barcode")
                    find = False
                    data = "More than one imagen"
                    tipo = ""
                    read_ready = False
                elif len(barcodes) < 1:
                    timeToread+=1
                    if timeToread >= 10000:
                        print("time out to read barcode")
                        find = False
                        data = "Not Found"
                        tipo = ""
                        read_ready = False

                else:
                    # extract the bounding box location of the barcode and draw
                    # the bounding box surrounding the barcode on the image
                    (x, y, w, h) = barcodes[0].rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # the barcode data is a bytes object so if we want to draw it
                    # on our output image we need to convert it to a string first
                    data = barcodes[0].data.decode("utf-8")
                    tipo = barcodes[0].type
                    find = True
                    read_ready = False
                #time.sleep(0.1)
                # show the output frame
                cv2.imshow("Barcode Scanner", frame)
                key = cv2.waitKey(1) & 0xFF
                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break

            return ([find, data, tipo])
        except Exception as Err:
            print(f"### Error ### {Err}")
            return ([False, "", ""])

