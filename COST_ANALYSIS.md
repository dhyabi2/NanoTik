# Video Generation Cost Analysis - 15 Second Video

## API Pricing Research (2025)

### 1. Azure Speech TTS (Voiceover)
- **Pricing**: $16 per 1 million characters (Neural TTS)
- **Free Tier**: 500,000 characters/month

### 2. Pexels Video API (Stock Footage)
- **Pricing**: **FREE** (completely free API)
- **Limits**: 200 requests/hour, 20,000/month (free)
- **Unlimited**: Available for free with attribution
- **Cost**: $0.00

### 3. OpenAI API (Script Generation)
- **GPT-4o**: $3/million input tokens, $10/million output tokens
- **GPT-4o Mini**: $0.15/million input tokens, $0.60/million output tokens
- **GPT-3.5 Turbo**: $0.50/million input tokens, $1.50/million output tokens

### 4. Nano (XNO) Current Price
- **Current Price**: ~$0.86 USD per XNO (as of 2025)
- **Range**: $0.81 - $0.86 USD

---

## Cost Breakdown: 15-Second Video

### Assumptions:
- **Duration**: 15 seconds
- **Script**: ~30 words (2 words/second)
- **Voiceover**: ~150 characters (5 chars/word)
- **Video clips**: 3 clips (5 seconds each)
- **Quality**: Basic (SD)

### Detailed Cost Calculation:

#### 1. Script Generation (GPT-4o)
- **Input**: ~100 tokens (prompt)
- **Output**: ~75 tokens (30 words × 2.5 chars/word ÷ 4 chars/token)
- **Total tokens**: 175 tokens

**Calculation:**
- Input cost: 100 tokens × ($3 / 1M tokens) = $0.0003
- Output cost: 75 tokens × ($10 / 1M tokens) = $0.00075
- **Total**: $0.00105 ≈ **$0.001**

#### 2. Voiceover Generation (Azure TTS Neural)
- **Characters**: ~150 characters
- **Price**: $16 per 1M characters

**Calculation:**
- 150 chars × ($16 / 1M chars) = $0.0024
- **Total**: **$0.0024** ≈ **$0.002**

#### 3. Video Clips (Pexels)
- **Cost**: **$0.00** (FREE)

#### 4. Subtitle Generation (Azure Speech Recognition)
- **Price**: $1 per audio hour for batch transcription
- **Duration**: 15 seconds = 0.00417 hours

**Calculation:**
- 0.00417 hours × $1 = $0.00417
- **Total**: **$0.004**

---

## Total Cost Per 15-Second Video

| Component | Cost (USD) |
|-----------|-----------|
| Script Generation (GPT-4o) | $0.001 |
| Voiceover (Azure TTS) | $0.002 |
| Video Clips (Pexels) | $0.000 |
| Subtitles (Azure SR) | $0.004 |
| **TOTAL COST** | **$0.007** |

**Rounded**: **$0.01 USD per 15-second video**

---

## Pricing Strategy: Cost + 100% Markup

### Base Cost: $0.007 USD
### Markup: 100% (2x)
### **Selling Price: $0.014 USD** (rounded to **$0.015**)

### Convert to XNO (Nano)

**Current XNO Price**: $0.86 USD

**Calculation:**
- $0.015 USD ÷ $0.86 per XNO = **0.0174 XNO**
- **Rounded**: **0.02 XNO** per 15-second video

---

## Complete Pricing Table (All Durations)

Assuming proportional scaling:

| Duration | Base Cost | Cost + 100% | Price in USD | Price in XNO (@ $0.86) |
|----------|-----------|-------------|--------------|------------------------|
| **15 sec** | $0.007 | $0.014 | **$0.015** | **0.02 XNO** |
| **30 sec** | $0.014 | $0.028 | **$0.03** | **0.035 XNO** |
| **60 sec** | $0.028 | $0.056 | **$0.06** | **0.07 XNO** |
| **90 sec** | $0.042 | $0.084 | **$0.09** | **0.10 XNO** |
| **120 sec** | $0.056 | $0.112 | **$0.12** | **0.14 XNO** |
| **180 sec** | $0.084 | $0.168 | **$0.17** | **0.20 XNO** |

---

## Quality Tier Pricing

Different quality levels have different processing requirements:

### Basic Quality (SD - 720p)
- **Base multiplier**: 1x
- **15 sec**: 0.02 XNO
- **60 sec**: 0.07 XNO
- **180 sec**: 0.20 XNO

### HD Quality (1080p)
- **Base multiplier**: 1.5x (higher resolution encoding)
- **15 sec**: 0.03 XNO
- **60 sec**: 0.10 XNO
- **180 sec**: 0.30 XNO

### Premium Quality (1080p + Enhanced)
- **Base multiplier**: 2x (highest quality encoding + processing)
- **15 sec**: 0.04 XNO
- **60 sec**: 0.14 XNO
- **180 sec**: 0.40 XNO

---

## Recommended Pricing Packages

### Starter Package
- **Credits**: 100
- **Cost**: 1 XNO
- **Bonus**: 0 credits
- **Equivalent**: ~5 basic 60-sec videos OR 50 basic 15-sec videos

### Popular Package (⭐ RECOMMENDED)
- **Credits**: 200
- **Cost**: 2 XNO
- **Bonus**: 20 credits (10% bonus)
- **Total**: 220 credits
- **Equivalent**: ~11 basic 60-sec videos

### Pro Package
- **Credits**: 500
- **Cost**: 5 XNO
- **Bonus**: 100 credits (20% bonus)
- **Total**: 600 credits
- **Equivalent**: ~30 basic 60-sec videos

### Enterprise Package
- **Credits**: 1000
- **Cost**: 10 XNO
- **Bonus**: 250 credits (25% bonus)
- **Total**: 1250 credits
- **Equivalent**: ~62 basic 60-sec videos

---

## Credit System Conversion

### Simplified Credit System (Current Implementation)

| Video Quality | Credits per Video |
|--------------|-------------------|
| Basic | 1 credit |
| HD | 2 credits |
| Premium | 3 credits |

**Credit Value**: 1 credit = 0.01 XNO (at base pricing)

This simplified system makes it easier for users:
- Easy to understand
- Predictable pricing
- No need to calculate per-second costs

---

## Cost Optimization Opportunities

### 1. Use GPT-4o Mini (90% cost reduction on script)
- **GPT-4o**: $0.001 per video
- **GPT-4o Mini**: $0.0001 per video
- **Savings**: $0.0009 per video

### 2. Batch Processing
- Generate multiple scripts in one API call
- Reduce per-video overhead

### 3. Caching
- Cache common scripts/phrases
- Reuse similar content structures

### 4. Voice Previews (Already Implemented)
- Pre-generated previews save ~$0.002 per preview
- 100 voices × 10 users = $0.20 saved vs $2.00 on-demand
- **90% savings** on preview generation

---

## Monthly Cost Projections

Assuming 1000 videos generated per month (mix of durations):

### User Distribution:
- 30% - 15 sec videos (300 videos)
- 40% - 60 sec videos (400 videos)
- 30% - 180 sec videos (300 videos)

### Average Quality Distribution:
- 60% Basic (600 videos)
- 30% HD (300 videos)
- 10% Premium (100 videos)

### Monthly API Costs:
- **Script Generation**: ~$1.00
- **Voiceover**: ~$4.00
- **Subtitles**: ~$6.00
- **Video Clips**: $0.00 (FREE)
- **Total**: **~$11/month for 1000 videos**

### Revenue (with 100% markup):
- Cost: $11
- Revenue: $22
- **Profit**: $11/month

### At Scale (10,000 videos/month):
- Cost: ~$110
- Revenue: ~$220
- **Profit**: ~$110/month

---

## Conclusion

### Final Recommended Pricing:

**Per Video (Duration-Based):**
- Basic Quality: 1 credit per video (any duration ≤180 sec)
- HD Quality: 2 credits per video
- Premium Quality: 3 credits per video

**Credit Packages:**
- 100 credits = 1 XNO ($0.86)
- 200 credits + 20 bonus = 2 XNO
- 500 credits + 100 bonus = 5 XNO
- 1000 credits + 250 bonus = 10 XNO

**This pricing structure:**
✅ Covers all API costs (2x markup)
✅ Simple and predictable
✅ Competitive with market rates
✅ Profitable at scale
✅ Encourages bulk purchases with bonuses
