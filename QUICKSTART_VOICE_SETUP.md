# Quick Start: Voice Preview Setup

## 🎯 Goal
Pre-generate all voice preview audio files to save API costs and provide instant previews.

## 📋 Prerequisites
- Azure Speech Service configured (key in `.env` or `config.toml`)
- Python environment set up with dependencies installed

## 🚀 Quick Setup (3 Steps)

### Step 1: Verify Azure Configuration

Check that your Azure Speech key is configured:

```bash
# Windows
type .env

# Linux/Mac
cat .env
```

You should see:
```
AZURE_SPEECH_KEY=your-key-here
AZURE_SPEECH_REGION=eastus
```

### Step 2: Run the Generator

**Windows:**
```bash
generate_previews.bat
```
*or*
```bash
python generate_voice_previews.py
```

**Linux/Mac:**
```bash
chmod +x generate_previews.sh
./generate_previews.sh
```
*or*
```bash
python3 generate_voice_previews.py
```

### Step 3: Wait for Completion

The script will:
- ✅ Generate 100+ voice preview files
- ✅ Save them to `voice_previews/` folder
- ✅ Show progress and completion summary

**Expected time:** 10-15 minutes
**Expected cost:** ~$0.08 (one-time Azure TTS charge)

## ✅ Verification

After completion, verify the files were created:

```bash
# Windows
dir voice_previews

# Linux/Mac
ls -lh voice_previews/
```

You should see 100+ `.wav` files.

## 🎉 Done!

Your app is now ready to use voice previews!

When users click "🔊 Preview":
- ⚡ **Instant playback** from pre-generated files
- 💰 **Zero API cost** per preview
- 🚀 **Better user experience**

## 🔄 Updating Previews

If you need to regenerate (e.g., changed preview text):

```bash
# Delete old files
rm -rf voice_previews/    # Linux/Mac
rd /s /q voice_previews   # Windows

# Regenerate
python generate_voice_previews.py
```

## 📊 Storage Info

- **Size per file:** ~40-60 KB
- **Total size:** ~5-6 MB (for 100+ voices)
- **Disk space needed:** Minimal

## 💡 Tips

1. **Include in Git (Recommended for small teams)**
   - Uncomment `# voice_previews/` in `.gitignore`
   - Commit the folder to share with team

2. **Exclude from Git (Recommended for large deployments)**
   - Keep `voice_previews/` in `.gitignore`
   - Run generator on each deployment environment

3. **CDN/Cloud Storage (For production at scale)**
   - Upload to AWS S3, Cloudflare R2, or similar
   - Update app to fetch from cloud URL

## 🆘 Troubleshooting

**"Azure Speech key not configured"**
- Check your `.env` file has `AZURE_SPEECH_KEY`
- Verify the key is valid

**"Failed to generate preview"**
- Check internet connection
- Verify Azure quota/limits
- Try again (script skips existing files)

**App still generating on-demand**
- Ensure `voice_previews/` folder exists
- Check file naming matches voice IDs
- Verify file permissions

## 📖 More Info

See `VOICE_PREVIEWS_README.md` for detailed documentation.

---

**That's it! Enjoy instant voice previews! 🎤**
