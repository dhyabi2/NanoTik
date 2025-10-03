"""
Script to pre-generate voice preview samples for all available voices
Run this once to create all preview files and save API costs
"""

import os
import sys
from pathlib import Path
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.voices import VOICE_CATALOG
from app.services.voice_preview_service import VoicePreviewService
from app.config import load_config

# Preview texts for different languages
PREVIEW_TEXTS = {
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


def generate_all_voice_previews():
    """Generate preview audio files for all voices in the catalog"""

    # Load config
    config = load_config()

    # Get Azure Speech credentials
    speech_key = config['azure'].get('speech_key', '')
    speech_region = config['azure'].get('speech_region', 'eastus')

    if not speech_key:
        print("ERROR: Azure Speech key not configured!")
        print("Please set AZURE_SPEECH_KEY in your .env file or config.toml")
        return

    # Initialize speech config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

    # Initialize voice preview service
    preview_service = VoicePreviewService(speech_config)

    # Create output directory
    output_dir = Path('./voice_previews')
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating voice previews for {len(VOICE_CATALOG)} voices...")
    print(f"Output directory: {output_dir.absolute()}\n")

    success_count = 0
    error_count = 0

    for idx, (voice_id, voice_info) in enumerate(VOICE_CATALOG.items(), 1):
        # Create filename
        output_file = output_dir / f"{voice_id}.wav"

        # Skip if file already exists
        if output_file.exists():
            print(f"[{idx}/{len(VOICE_CATALOG)}] SKIP: {voice_id} (already exists)")
            success_count += 1
            continue

        try:
            # Get language code for preview text
            lang_code = voice_info['language'].split('-')[0]
            preview_text = PREVIEW_TEXTS.get(lang_code, PREVIEW_TEXTS['en'])

            print(f"[{idx}/{len(VOICE_CATALOG)}] Generating: {voice_id} ({voice_info['name']})...")

            # Generate preview
            preview_service.generate_preview(
                voice_id=voice_id,
                text=preview_text,
                output_path=str(output_file)
            )

            print(f"    ✓ Success: {output_file.name} ({output_file.stat().st_size / 1024:.1f} KB)")
            success_count += 1

        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            error_count += 1

            # Clean up partial file
            if output_file.exists():
                output_file.unlink()

    print("\n" + "="*60)
    print(f"SUMMARY:")
    print(f"  Total voices: {len(VOICE_CATALOG)}")
    print(f"  ✓ Success: {success_count}")
    print(f"  ✗ Errors: {error_count}")
    print(f"  Output directory: {output_dir.absolute()}")
    print("="*60)


if __name__ == "__main__":
    print("="*60)
    print("Voice Preview Generator")
    print("Pre-generating audio samples for all available voices")
    print("="*60 + "\n")

    generate_all_voice_previews()

    print("\nDone! Voice previews are ready to use.")
    print("The app will now use these pre-generated files instead of generating on-demand.")
