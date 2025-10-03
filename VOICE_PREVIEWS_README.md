# Voice Previews Generator

## Overview

This script pre-generates voice preview audio samples for all 100+ available Azure TTS voices. Running this script once will save significant API costs by eliminating the need to generate previews on-demand when users test voices.

## Why Pre-generate?

- **Cost Savings**: Azure TTS charges per character synthesized. Pre-generating saves costs from multiple users testing the same voices.
- **Faster Preview**: Instant playback from pre-generated files vs. waiting for synthesis.
- **Offline Capability**: Previews work even without Azure API access.

## How to Run

### 1. Ensure Azure Speech Credentials are Configured

Make sure you have your Azure Speech key configured in one of these ways:

**Option A: Environment Variable**
```bash
export AZURE_SPEECH_KEY="your-key-here"
export AZURE_SPEECH_REGION="eastus"
```

**Option B: .env File**
```
AZURE_SPEECH_KEY=your-key-here
AZURE_SPEECH_REGION=eastus
```

**Option C: config.toml**
```toml
[azure]
speech_key = "your-key-here"
speech_region = "eastus"
```

### 2. Run the Generator Script

```bash
python generate_voice_previews.py
```

### 3. Wait for Completion

The script will:
- Generate preview audio for all 100+ voices
- Save them to `./voice_previews/` directory
- Show progress and summary

**Expected Output:**
```
============================================================
Voice Preview Generator
Pre-generating audio samples for all available voices
============================================================

Generating voice previews for 100 voices...
Output directory: /path/to/voice_previews

[1/100] Generating: en-US-AnaNeural (Ana (US, Female))...
    ✓ Success: en-US-AnaNeural.wav (45.2 KB)
[2/100] Generating: en-US-AndrewNeural (Andrew (US, Male))...
    ✓ Success: en-US-AndrewNeural.wav (47.8 KB)
...
```

### 4. Verify Output

After completion, check the `voice_previews` folder:

```bash
ls -lh voice_previews/
```

You should see 100+ `.wav` files, one for each voice.

## File Structure

```
voice_previews/
├── en-US-AnaNeural.wav
├── en-US-AndrewNeural.wav
├── en-US-AriaNeural.wav
├── zh-CN-XiaoxiaoNeural.wav
├── zh-CN-YunxiNeural.wav
├── ar-SA-ZariyahNeural.wav
└── ... (100+ more)
```

## Usage in Application

The application automatically uses pre-generated files when available:

1. **User clicks "🔊 Preview"**
2. **App checks** `./voice_previews/{voice_id}.wav`
3. **If exists**: Plays pre-generated file (instant, free)
4. **If not exists**: Generates on-demand (slower, costs API credits)

## Regenerating Previews

If you want to regenerate all previews (e.g., after changing preview text):

```bash
# Delete old previews
rm -rf voice_previews/

# Regenerate
python generate_voice_previews.py
```

## Incremental Generation

The script **skips existing files**, so you can:
- Run it multiple times safely
- Generate only missing voices
- Add new voices incrementally

## Storage Requirements

- **Per file**: ~40-60 KB (5-second audio sample)
- **Total for 100 voices**: ~5-6 MB
- **Minimal disk space** required

## Troubleshooting

### "Azure Speech key not configured"
- Ensure your `.env` file or `config.toml` has the Azure Speech credentials
- Verify the credentials are correct

### "Failed to generate preview"
- Check your internet connection
- Verify Azure Speech service quota/limits
- Check if the voice ID is valid

### Files not being used in app
- Ensure `voice_previews/` folder is in the same directory as `app.py`
- Check file permissions (files should be readable)
- Verify filename matches voice ID exactly (case-sensitive)

## Cost Estimation

**Without Pre-generation:**
- 100 voices × 10 users testing = 1,000 API calls
- ~50 characters per preview × 1,000 = 50,000 characters
- Cost: ~$0.80 (at $16 per 1M characters)

**With Pre-generation:**
- 100 voices × 1 generation = 100 API calls
- ~50 characters per preview × 100 = 5,000 characters
- Cost: ~$0.08 (one-time)

**Savings: ~90%** for every 10 users!

## Advanced: Custom Preview Text

Edit `generate_voice_previews.py` to customize preview text:

```python
PREVIEW_TEXTS = {
    'en': "Your custom English preview text here!",
    'zh': "你的自定义中文预览文本！",
    # ... add more languages
}
```

Then regenerate:
```bash
rm -rf voice_previews/
python generate_voice_previews.py
```

## Deployment

For production deployment, you can:

1. **Pre-generate locally**, then deploy the `voice_previews/` folder
2. **Add to version control** (recommended for small teams)
3. **Run once on server** after deployment
4. **Use CDN/cloud storage** for very large deployments

## Questions?

- Check the script output for errors
- Review Azure Speech service documentation
- Verify voice IDs in `app/utils/voices.py`
