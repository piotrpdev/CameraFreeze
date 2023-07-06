# Based on the pyvirtualcam 'webcam_filter' example with slight changes https://github.com/letmaik/pyvirtualcam

import argparse
import signal
import sys
import threading
import keyboard
import time
import logging
import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--camera", type=int, default=1, help="ID of real webcam device (default: 1)")
parser.add_argument("-x", "--width", type=int, default=1280, help="Preferred width for both cameras (default: 1280)")
parser.add_argument("-y", "--height", type=int, default=720, help="Preferred height for both cameras (default: 720)")
parser.add_argument("-fi", "--fps-in", type=int, default=30, help="Preferred FPS in for real camera (default: 30)")
parser.add_argument("-fo", "--fps-out", type=int, default=30, help="FPS out for virtual camera (default: 30)")
parser.add_argument("-pk", "--pause-key", default="#", help="Key used to pause the virtual camera (default: #)")
args = parser.parse_args()

alive = True
pause = False

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def start_camera():
    # Set up webcam capture.
    vc = cv2.VideoCapture(args.camera)

    if not vc.isOpened():
        logging.error('Could not open video source')
        exit_safely(None, None)
        return

    pref_width = args.width
    pref_height = args.height
    pref_fps_in = args.fps_in
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
    vc.set(cv2.CAP_PROP_FPS, pref_fps_in)

    # Query final capture device values (may be different from preferred settings).
    width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_in = vc.get(cv2.CAP_PROP_FPS)

    logging.info(f'Webcam capture started: ID: {args.camera} ({width}x{height} @ {fps_in}fps)')

    with pyvirtualcam.Camera(width, height, args.fps_out, fmt=PixelFormat.BGR) as cam:
        logging.info(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')

        ret, frame = None, None

        while alive:
            # Read frame from webcam.
            ret, frame = vc.read()
            if not ret:
                raise RuntimeError('Error fetching frame')

            # Send to virtual cam.
            if not pause:
                cam.send(frame)

            # Wait until it's time for the next frame.
            cam.sleep_until_next_frame()


def listen_for_key():
    while alive:
        try:
            if keyboard.is_pressed(args.pause_key):
                global pause
                pause = not pause
                logging.info('Camera {}'.format('paused' if pause else 'un-paused'))
                time.sleep(0.3)
        except:
            logging.error("Something went wrong with the key listener")


camera_thread = threading.Thread(target=start_camera)
key_thread = threading.Thread(target=listen_for_key)


def exit_safely(signal, frame):
    global alive

    logging.info('Shutting down')
    alive = False

    time.sleep(0.3)

    sys.exit(0)


if __name__ == '__main__':
    # https://www.pythontutorial.net/python-concurrency/python-threading/
    # https://webcamtests.com/viewer
    signal.signal(signal.SIGINT, exit_safely)

    camera_thread.start()
    key_thread.start()

    camera_thread.join()
    key_thread.join()
