import cv2
from ..config.config import Config
from ..utils.logger import Logger
from typing import Optional

class Camera:
    """
    Handles camera initialization and frame retrieval using OpenCV VideoCapture.
    Assumes a standard USB camera or Raspberry Pi camera module is available as /dev/video0.
    """

    def __init__(self):
        self.logger = Logger("Camera")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.logger.error("Failed to open camera. Check if camera is connected and enabled.")
        else:
            self.logger.info("Camera opened successfully.")

        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, Config.CAMERA_FRAMERATE)
        self.logger.debug(f"Camera configured: {Config.CAMERA_WIDTH}x{Config.CAMERA_HEIGHT}@{Config.CAMERA_FRAMERATE}fps")

    def get_frame(self) -> Optional[cv2.Mat]:
        """
        Captures a frame from the camera. If unsuccessful, returns None.
        """
        ret, frame = self.cap.read()
        if not ret:
            self.logger.warn("Failed to read frame from camera. Retrying next cycle.")
            return None
        return frame

    def release(self):
        """
        Releases the camera resource.
        """
        if self.cap:
            self.cap.release()
            self.logger.info("Camera released.")
