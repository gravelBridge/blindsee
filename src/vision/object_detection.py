from ..utils.logger import Logger
from .model import ObjectDetectionModel
from ..config.config import Config
from typing import List, Tuple
import numpy as np

class ObjectDetector:
    """
    Wraps around ObjectDetectionModel to provide additional logic:
    - Retrieves detected objects
    - Checks if any object is too close to the user based on bounding box area.
    """

    def __init__(self):
        self.logger = Logger("ObjectDetector")
        self.model = ObjectDetectionModel()

    def detect_objects(self, frame: np.ndarray) -> List[Tuple[str, float, List[float]]]:
        """
        Detects objects in the given frame using the loaded TFLite model.
        Returns a list of (label, score, [ymin,xmin,ymax,xmax]) normalized between 0 and 1.
        """
        if frame is None:
            self.logger.warn("No frame provided to detect_objects, returning empty list.")
            return []
        return self.model.predict(frame)

    def is_object_too_close(self, frame: np.ndarray, objects: List[Tuple[str, float, List[float]]]) -> bool:
        """
        Determines if any detected object occupies a large fraction of the frame.
        This indicates the object is very close.

        OBJECT_CLOSE_THRESHOLD defines how large the bounding box area can be relative to frame area.
        If any object exceeds this threshold, return True.
        """
        if frame is None or len(objects) == 0:
            return False

        h, w, _ = frame.shape
        frame_area = h * w

        for (label, score, box) in objects:
            ymin, xmin, ymax, xmax = box
            # Convert normalized coordinates to actual pixels if needed
            # box_area in normalized form * frame_area
            box_area = (ymax - ymin) * (xmax - xmin) * frame_area
            if box_area > Config.OBJECT_CLOSE_THRESHOLD * frame_area:
                self.logger.debug(f"Object '{label}' too close, box area fraction: {box_area/frame_area:.2f}")
                return True
        return False
