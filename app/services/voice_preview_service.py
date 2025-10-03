"""
Voice Preview Service
Generates short audio samples for voice testing
"""

import os
import azure.cognitiveservices.speech as speechsdk
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class VoicePreviewService:
    """Service for generating voice preview samples"""

    def __init__(self, speech_config):
        """
        Initialize voice preview service

        Args:
            speech_config: Azure SpeechConfig object
        """
        self.speech_config = speech_config

    def generate_preview(self, voice_id: str, text: str = None, output_path: str = None) -> str:
        """
        Generate a preview audio sample for a voice

        Args:
            voice_id: Azure voice ID (e.g., 'en-US-JennyNeural')
            text: Text to synthesize (defaults to sample text)
            output_path: Path to save audio file (defaults to temp file)

        Returns:
            Path to generated audio file
        """
        if not text:
            # Default preview text in different languages
            preview_texts = {
                'en': "Hello! This is a preview of my voice. I hope you like it!",
                'zh': "你好！这是我的声音预览。希望你喜欢！",
                'ar': "مرحبا! هذه معاينة لصوتي. أتمنى أن تعجبك!",
                'es': "¡Hola! Esta es una vista previa de mi voz. ¡Espero que te guste!",
                'fr': "Bonjour! Ceci est un aperçu de ma voix. J'espère que cela vous plaira!",
                'de': "Hallo! Dies ist eine Vorschau meiner Stimme. Ich hoffe, es gefällt Ihnen!",
                'it': "Ciao! Questa è un'anteprima della mia voce. Spero ti piaccia!",
                'ja': "こんにちは！これは私の声のプレビューです。気に入っていただければ幸いです！",
                'ko': "안녕하세요! 제 목소리 미리보기입니다. 마음에 드셨으면 좋겠어요!",
                'pt': "Olá! Esta é uma prévia da minha voz. Espero que você goste!",
                'ru': "Привет! Это предварительный просмотр моего голоса. Надеюсь, вам понравится!",
                'hi': "नमस्ते! यह मेरी आवाज़ का पूर्वावलोकन है। मुझे आशा है कि आपको यह पसंद आएगा!",
                'tr': "Merhaba! Bu benim sesimin bir ön izlemesi. Umarım beğenirsiniz!",
                'nl': "Hallo! Dit is een voorproefje van mijn stem. Ik hoop dat je het leuk vindt!",
                'pl': "Cześć! To jest podgląd mojego głosu. Mam nadzieję, że ci się spodoba!",
                'sv': "Hej! Det här är en förhandsgranskning av min röst. Jag hoppas att du gillar det!",
            }

            # Extract language code from voice_id
            lang_code = voice_id.split('-')[0] if '-' in voice_id else 'en'
            text = preview_texts.get(lang_code, preview_texts['en'])

        if not output_path:
            # Create temp file
            temp_dir = Path('./temp')
            temp_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(temp_dir / f"voice_preview_{os.urandom(4).hex()}.wav")

        try:
            # Configure speech synthesis
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_config.subscription_key,
                region=self.speech_config.region
            )
            speech_config.speech_synthesis_voice_name = voice_id

            # Configure audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )

            # Generate speech
            result = synthesizer.speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Voice preview generated: {voice_id} -> {output_path}")
                return output_path
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                # Clean up partial file
                if os.path.exists(output_path):
                    os.unlink(output_path)
                raise Exception(f"Voice preview canceled: {cancellation.reason}. Error: {cancellation.error_details}")
            else:
                # Clean up partial file
                if os.path.exists(output_path):
                    os.unlink(output_path)
                raise Exception(f"Voice preview failed: {result.reason}")

        except Exception as e:
            # Clean up on error
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
            raise Exception(f"Failed to generate voice preview: {str(e)}")
