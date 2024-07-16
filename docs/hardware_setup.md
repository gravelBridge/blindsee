# Hardware Setup for Raspberry Pi 2

## Prerequisites
- Raspberry Pi 2 (with Raspbian or Raspberry Pi OS installed)
- Raspberry Pi Camera Module (CSI interface)
- EEG Sensor (e.g., NeuroSky MindWave) via UART/Serial
- A push-button connected to a GPIO pin (e.g., GPIO 17) and GND
- Speakers or headphones for audio output (3.5mm jack or USB audio device)

## Steps
1. **Camera**:  
   - Enable camera in `raspi-config` if needed.  
   - Connect the camera ribbon cable carefully to the Pi’s camera port.
   
2. **EEG Sensor**:  
   - Connect EEG's TX to Pi’s RX (e.g., GPIO 15 for UART RX).
   - Connect Ground to Ground.
   - If needed, level shift signals to 3.3V. Check EEG device specs.
   - Ensure `enable_uart=1` in `/boot/config.txt`.

3. **Button**:  
   - Connect a momentary push button between GPIO pin (e.g., GPIO 17) and GND.
   - Internal pull-up will be enabled in software.
   - Use a normally open button for simplicity.

4. **Speakers**:  
   - Connect via 3.5mm jack.
   - Alternatively, use a USB sound card or Bluetooth, but ensure drivers and pairing.

5. **Power**:  
   - Use a stable 5V power supply capable of delivering sufficient current for the Pi, camera, and peripherals.
   
6. **Network & API Keys**:  
   - Ensure the Pi has internet access (Wi-Fi or Ethernet).
   - Set `OPENAI_API_KEY` environment variable before running the software:
     ```bash
     export OPENAI_API_KEY="sk-..."
     ```

## Additional Tips
- Check `developer_guide.md` for instructions on code structure and customization.
- Consider using a small portable battery pack if building wearable glasses.
- For best EEG performance, minimize electrical noise and ensure a good sensor-skin contact.
