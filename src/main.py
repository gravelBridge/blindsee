import time
import threading
from vision.camera import Camera
from vision.object_detection import ObjectDetector
from vision.openai_vision import OpenAIVision
from audio.tts import TextToSpeech
from eeg.eeg_reader import EEGReader
from utils.signal_handler import GracefulKiller
from utils.logger import Logger
from config.config import Config
from gpio.button import Button
from ai.emotion_analysis import EmotionAnalysis
from ai.reassuring_messages import ReassuringMessages
from typing import Dict

def eeg_loop(eeg_reader: EEGReader, shared_state: Dict):
    """
    Runs in a separate thread. Continuously reads EEG data and updates shared_state.
    """
    while not shared_state['killer'].kill_now:
        eeg_data = eeg_reader.read_data_blocking()
        if eeg_data:
            shared_state['eeg_data'] = eeg_data
        time.sleep(0.1)

def button_callback():
    """
    Callback triggered by a button press event.
    Sets a flag in shared_state for the main loop to process.
    """
    shared_state['button_pressed'] = True

logger = Logger("Main")

if __name__ == "__main__":
    # Initialize system components
    killer = GracefulKiller()
    shared_state = {
        'killer': killer,
        'eeg_data': None,
        'button_pressed': False
    }

    camera = Camera()
    detector = ObjectDetector()
    tts = TextToSpeech()
    eeg_reader = EEGReader()
    vision_ai = OpenAIVision()
    re_msgs = ReassuringMessages()

    # Start EEG reading thread
    eeg_thread = threading.Thread(target=eeg_loop, args=(eeg_reader, shared_state), daemon=True)
    eeg_thread.start()

    # Setup button
    button = Button()
    button.set_callback(button_callback)

    last_speak_time = time.time()

    # Main loop
    try:
        while not killer.kill_now:
            frame = camera.get_frame()
            if frame is None:
                # If frame is not available, just wait and try again
                time.sleep(0.1)
                continue

            eeg_data = shared_state.get('eeg_data', {})
            attention = eeg_data.get('attention', 50.0)
            meditation = eeg_data.get('meditation', 50.0)

            # Adjust narration interval based on attention
            if attention < Config.ATTENTION_THRESHOLD:
                attention_based_interval = Config.NARRATION_INTERVAL * 2
            else:
                attention_based_interval = Config.NARRATION_INTERVAL

            # Check if user is distressed
            distressed = EmotionAnalysis.is_user_distressed(
                eeg_data,
                Config.DISTRESS_ATTENTION_THRESHOLD,
                Config.DISTRESS_MEDITATION_THRESHOLD
            )

            if distressed:
                # Provide a personalized reassuring message that references the current scene
                reassure_msg = re_msgs.generate_message(frame)
                tts.speak(reassure_msg)

            # If the button was pressed, perform a scene analysis via GPT-4o
            if shared_state['button_pressed']:
                shared_state['button_pressed'] = False
                vision_result = vision_ai.analyze_frame(frame)
                if vision_result:
                    summary = vision_result.summary
                    if vision_result.contains_people:
                        summary += " There are people around."
                    else:
                        summary += " I don't see any people."

                    # Adapt message if attention or meditation is low
                    if attention < Config.ATTENTION_THRESHOLD:
                        summary = "I see some objects. Please stay focused."
                    if meditation < Config.MEDITATION_THRESHOLD:
                        summary += " Try to remain calm."

                    # Check proximity of objects
                    local_objects = detector.detect_objects(frame)
                    if detector.is_object_too_close(frame, local_objects):
                        summary += " Warning: An object is very close!"

                    tts.speak(summary)
                else:
                    tts.speak("I couldn't analyze the surroundings at this moment. Please try again.")

            # Periodic narration if not distressed
            if (time.time() - last_speak_time > attention_based_interval) and not distressed:
                local_objects = detector.detect_objects(frame)
                if local_objects:
                    # Construct a narrative from detected objects
                    object_labels = [obj[0] for obj in local_objects]
                    if len(object_labels) > 0:
                        narrative = "I see: " + ", ".join(object_labels)
                    else:
                        narrative = "I don't see any recognizable objects."

                    # Check closeness
                    if detector.is_object_too_close(frame, local_objects):
                        narrative += ". Warning: Something is too close!"

                    # Adapt narrative based on attention/meditation
                    if attention < Config.ATTENTION_THRESHOLD:
                        narrative = "Some objects detected. Please pay attention."
                    if meditation < Config.MEDITATION_THRESHOLD:
                        narrative += " Try to stay calm."

                    tts.speak(narrative)
                else:
                    # No objects detected
                    tts.speak("I don't see anything particular right now.")

                last_speak_time = time.time()

            # Sleep a bit before next iteration
            time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, shutting down.")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
    finally:
        # Cleanup resources
        button.cleanup()
        camera.release()
        logger.info("System shutting down gracefully.")
