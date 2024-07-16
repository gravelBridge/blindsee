from ..utils.logger import Logger
from typing import Dict

class EEGProcessor:
    """
    Processes raw EEG values into a structured dictionary.
    Currently just passes them through, but could be extended for:
    - Filtering noise
    - Running FFT or other signal processing
    - Detecting complex emotional or cognitive states
    """

    def __init__(self):
        self.logger = Logger("EEGProcessor")

    def process_eeg_data(self,
                         signal_quality: int,
                         attention: int,
                         meditation: int,
                         delta: int,
                         theta: int,
                         lowalpha: int,
                         highalpha: int,
                         lowbeta: int,
                         highbeta: int,
                         lowgamma: int,
                         middlegamma: int) -> Dict[str, float]:
        """
        Convert raw EEG data into a dictionary for easier interpretation.
        Adds logging and could apply scaling or normalization if needed.
        """
        self.logger.debug(
            f"EEG Data -> signal {signal_quality}, attention: {attention}, meditation: {meditation}, "
            f"delta: {delta}, theta: {theta}, lowalpha: {lowalpha}, highalpha: {highalpha}, "
            f"lowbeta: {lowbeta}, highbeta: {highbeta}, lowgamma: {lowgamma}, middlegamma: {middlegamma}"
        )

        # Potential expansions: scaling these values, normalizing them, or computing derived metrics.
        # For now, just return as-is:
        return {
            "signal_quality": float(signal_quality),
            "attention": float(attention),
            "meditation": float(meditation),
            "delta": float(delta),
            "theta": float(theta),
            "lowalpha": float(lowalpha),
            "highalpha": float(highalpha),
            "lowbeta": float(lowbeta),
            "highbeta": float(highbeta),
            "lowgamma": float(lowgamma),
            "middlegamma": float(middlegamma)
        }
