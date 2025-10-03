"""
Check Voice Preview Status
Quick script to check which voice previews are available and which are missing
"""

import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.voices import VOICE_CATALOG


def check_voice_previews():
    """Check status of voice preview files"""

    preview_dir = Path('./voice_previews')

    print("="*70)
    print("Voice Preview Status Checker")
    print("="*70)
    print()

    # Check if directory exists
    if not preview_dir.exists():
        print("❌ Voice previews directory NOT FOUND")
        print(f"   Expected location: {preview_dir.absolute()}")
        print()
        print("💡 To create voice previews, run:")
        print("   python generate_voice_previews.py")
        print()
        return

    print(f"📁 Preview directory: {preview_dir.absolute()}")
    print()

    # Check each voice
    available = []
    missing = []

    for voice_id, voice_info in VOICE_CATALOG.items():
        preview_file = preview_dir / f"{voice_id}.wav"

        if preview_file.exists():
            file_size = preview_file.stat().st_size / 1024  # KB
            available.append((voice_id, voice_info, file_size))
        else:
            missing.append((voice_id, voice_info))

    # Display results
    print(f"✅ Available: {len(available)}/{len(VOICE_CATALOG)} voices")
    print(f"❌ Missing: {len(missing)}/{len(VOICE_CATALOG)} voices")
    print()

    if available:
        total_size = sum([size for _, _, size in available])
        print(f"💾 Total size: {total_size/1024:.2f} MB")
        print()

    # Show missing voices
    if missing:
        print("="*70)
        print("Missing Voice Previews:")
        print("="*70)

        # Group by language
        missing_by_lang = {}
        for voice_id, voice_info in missing:
            lang = voice_info['language']
            if lang not in missing_by_lang:
                missing_by_lang[lang] = []
            missing_by_lang[lang].append((voice_id, voice_info['name']))

        for lang, voices in sorted(missing_by_lang.items()):
            print(f"\n{lang}:")
            for voice_id, name in voices:
                print(f"  - {voice_id} ({name})")

        print()
        print("💡 To generate missing previews, run:")
        print("   python generate_voice_previews.py")
        print()

    else:
        print("="*70)
        print("🎉 All voice previews are ready!")
        print("="*70)
        print()
        print("Your app will use these pre-generated files for instant previews.")
        print("No API costs will be incurred when users test voices.")
        print()

    # Show sample files
    if available:
        print("="*70)
        print("Sample Available Voices (first 10):")
        print("="*70)
        for voice_id, voice_info, size in available[:10]:
            print(f"  ✓ {voice_id}")
            print(f"    {voice_info['name']} - {size:.1f} KB")

        if len(available) > 10:
            print(f"  ... and {len(available) - 10} more")
        print()


if __name__ == "__main__":
    check_voice_previews()
