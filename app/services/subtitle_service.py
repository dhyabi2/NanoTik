"""
Subtitle Service for generating subtitles from audio
Uses Azure Speech SDK (edge method) for word-level timestamps
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import azure.cognitiveservices.speech as speechsdk

logger = logging.getLogger(__name__)


class SubtitleItem:
    """Represents a single subtitle item with timing"""
    def __init__(self, start: float, end: float, text: str):
        self.start = start
        self.end = end
        self.text = text

    def __repr__(self):
        return f"SubtitleItem({self.start:.2f}s - {self.end:.2f}s: '{self.text}')"


class SubtitleService:
    """Service for generating subtitles from audio files"""

    def __init__(self, speech_config):
        """
        Initialize subtitle service

        Args:
            speech_config: Azure SpeechConfig object
        """
        self.speech_config = speech_config

    def generate_subtitles(self, audio_path: str, language: str = 'en') -> List[SubtitleItem]:
        """
        Generate subtitles from audio file using Azure Speech SDK

        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'zh', 'ar')

        Returns:
            List of SubtitleItem objects with word-level timing
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Map language codes to Azure locale
        language_map = {
            'en': 'en-US',
            'zh': 'zh-CN',
            'ar': 'ar-SA'
        }
        locale = language_map.get(language, 'en-US')

        # Configure speech recognizer
        audio_config = speechsdk.AudioConfig(filename=audio_path)
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_config.subscription_key,
            region=self.speech_config.region
        )
        speech_config.speech_recognition_language = locale
        speech_config.request_word_level_timestamps()

        # Enable detailed results
        speech_config.output_format = speechsdk.OutputFormat.Detailed

        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        subtitles = []

        def handle_final_result(evt):
            """Handle recognized speech with word-level timestamps"""
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                try:
                    import json
                    # Get detailed results with word timings
                    detailed = json.loads(evt.result.json)

                    if 'NBest' in detailed and len(detailed['NBest']) > 0:
                        best = detailed['NBest'][0]

                        if 'Words' in best:
                            # Group words into subtitle chunks (5-7 words per subtitle)
                            words = best['Words']
                            chunk_size = 6

                            for i in range(0, len(words), chunk_size):
                                chunk_words = words[i:i + chunk_size]

                                if chunk_words:
                                    # Convert from ticks (100ns) to seconds
                                    start_time = chunk_words[0]['Offset'] / 10000000
                                    end_time = (chunk_words[-1]['Offset'] + chunk_words[-1]['Duration']) / 10000000
                                    text = ' '.join([w['Word'] for w in chunk_words])

                                    subtitle = SubtitleItem(start_time, end_time, text)
                                    subtitles.append(subtitle)
                                    logger.info(f"Subtitle: {subtitle}")
                except Exception as e:
                    logger.error(f"Error processing word-level timestamps: {e}")
                    # Fallback: create subtitle from full text
                    if evt.result.text:
                        subtitle = SubtitleItem(0, 0, evt.result.text)
                        subtitles.append(subtitle)

        # Connect callbacks
        recognizer.recognized.connect(handle_final_result)

        # Start continuous recognition
        logger.info(f"Starting speech recognition for: {audio_path}")
        recognizer.start_continuous_recognition()

        # Wait for recognition to complete
        import time
        # Get audio duration to know how long to wait
        try:
            from moviepy import AudioFileClip
            with AudioFileClip(audio_path) as audio:
                duration = audio.duration
            time.sleep(duration + 2)  # Wait for audio duration + buffer
        except:
            time.sleep(10)  # Default wait time

        recognizer.stop_continuous_recognition()

        logger.info(f"Generated {len(subtitles)} subtitle segments")
        return subtitles

    def save_to_srt(self, subtitles: List[SubtitleItem], output_path: str):
        """
        Save subtitles to SRT file

        Args:
            subtitles: List of SubtitleItem objects
            output_path: Path to save SRT file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitles, 1):
                # Format: HH:MM:SS,mmm
                start_time = self._format_timestamp(subtitle.start)
                end_time = self._format_timestamp(subtitle.end)

                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{subtitle.text}\n")
                f.write("\n")

        logger.info(f"Saved {len(subtitles)} subtitles to: {output_path}")

    def _format_timestamp(self, seconds: float) -> str:
        """
        Format seconds to SRT timestamp format

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
