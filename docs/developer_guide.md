# Developer Guide

## Code Structure Overview

- **`src/main.py`**:  
  Main application loop orchestrating EEG input, vision analysis, TTS output, and user button input.

- **`src/config/config.py`**:  
  Centralized configuration. Adjust parameters such as camera resolution, EEG thresholds, object detection confidence, and API keys.

- **`src/eeg`**:  
  - `eeg_reader.py`: Reads raw EEG data from the serial port, parses packets, and extracts attention/meditation levels and brainwave bands.
  - `eeg_processor.py`: Processes the raw EEG data into a structured format and could be extended for more advanced analysis.

- **`src/vision`**:
  - `camera.py`: Manages camera capture.
  - `model.py`: Uses a TFLite model for local object detection.
  - `object_detection.py`: Wraps detection logic and includes helper methods like checking if objects are too close.
  - `openai_vision.py`: Integrates with GPT-4o for scene interpretation and structured responses.

- **`src/ai`**:
  - `emotion_analysis.py`: Determines if the user is in distress based on EEG data.
  - `reassuring_messages.py`: Fetches a reassuring message from GPT-4o when user is distressed.

- **`src/audio/tts.py`**:
  Text-to-Speech integration using `pyttsx3`. Provides audible feedback.

- **`src/gpio/button.py`**:
  Manages GPIO input from a physical button, debouncing logic, and triggers certain actions in the main loop.

- **`src/utils`**:
  - `logger.py`: Centralized logging.
  - `signal_handler.py`: Graceful shutdown on SIGINT/SIGTERM.

## Extending the System

### Adding New Object Detection Models
- Replace the model file in `models/object_detection/`.
- Update `MODEL_PATH` and `LABELS_PATH` in `config.py` if needed.
- Adjust `MIN_CONFIDENCE` to suit your model’s performance.

### Integrating New Sensors
- Add new modules under `src/` (e.g., `src/sensors/`).
- Modify `main.py` to incorporate additional sensors into the logic flow.

### Changing GPT-4o Behavior
- Modify prompts in `reassuring_messages.py` or `openai_vision.py` to change how the model responds.
- Adjust `OPENAI_MODEL` in `config.py` to use different GPT-4o model variants or new future models.

## Performance Considerations
- **Object Detection**: Tweak resolution or use hardware acceleration if available.
- **EEG Processing**: If latency is an issue, consider running EEG reading in a separate thread or process.
- **Caching**: If certain responses from GPT-4o are repetitive, implement caching logic.

## Safety and Reliability
- Always test hardware connections carefully.
- Implement retries and fallback logic for network errors.
- Consider adding exception handling for OpenAI API calls in `openai_vision.py` and `reassuring_messages.py`.

## Debugging and Logging
- Use `logger.py` and check stderr for detailed logs.
- Enable more verbose logging in `logger.py` or add debug prints in `main.py`.