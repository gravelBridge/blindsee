import openai
from ..config.config import Config
from ..utils.logger import Logger
import time
import cv2
import base64

class ReassuringMessages:
    """
    Generates a gentle and encouraging message when the user is distressed.
    Integrates with GPT-4o, retries on failure.
    Now also sends the current scene image from the camera to GPT-4o,
    so the reassuring message can reference the actual environment.
    """

    def __init__(self):
        self.logger = Logger("ReassuringMessages")
        openai.api_key = Config.OPENAI_API_KEY
        self.max_retries = 3
        self.retry_delay = 2.0

    def encode_image(self, frame):
        """
        Encodes the given frame as a base64 JPEG.
        If encoding fails, returns an empty string.
        """
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            self.logger.warn("Failed to encode frame for reassurance message. Returning empty image data.")
            return ""
        return base64.b64encode(buffer).decode('utf-8')

    def generate_message(self, frame) -> str:
        """
        Fetches a reassuring message from GPT-4o, referencing the scene in the image.
        If fails after multiple retries, returns a fallback message.

        The prompt includes the scene image to allow GPT-4o to tailor the reassurance.
        """
        image_data = self.encode_image(frame)
        if not image_data:
            # If no image data, fallback to a non-scene-based reassurance
            self.logger.warn("No image data for reassuring message, proceeding without scene context.")
            return self._fetch_reassurance_without_image()

        prompt = [
            {
                "role": "system",
                "content": (
                    "You are a reassuring assistant that comforts the user in distress. "
                    "You have access to a single image representing the user's current environment. "
                    "You should provide a calm, gentle, and encouraging message that references the environment "
                    "in a subtle way to help the user feel safe and relaxed."
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "I'm feeling anxious. Please reassure me."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}",
                            "detail": Config.OPENAI_VISION_DETAIL
                        }
                    }
                ]
            }
        ]

        for attempt in range(self.max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=Config.OPENAI_MODEL,
                    messages=prompt,
                    max_tokens=100,
                    temperature=0.7,
                    top_p=1.0
                )
                message = response.choices[0].message.content.strip()
                self.logger.debug(f"Personalized reassuring message retrieved: {message}")
                return message
            except openai.error.OpenAIError as e:
                self.logger.warn(f"OpenAI API error while fetching personalized reassuring message (attempt {attempt+1}): {e}")
                time.sleep(self.retry_delay)
            except Exception as ex:
                self.logger.error(f"Unexpected error fetching personalized reassuring message: {ex}")
                time.sleep(self.retry_delay)

        self.logger.error("Max retries exceeded while fetching personalized reassuring message, returning a default fallback.")
        return "Please try to stay calm. Everything will be okay. I see a safe environment around you."

    def _fetch_reassurance_without_image(self) -> str:
        """
        Fallback method if no image data is available, similar to the previous logic but without image context.
        """
        prompt = [
            {
                "role": "system",
                "content": "You are a reassuring assistant that comforts the user in distress, speaks softly and kindly."
            },
            {
                "role": "user",
                "content": "Please provide a calm, gentle and encouraging message to help me feel safe and relaxed."
            }
        ]

        for attempt in range(self.max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=Config.OPENAI_MODEL,
                    messages=prompt,
                    max_tokens=100,
                    temperature=0.7,
                    top_p=1.0
                )
                message = response.choices[0].message.content.strip()
                self.logger.debug(f"Reassuring message (no image): {message}")
                return message
            except openai.error.OpenAIError as e:
                self.logger.warn(f"OpenAI API error while fetching reassurance (no image) (attempt {attempt+1}): {e}")
                time.sleep(self.retry_delay)
            except Exception as ex:
                self.logger.error(f"Unexpected error fetching reassurance without image: {ex}")
                time.sleep(self.retry_delay)

        self.logger.error("Max retries exceeded while fetching reassurance without image, returning a default fallback.")
        return "Try to remain calm. Everything will be alright."