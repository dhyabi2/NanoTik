#!/bin/bash

echo "============================================================"
echo "Voice Preview Generator"
echo "============================================================"
echo ""
echo "This will generate audio previews for all 100+ voices."
echo "This is a ONE-TIME setup that saves API costs."
echo ""
echo "Estimated time: 10-15 minutes"
echo "Estimated cost: ~\$0.08 (one-time Azure TTS charges)"
echo ""
read -p "Press Enter to continue..."

python3 generate_voice_previews.py

echo ""
echo "============================================================"
echo "Generation Complete!"
echo "============================================================"
echo ""
echo "Voice previews are now saved in the 'voice_previews' folder."
echo "The app will use these files automatically."
echo ""
read -p "Press Enter to exit..."
