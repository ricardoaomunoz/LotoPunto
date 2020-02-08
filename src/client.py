import time
import os

from services.receipt_content import ReceiptHeader, ReceiptDescription
this_dir, this_filename = os.path.split(__file__)
GRAPHICS_PATH = os.path.join(this_dir, "examples/graphics/climacons/clear-night.png")

person = ReceiptHeader(9878654524313, None, 1, "demo")
person.print_header()
lista = (["QTY", "PRICE", "DESCRIPTION", "TOTAL"],["01", "160,99", "SKIRT", 500.00],["02", "10.33", "COAT", 300.01],["03", "100,99", "SKIRT", 200.00], ["04", "20.01", "SKIRT", 20.02])
person.print_description(lista)
person.print_bottom("Factura de venta N W:B345 \n Autorizacion de Numercion de Facturacion DIAN sistema POS: 12643677863877364 26/09/2019 - Vigencia 24 meses \n ")


from services.camera_service import PicameraControl

cam = PicameraControl()
cam.preview(5)
cam.stop_recordingvideo
cam.start_video("video_prueba.h264")
time.sleep(5)
cam.stop_recordingvideo()
codigoQR = cam.read_code()
print(codigoQR)

#person1 = ReceiptDescription(2, "Aca empieza la descripcion", (["QTY", "PRICE", "DESCRIPTION", "TOTAL"],["01", "160,99", "SKIRT", "500.00"],["02", "10.33", "COAT", "300.01"]))
#person1.print_description()