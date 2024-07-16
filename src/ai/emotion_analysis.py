from typing import Dict

class EmotionAnalysis:
    """
    Analyzes EEG data to determine if the user is distressed.
    Future expansions could include more complex emotional states,
    or integrating multiple EEG features over time.

    Current logic: If attention < DISTRESS_ATTENTION_THRESHOLD and
    meditation < DISTRESS_MEDITATION_THRESHOLD, user is considered distressed.
    """

    @staticmethod
    def is_user_distressed(eeg_data: Dict[str, float], distress_attention_threshold: int, distress_meditation_threshold: int) -> bool:
        attention = eeg_data.get('attention', 50)
        meditation = eeg_data.get('meditation', 50)
        # Potential future expansion:
        # Could integrate delta/theta/alpha/beta/gamma ratios to detect stress patterns.
        return (attention < distress_attention_threshold) and (meditation < distress_meditation_threshold)
