import base64
import cv2
import openai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict, Any
from ..config.config import Config
from ..utils.logger import Logger
import time

class DetectedObject(BaseModel):
    label: str
    description: str

class VisionOutput(BaseModel):
    objects: List[DetectedObject]
    contains_people: bool
    summary: str

class OpenAIVision:
    """
    Integrates with GPT-4o to describe the scene.
    Uses a structured JSON schema to ensure consistent output.
    Includes retry logic and error handling for API calls.
    """

    def __init__(self):
        self.logger = Logger("OpenAIVision")
        openai.api_key = Config.OPENAI_API_KEY
        self.max_retries = 3
        self.retry_delay = 2.0

    def encode_image(self, frame) -> str:
        """
        Encodes the image frame to base64 for sending to GPT-4o.
        """
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            self.logger.warn("Failed to encode frame to JPEG, returning empty string.")
            return ""
        return base64.b64encode(buffer).decode('utf-8')

    def analyze_frame(self, frame) -> Optional[VisionOutput]:
        """
        Sends image to GPT-4o and requests a structured response.
        Returns VisionOutput object or None if failed.
        """
        if frame is None:
            self.logger.warn("No frame provided to analyze_frame.")
            return None

        image_b64 = self.encode_image(frame)
        if not image_b64:
            self.logger.warn("Empty image data, cannot analyze.")
            return None

        user_message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the contents of this image and identify if there are any people. Provide a list of objects, a boolean if people are present, and a short summary."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}",
                            "detail": Config.OPENAI_VISION_DETAIL
                        }
                    }
                ]
            }
        ]

        schema = {
          "type": "object",
          "properties": {
            "objects": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "label": {"type": "string"},
                  "description": {"type": "string"}
                },
                "required": ["label", "description"],
                "additionalProperties": False
              }
            },
            "contains_people": {"type": "boolean"},
            "summary": {"type": "string"}
          },
          "required": ["objects", "contains_people", "summary"],
          "additionalProperties": False
        }

        for attempt in range(self.max_retries):
            try:
                self.logger.debug("Sending image to GPT-4o.")
                response = openai.ChatCompletion.create(
                    model=Config.OPENAI_MODEL,
                    messages=user_message,
                    max_tokens=500,
                    response_format={"type":"json_schema", "json_schema":{"strict":True,"schema":schema}}
                )

                message = response.choices[0].message
                if message.get("refusal"):
                    self.logger.warn("Model refused the request.")
                    return None

                parsed = message.get("parsed")
                if parsed:
                    try:
                        vision_output = VisionOutput(**parsed)
                        self.logger.debug("Received valid structured output from GPT-4o.")
                        return vision_output
                    except ValidationError as ve:
                        self.logger.error(f"Validation error in VisionOutput: {ve}")
                        return None
                else:
                    self.logger.warn("No parsed structured output returned from GPT-4o.")
                    return None

            except openai.error.OpenAIError as e:
                self.logger.warn(f"OpenAI API error on attempt {attempt+1}/{self.max_retries}: {e}")
                time.sleep(self.retry_delay)
            except Exception as ex:
                self.logger.error(f"Unexpected error calling GPT-4o: {ex}")
                time.sleep(self.retry_delay)

        self.logger.error("Max retries exceeded for GPT-4o.")
        return None
