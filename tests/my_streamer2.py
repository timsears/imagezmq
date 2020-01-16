"""test_2_rpi_send_images.py -- send PiCamera image stream.

A Raspberry Pi test program that uses imagezmq to send image frames from the
PiCamera continuously to a receiving program on a Mac that will display the
images as a video stream.

This program requires that the image receiving program be running first. Brief
test instructions are in that program: test_2_mac_receive_images.py.
"""

# import imagezmq from parent directory
import sys
sys.path.insert(0, '../imagezmq')  # imagezmq.py is in ../imagezmq

import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq
import argparse
import socket

picam = VideoStream(usePiCamera=True, resolution=(1200, 1200)).start()
time.sleep(1.0)  # allow camera sensor to warm up

parser = argparse.ArgumentParser()
parser.add_argument('--server', dest = 'server',
                    help='Name of the server to send images to',
                    required=True,
                    default=None)

parser.add_argument('--port', dest = 'port',
                    help ='Port to send to',
                    required = True,
                    default = None)

args = parser.parse_args()

viewer_name = args.server
viewer_port = args.port

# defaults is to send to nassella.local:8234
cam_name = socket.gethostname()
print(f'Starting {cam_name}')
viewer_ip = socket.gethostbyname(viewer_name)
viewer_addr = f'tcp://{viewer_ip}:{viewer_port}'
print(f'Sending to {viewer_name} at {viewer_addr}')
viewer = imagezmq.ImageSender(connect_to = f'tcp://{viewer_ip}:{viewer_port}')

jpeg_quality = 100  # 0 to 100, higher is better quality, 95 is cv2 default
while True:  # send images as stream until Ctrl-C
    image = picam.read()
    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    viewer.send_jpg(cam_name, jpg_buffer)

