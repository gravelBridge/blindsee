import serial
from .eeg_processor import EEGProcessor
from ..config.config import Config
from ..utils.logger import Logger
from typing import Optional, Dict

class EEGReader:
    """
    Continuously reads EEG data from the specified serial port.
    Expects data packets in a specific format (from devices like NeuroSky MindWave).

    Methods:
        read_data_blocking() -> Optional[Dict[str, float]]:
            Blocks until a valid EEG data packet is received and returns processed EEG metrics.
    """

    def __init__(self):
        self.logger = Logger("EEGReader")
        try:
            self.ser = serial.Serial(Config.EEG_SERIAL_PORT, Config.EEG_BAUD_RATE)
            self.logger.info(f"EEG serial connection opened on {Config.EEG_SERIAL_PORT} at {Config.EEG_BAUD_RATE} baud.")
        except Exception as e:
            self.logger.error(f"Failed to open EEG serial port: {e}")
            self.ser = None
        self.processor = EEGProcessor()

    def read_data_blocking(self) -> Optional[Dict[str, float]]:
        """
        Reads EEG data packets in a blocking manner until a valid packet is found.
        Returns a dictionary of EEG metrics like attention, meditation, and band powers.
        If KeyboardInterrupt is raised, returns None.
        """
        if not self.ser:
            self.logger.warn("No serial port available for EEG reading.")
            return None

        try:
            while True:
                data = self.ser.read(1)
                if not data:
                    continue

                if data[0] == 0xaa:  # Start of a packet
                    data2 = self.ser.read(1)
                    if data2 and data2[0] == 0xaa:
                        # Possible payload
                        data3 = self.ser.read(1)
                        if not data3:
                            continue

                        if data3[0] == 0x04:
                            # Poor signal quality packet
                            data4 = self.ser.read(5)
                            if data4 and len(data4) == 5 and data4[0] == 0x80 and data4[1] == 0x02:
                                # just ignore these, or could store poor signal info
                                high = data4[2]
                                low = data4[3]
                                checkSum = data4[4]
                                s = ((0x80 + 0x02 + high + low) ^ 0xffffffff) & 0xff
                                if s != checkSum:
                                    self.logger.warn("Checksum failed for poor signal data. Data may be noisy.")
                                # No return here, just continue reading.

                        elif data3[0] == 0x20:
                            # Big data packet with EEG values
                            data5 = self.ser.read(33)
                            if data5 and len(data5) == 33 and data5[0] == 0x02 and data5[2] == 0x83 and data5[3] == 0x18:
                                if data5[30] == 0x05:
                                    meditation = data5[31]
                                    if data5[28] == 0x04:
                                        attention = data5[29]

                                        # Extract band powers
                                        delta = (data5[4] << 16) | (data5[5] << 8) | data5[6]
                                        theta = (data5[7] << 16) | (data5[8] << 8) | data5[9]
                                        lowalpha = (data5[10] << 16) | (data5[11] << 8) | data5[12]
                                        highalpha = (data5[13] << 16) | (data5[14] << 8) | data5[15]
                                        lowbeta = (data5[16] << 16) | (data5[17] << 8) | data5[18]
                                        highbeta = (data5[19] << 16) | (data5[20] << 8) | data5[21]
                                        lowgamma = (data5[22] << 16) | (data5[23] << 8) | data5[24]
                                        middlegamma = (data5[25] << 16) | (data5[26] << 8) | data5[27]

                                        eeg_data = self.processor.process_eeg_data(
                                            signal_quality=data5[1],
                                            attention=attention,
                                            meditation=meditation,
                                            delta=delta,
                                            theta=theta,
                                            lowalpha=lowalpha,
                                            highalpha=highalpha,
                                            lowbeta=lowbeta,
                                            highbeta=highbeta,
                                            lowgamma=lowgamma,
                                            middlegamma=middlegamma
                                        )
                                        return eeg_data
                                    else:
                                        self.logger.warn(f"Unexpected attention byte. Got {data5[28]} instead of 0x04.")
                                else:
                                    self.logger.warn(f"Unexpected meditation byte. Got {data5[30]} instead of 0x05.")
                            else:
                                self.logger.warn("Invalid big EEG data packet format.")
                        else:
                            self.logger.warn(f"Unexpected data byte in EEG packet: {data3[0]}")
        except KeyboardInterrupt:
            if self.ser:
                self.ser.close()
            self.logger.info("EEG reading interrupted by user.")
            return None
        except Exception as ex:
            self.logger.error(f"Unexpected error reading EEG: {ex}")
            return None
