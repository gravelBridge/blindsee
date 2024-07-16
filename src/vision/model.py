import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
from ..config.config import Config
from ..utils.logger import Logger
from typing import List, Tuple

class ObjectDetectionModel:
    """
    Loads a TFLite object detection model and performs inference on a frame.
    Uses the model specified in Config.MODEL_PATH and Config.LABELS_PATH.

    Methods:
        predict(frame: np.ndarray) -> List[Tuple[str, float, List[float]]]:
            Returns a list of (label, score, bbox) for detected objects.
    """

    def __init__(self):
        self.logger = Logger("ObjectDetectionModel")
        try:
            self.interpreter = tflite.Interpreter(model_path=Config.MODEL_PATH)
            self.interpreter.allocate_tensors()
        except Exception as e:
            self.logger.error(f"Failed to load TFLite model: {e}")
            raise

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.labels = self.load_labels(Config.LABELS_PATH)
        self.logger.info("Object detection model loaded successfully.")

    def load_labels(self, label_path: str) -> List[str]:
        self.logger.debug(f"Loading labels from: {label_path}")
        try:
            with open(label_path, 'r') as f:
                labels = [line.strip() for line in f.readlines() if line.strip()]
            self.logger.debug(f"Loaded {len(labels)} labels.")
            return labels
        except FileNotFoundError:
            self.logger.warn("Label file not found, using empty label list.")
            return []
        except Exception as e:
            self.logger.error(f"Error loading labels: {e}")
            return []

    def predict(self, frame: np.ndarray) -> List[Tuple[str, float, List[float]]]:
        """
        Perform object detection on the provided frame.
        Returns: [(label, score, [ymin, xmin, ymax, xmax]), ...]
        Coordinates are normalized between 0 and 1.
        """
        if frame is None:
            self.logger.warn("Received empty frame for prediction.")
            return []

        input_shape = self.input_details[0]['shape']
        height, width = input_shape[1], input_shape[2]

        # Resize frame to model input size
        frame_resized = cv2.resize(frame, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0).astype('uint8')

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        try:
            self.interpreter.invoke()
        except Exception as e:
            self.logger.error(f"Model inference failed: {e}")
            return []

        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

        results = []
        for i, score in enumerate(scores):
            if score > Config.MIN_CONFIDENCE:
                class_id = int(classes[i])
                label = self.labels[class_id] if class_id < len(self.labels) else "Unknown"
                box = boxes[i].tolist()
                results.append((label, float(score), box))

        self.logger.debug(f"Detected {len(results)} objects above confidence {Config.MIN_CONFIDENCE}.")
        return results
