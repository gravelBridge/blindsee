import os

class Config:
    """
    Config class holds all system configuration parameters.
    These can be adjusted to tune the performance, thresholds, and behavior.
    Environment variables and file paths are resolved here.
    """

    # EEG settings
    EEG_SERIAL_PORT = os.getenv("EEG_SERIAL_PORT", "/dev/serial0")
    EEG_BAUD_RATE = int(os.getenv("EEG_BAUD_RATE", "57600"))

    # Camera settings
    CAMERA_WIDTH = int(os.getenv("CAMERA_WIDTH", "640"))
    CAMERA_HEIGHT = int(os.getenv("CAMERA_HEIGHT", "480"))
    CAMERA_FRAMERATE = int(os.getenv("CAMERA_FRAMERATE", "30"))

    # Model settings for local object detection
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../models/object_detection/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
    LABELS_PATH = os.path.join(os.path.dirname(__file__), "../../models/object_detection/labels.txt")
    MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.5"))

    # Audio settings
    VOICE_RATE = int(os.getenv("VOICE_RATE", "150"))
    VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))

    # EEG thresholds for attention and meditation
    ATTENTION_THRESHOLD = int(os.getenv("ATTENTION_THRESHOLD", "30"))
    MEDITATION_THRESHOLD = int(os.getenv("MEDITATION_THRESHOLD", "30"))

    # Emotional state thresholds
    DISTRESS_ATTENTION_THRESHOLD = int(os.getenv("DISTRESS_ATTENTION_THRESHOLD", "20"))
    DISTRESS_MEDITATION_THRESHOLD = int(os.getenv("DISTRESS_MEDITATION_THRESHOLD", "20"))

    # OpenAI API Key and model settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise EnvironmentError("Please set OPENAI_API_KEY env variable.")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
    OPENAI_VISION_DETAIL = os.getenv("OPENAI_VISION_DETAIL", "high")

    # Interval between automatic narrations in seconds
    NARRATION_INTERVAL = int(os.getenv("NARRATION_INTERVAL", "10"))

    # GPIO pin for button input
    BUTTON_GPIO_PIN = int(os.getenv("BUTTON_GPIO_PIN", "17"))
    BUTTON_DEBOUNCE_TIME = int(os.getenv("BUTTON_DEBOUNCE_TIME", "200"))  # ms

    # Threshold for considering an object "too close"
    OBJECT_CLOSE_THRESHOLD = float(os.getenv("OBJECT_CLOSE_THRESHOLD", "0.1"))
