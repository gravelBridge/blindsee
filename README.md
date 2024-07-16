# BlindSee: Assistive Vision Glasses for the Visually Impaired on Raspberry Pi 2

**BlindSee** is a comprehensive solution for wearable assistive glasses designed to aid visually impaired individuals. We integrate multiple components such as EEG-based emotion detection, computer vision for obstacle and scene understanding, AI-driven descriptive audio feedback, and a physical button interface for user control.

By leveraging OpenAI's GPT-4o for scene understanding and reassurance, local object detection with a TFLite model, and EEG-based emotional state analysis, BlindSee aims to provide users with contextual, real-time assistance.

This code accompanies the technical report available [here](https://drive.google.com/file/d/1bWftReNevNqUjvrPQpjiQFK0YzpWFYly/view).

## Key Features

- **EEG Integration:**  
  BlindSee reads EEG signals from a sensor (e.g., NeuroSky MindWave) connected to the Raspberry Pi’s serial interface.  
  - Detects attention and meditation levels.  
  - Identifies distress states (low attention and meditation) and provides comforting messages.

- **Computer Vision:**  
  Utilizes a camera module on the Raspberry Pi 2 to:  
  - Recognize objects and detect if any are too close.  
  - Periodically narrate the surroundings.  
  - On button press, queries GPT-4o for a detailed scene description.

- **GPT-4o Assistance:**  
  GPT-4o provides AI-driven scene understanding and reassurance:  
  - On-demand scene description when the user presses a button.  
  - Personalized reassuring messages when user appears distressed, factoring in real-time camera imagery.

- **Audio Feedback (TTS):**  
  Uses pyttsx3 for text-to-speech, allowing audible narration of detected objects, obstacles, and reassuring messages.

- **Simple User Interaction (Button):**  
  A single button press triggers immediate scene analysis and narration.  
  No complex UI is needed, just a tactile button for easy user input.

## Hardware Assumptions

- **Raspberry Pi 2** (running a compatible Linux distro).
- **Raspberry Pi Camera Module** connected to CSI camera port.
- **EEG Sensor** via UART pins (e.g., GPIO 15 for RX).
- **Button** connected to a GPIO pin (e.g., GPIO 17) and ground, using internal pull-ups.
- **Speakers or Headphones** for audio output from the Pi’s audio jack.

## Software Components

- **Vision**:  
  - Local object detection with a TFLite model (e.g., SSD MobileNet v2).
  - GPT-4o scene analysis returning structured JSON with object descriptions.
- **EEG**:  
  - Reads raw EEG packets, extracts attention/meditation.
  - Identifies distress states if both attention and meditation are below certain thresholds.
- **AI Integration**:  
  - GPT-4o for scene analysis on-demand and for generating reassuring messages.
  - Reassurance prompts include the current camera frame as context.
- **Audio (TTS)**:  
  - pyttsx3 for local text-to-speech processing.
  - Narrates objects, warnings, and reassuring messages.

## Getting Started

1. **Set Environment Variables**:  
   Before running, ensure you have an OpenAI API key:  
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

2. **Install Dependencies**:  
   On Raspberry Pi:  
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip python3-opencv libatlas-base-dev espeak
   pip3 install -r requirements.txt
   ```

3. **Run the Application**:  
   ```bash
   python3 src/main.py
   ```

4. **Wear and Operate**:  
   - Put on the glasses with the camera facing forward.  
   - Wear EEG sensor as directed by its manufacturer.  
   - Listen via headphones or speakers.  
   - Press the button to trigger GPT-4o scene narration.

## Usage Details

- **Periodic Narration**: The system automatically narrates surroundings at intervals defined in `config.py` (`NARRATION_INTERVAL`). If attention is low, intervals lengthen to reduce cognitive load.
- **Button Press**: Immediately triggers GPT-4o scene analysis and narration, even outside the normal interval schedule.
- **Distress Detection**: If the user’s EEG readings indicate distress, BlindSee asks GPT-4o for a gentle, encouraging message referencing the camera’s current view. The user hears a calm message describing something in the environment to reassure them.
- **Object Proximity Warning**: If any detected object’s bounding box is large enough (relative to the frame) to suggest closeness, BlindSee speaks a warning: “Warning: Something is too close!”

## Configuration

Edit `src/config/config.py` to adjust parameters:
- Camera resolution, framerate, and port.
- EEG thresholds for attention, meditation, and distress detection.
- OpenAI model and detail settings.
- Object detection confidence and “too close” threshold.
- GPIO pin assignments for the button.

## Advanced Features

- **Customization of GPT-4o Messages**:  
  Modify prompts in `src/ai/reassuring_messages.py` or `src/vision/openai_vision.py` to change scene or reassurance styles.
  
- **Change TTS Voice/Rate**:  
  In `src/audio/tts.py`, configure pyttsx3 voices or rates for more personalized audio feedback.

- **Switch Object Detection Models**:  
  Replace the TFLite model in `models/object_detection/` and update paths in `config.py`.

## Logging and Debugging

- All logs are printed to stderr with timestamps and module names.
- Check logs for clues if no audio is played, no objects are recognized, or GPT-4o fails to respond.
- Increase verbosity by adding more `debug` calls in `logger.py` or main code.

## Safety and Reliability

- Always ensure stable power and proper wiring for EEG sensor and button.
- Use a camera that is compatible and enabled via `raspi-config`.
- Handle exceptions from GPT-4o (network issues or refusals) gracefully with retries (implemented in code).

## Future Directions

- **Multi-Modal Emotion Analysis**: Integrate more EEG band interpretations, heart rate sensors, or other biometrics.
- **Advanced Scene Understanding**: Use more sophisticated object detection models or integrate depth sensors.
- **Localization & Navigation**: Add GPS or indoor localization to offer navigation instructions.
- **Voice Commands**: Extend input interface beyond a button, adding voice commands recognized by another model.

## Community and Contributions

- This is a research-oriented prototype. Contributions, bug reports, and improvements are welcome.
- Consider adding tests under `tests/` or refining hardware integration steps in `docs/`.

## Related Documentation

- **User Manual**: `docs/user_manual.md`
- **Hardware Setup**: `docs/hardware_setup.md`
- **Developer Guide**: `docs/developer_guide.md`

## Contact

For inquiries or support, contact the authors or contributors listed in `setup.py` or open an issue in the repository.

## Disclaimer

This is a prototype system. While it strives to aid visually impaired users, it may not be fully reliable in all environments. Always ensure a safe environment and do not rely solely on BlindSee for navigation or safety.
