# User Manual

## How to Use
1. **Startup**: Turn on the Raspberry Pi 2. After it boots, ensure your OPENAI_API_KEY is set:
```bash
   export OPENAI_API_KEY="sk-..."
```
   Then run:
```bash
   python3 src/main.py
```

2. **Wearing the Glasses**: Put on the glasses so the camera faces forward. Place the EEG sensor on your head as instructed by its manufacturer. Use headphones or speakers to hear audio feedback.

3. **Button Press**: Press the button once to immediately get a spoken description of your surroundings. This snapshot request is sent to GPT-4o, which returns a summary of the scene and objects present.

4. **Periodic Updates**: Without pressing the button, the system periodically narrates what it sees. This includes detecting objects and warning you if something is too close.

5. **Distress Alerts**: If the system detects you are distressed (based on your EEG readings), it will pause normal narrations and use GPT-4o to provide a reassuring, personalized message. It sends the current scene image along with a request for a comforting and context-aware message, ensuring the reassurance is relevant to what the camera sees around you.

## Interpreting Feedback
- Object Announcements: “I see: a chair, a table” means the system recognized these objects.
- Close Object Warnings: “Warning: Something is too close!” means you should stop moving and be cautious.
- Distress Reassurance: If you hear a gentle, encouraging message like “Everything will be okay. I see a calm environment around you,” it means you seemed distressed and the system is trying to reassure you based on the current scene.

## Troubleshooting
- No Audio: Check the volume settings, ensure headphones or speakers are connected, and verify pyttsx3 is installed correctly.
- No Description Given: Ensure OPENAI_API_KEY is set and the Pi has an internet connection. Check logs for errors.
- EEG Not Working: Confirm that the EEG sensor is connected properly and that the serial port is not in use by another process.
- Camera Issues: Ensure the camera is enabled and connected. Try vcgencmd get_camera to verify camera support.

## Advanced Adjustments
- Change Intervals or Thresholds: Edit src/config/config.py to adjust narration intervals, EEG thresholds, or object detection confidence levels.
- Modify GPT-4o Behavior: Change the prompts in src/ai/reassuring_messages.py or src/vision/openai_vision.py to alter how GPT-4o describes scenes or provides reassurance.
- Add New Hardware: Refer to developer_guide.md to integrate new sensors or modify the system’s capabilities.
