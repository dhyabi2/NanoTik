"""
NanoTik - AI Video Generator with Nano Cryptocurrency Payments
Enhanced version of MoneyPrinterTurbo with modern UI and payment integration
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="NanoTik - AI Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Lazy imports - only import what's needed when needed
@st.cache_resource
def get_services():
    """Initialize services once and cache them"""
    from app.config import load_config
    from app.services.payment_service import PaymentService
    from app.services.video_service import VideoService
    from app.services.voice_preview_service import VoicePreviewService
    from app.services.auth_service import get_auth_service
    from app.database import get_database
    import azure.cognitiveservices.speech as speechsdk

    config = load_config()
    db = get_database()
    auth_service = get_auth_service()
    payment_service = PaymentService()
    video_service = VideoService(config)

    # Initialize voice preview service
    speech_key = config['azure'].get('speech_key', '')
    speech_region = config['azure'].get('speech_region', 'eastus')
    if speech_key:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        voice_preview_service = VoicePreviewService(speech_config)
    else:
        voice_preview_service = None

    return {
        'config': config,
        'db': db,
        'auth_service': auth_service,
        'payment_service': payment_service,
        'video_service': video_service,
        'voice_preview_service': voice_preview_service
    }

# Import only UI utilities at module level
from app.utils.i18n import get_text, set_language, SUPPORTED_LANGUAGES
from app.utils.voices import get_voices_by_language, get_default_voice

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Get cached services
services = get_services()
db = services['db']
auth_service = services['auth_service']
payment_service = services['payment_service']
video_service = services['video_service']
voice_preview_service = services['voice_preview_service']
config = services['config']

# Handle authentication and user initialization
if not st.session_state.get('authenticated', False):
    # Not authenticated - use anonymous session (always reinitialize after logout)
    if 'user_session' not in st.session_state or 'user_id' not in st.session_state:
        if 'user_session' not in st.session_state:
            from app.models.user import UserSession
            st.session_state.user_session = UserSession()

        # Get or create anonymous user in database
        db_user = db.get_user_by_session(st.session_state.user_session.session_id)
        if not db_user:
            db_user = db.create_user(st.session_state.user_session.session_id)
        st.session_state.user_id = db_user['id']
        st.session_state.credits = db_user['credits']
else:
    # Authenticated with Google - get or create authenticated user
    if 'user_id' not in st.session_state and st.session_state.get('google_id'):
        # Check if Google user exists
        db_user = db.get_user_by_google_id(st.session_state.google_id)

        if not db_user:
            # Create new authenticated user
            db_user = db.create_authenticated_user(
                email=st.session_state.user_email,
                google_id=st.session_state.google_id,
                name=st.session_state.user_name,
                profile_picture=st.session_state.get('user_picture')
            )

        # Always check for anonymous credits to migrate (on every login)
        anonymous_user = None
        if 'user_session' in st.session_state:
            anonymous_user = db.get_user_by_session(st.session_state.user_session.session_id)

        # Migrate if anonymous user exists, is different, and has something to migrate
        if anonymous_user and anonymous_user['id'] != db_user['id']:
            # Check if there's anything to migrate
            has_credits = anonymous_user['credits'] > 0
            has_trial = anonymous_user.get('has_used_trial', False)

            if has_credits or has_trial:
                # Transfer credits
                if has_credits:
                    db.add_credits(db_user['id'], anonymous_user['credits'])
                    db_user['credits'] = db_user.get('credits', 0) + anonymous_user['credits']
                    # Clear anonymous user credits after successful transfer
                    db.update_user_credits(anonymous_user['id'], 0)

                # Transfer free trial status if used
                if has_trial:
                    db.use_free_trial(db_user['id'])

        st.session_state.user_id = db_user['id']
        st.session_state.credits = db_user.get('credits', 0)

# Ensure credits is always set
if 'credits' not in st.session_state:
    st.session_state.credits = 0


def render_login_page():
    """Render the login page for unauthenticated users"""
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🎬 NanoTik")
        st.subheader(get_text('app.subtitle', st.session_state.language))

        st.markdown("<br>", unsafe_allow_html=True)

        # Login card
        with st.container():
            st.markdown("### Welcome!")
            st.write("Sign in with Google to start creating AI-powered videos")

            st.markdown("<br>", unsafe_allow_html=True)

            # Get redirect URI - for localhost development
            if 'REPLIT_DOMAINS' in os.environ:
                redirect_uri = f"https://{os.getenv('REPLIT_DOMAINS').split(',')[0]}"
            elif os.getenv('REPL_SLUG'):
                redirect_uri = f"https://{os.getenv('REPL_SLUG', 'localhost')}.{os.getenv('REPL_OWNER', 'replit')}.repl.co"
            else:
                # Localhost development
                redirect_uri = "http://localhost:5000"

            # Login button - centered
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                result = auth_service.login(redirect_uri)
                if result:
                    st.rerun()

        # Language selector at bottom
        st.markdown("<br><br>", unsafe_allow_html=True)
        language = st.selectbox(
            get_text('language.select', st.session_state.language),
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: SUPPORTED_LANGUAGES[x],
            key='language_selector'
        )
        if language != st.session_state.language:
            st.session_state.language = language
            set_language(language)
            st.rerun()

        # Features preview
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ✨ Features")
        st.write("✅ AI-powered video generation")
        st.write("✅ Multiple languages support")
        st.write("✅ HD & Premium quality options")
        st.write("✅ Pay with Nano cryptocurrency")


def render_header():
    """Render the application header with user info and language selector"""
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.title("🎬 NanoTik")
        st.caption(get_text('app.subtitle', st.session_state.language))

    with col2:
        # Show user info and logout button (only if authenticated)
        if st.session_state.get('authenticated'):
            if st.session_state.get('user_picture'):
                st.image(st.session_state.user_picture, width=40)
            st.caption(f"👤 {st.session_state.get('user_name', 'User')}")
            if st.button("Logout", key="logout_btn"):
                auth_service.logout()
                st.rerun()
        else:
            st.caption("👤 Anonymous User")

    with col3:
        language = st.selectbox(
            get_text('language.select', st.session_state.language),
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: SUPPORTED_LANGUAGES[x],
            key='language_selector'
        )
        if language != st.session_state.language:
            st.session_state.language = language
            set_language(language)
            st.rerun()


def render_sidebar():
    """Render the sidebar - payment per task model"""
    pass  # No sidebar needed for payment per task model


def handle_purchase(credits, bonus, price):
    """Handle credit purchase with Splitroute payment"""
    try:
        # Generate Splitroute payment invoice
        payment_result = payment_service.create_payment_request(
            amount=price,
            credits=credits + bonus,
            user_id=st.session_state.user_id
        )
        
        if payment_result['success']:
            # Store payment info in session
            st.session_state.pending_payment = payment_result
            st.rerun()
        else:
            st.error(f"{get_text('payment.failed', st.session_state.language)}: {payment_result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"{get_text('payment.error', st.session_state.language)}: {str(e)}")


@st.dialog("Complete Payment - 0.01 XNO")
def show_video_payment_dialog():
    """Show payment dialog with QR code for video generation"""
    payment = st.session_state.pending_video_payment

    st.markdown("### Pay to Generate Video")
    st.write(f"**Amount**: {payment['amount']} XNO")
    st.info("Scan the QR code with your Nano wallet or send to the address below")

    st.divider()

    # Show QR code
    if payment.get('qr_code'):
        # Center the QR code
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(payment['qr_code'], width=300)

    # Show payment address
    st.write("**Payment Address:**")
    st.code(payment['payment_address'], language=None)

    st.divider()

    # Check payment status button
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✓ Click here to continue", use_container_width=True, type="primary"):
            with st.spinner("Verifying payment..."):
                verification = payment_service.verify_payment(payment['invoice_id'])

                if verification.get('success') and verification.get('status') == 'paid':
                    # Payment confirmed - close dialog and start video generation
                    st.session_state.payment_verified = True
                    del st.session_state.pending_video_payment
                    # Rerun immediately to close dialog
                    st.rerun()
                elif verification.get('status') == 'expired':
                    # Store error message and close dialog
                    st.session_state.payment_error = "Payment expired. Please try again."
                    del st.session_state.pending_video_payment
                    if 'pending_video_params' in st.session_state:
                        del st.session_state.pending_video_params
                    st.rerun()
                elif not verification.get('success'):
                    st.error(f"Verification error: {verification.get('error', 'Unknown error')}")
                else:
                    st.error("⚠️ Payment not received yet. Please complete the payment and try again.")

    with col2:
        if st.button("Cancel", use_container_width=True):
            del st.session_state.pending_video_payment
            del st.session_state.pending_video_params
            st.rerun()


@st.dialog("Complete Payment")
def show_payment_dialog():
    """Show payment dialog with QR code and payment address"""
    payment = st.session_state.pending_payment

    st.write(f"**Amount**: {payment['amount']} XNO")
    st.write(f"**Credits**: {payment['credits']}")

    st.divider()

    # Show QR code if available
    if payment.get('qr_code'):
        st.image(payment['qr_code'], width=300)

    # Show payment address
    st.code(payment['payment_address'], language=None)

    st.info("Send the exact amount to the address above. Payment will be verified automatically.")

    # Check payment status button
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Check Payment Status", use_container_width=True):
            with st.spinner("Checking payment..."):
                verification = payment_service.verify_payment(payment['invoice_id'])

                if verification['success'] and verification['status'] == 'paid':
                    st.session_state.credits = verification['new_balance']
                    # Store success message before closing dialog
                    st.session_state.payment_success_message = f"Payment confirmed! {verification['credits_added']} credits added."
                    del st.session_state.pending_payment
                    st.rerun()
                elif verification['status'] == 'expired':
                    st.error("Payment expired. Please create a new payment.")
                    del st.session_state.pending_payment
                    st.rerun()
                else:
                    st.warning("Payment not received yet. Please wait a moment and try again.")

    with col2:
        if st.button("Cancel", use_container_width=True):
            del st.session_state.pending_payment
            st.rerun()


def render_video_generator():
    """Render the main video generation interface"""
    st.header(get_text('video.generate', st.session_state.language))

    # Check for free trial - get user from database
    if st.session_state.get('authenticated'):
        db_user = db.get_user_by_google_id(st.session_state.google_id)
    else:
        db_user = db.get_user_by_session(st.session_state.user_session.session_id)

    has_free_trial = db_user and not db_user.get('has_used_trial', False)

    # Check credits or free trial
    if st.session_state.credits < 1 and not has_free_trial:
        st.warning("You need credits to generate videos. Please purchase credits from the sidebar.")
        return

    if has_free_trial:
        st.info("🎁 **Using your FREE TRIAL** - This video generation is on us!")

    # Voice selection and preview (OUTSIDE form to allow button interaction)
    st.subheader("🎤 Voice Selection")
    st.caption("💡 Choose a voice that matches your content style. Use Preview to hear each voice before generating your video.")

    # Filter voices by selected language
    lang_code = st.session_state.language
    available_voices = get_voices_by_language(lang_code)

    # Create voice options for dropdown
    voice_options = {
        voice_id: f"{info['name']} ({info['gender']})"
        for voice_id, info in available_voices.items()
    }

    # Default voice based on language
    default_voice = get_default_voice(lang_code)

    # Initialize selected voice in session state
    if 'selected_voice' not in st.session_state:
        st.session_state.selected_voice = default_voice

    col_voice1, col_voice2 = st.columns([3, 1])

    with col_voice1:
        selected_voice = st.selectbox(
            "Select Voice",
            options=list(voice_options.keys()),
            format_func=lambda x: voice_options[x],
            index=list(voice_options.keys()).index(st.session_state.selected_voice) if st.session_state.selected_voice in voice_options else 0,
            key='voice_selector',
            help="🗣️ **Professional AI Voices**: Natural-sounding voice narration for your videos.\n\n• Choose **female voices** for warm, engaging content\n• Choose **male voices** for authoritative, professional content\n• Always preview before generating!"
        )
        # Update session state
        st.session_state.selected_voice = selected_voice

    with col_voice2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("🔊 Preview", use_container_width=True, help="Listen to a sample of the selected voice"):
            # Check for pre-generated preview file first
            preview_dir = Path('./voice_previews')
            preview_file = preview_dir / f"{selected_voice}.wav"

            if preview_file.exists():
                # Use pre-generated file
                try:
                    with open(preview_file, 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/wav')
                except Exception as e:
                    st.error(f"Failed to load preview: {str(e)}")
            else:
                # Generate on-demand if file doesn't exist
                if voice_preview_service:
                    with st.spinner("Generating voice preview..."):
                        try:
                            temp_preview = voice_preview_service.generate_preview(selected_voice)
                            # Play audio
                            with open(temp_preview, 'rb') as audio_file:
                                audio_bytes = audio_file.read()
                                st.audio(audio_bytes, format='audio/wav')
                            # Clean up temp file
                            os.unlink(temp_preview)
                        except Exception as e:
                            st.error(f"Failed to generate preview: {str(e)}")
                else:
                    st.error("Voice preview not available. Please configure voice service.")

    st.divider()

    # Video generation form
    with st.form("video_generator"):
        # Topic input
        topic = st.text_input(
            get_text('video.topic', st.session_state.language),
            placeholder=get_text('video.topic_placeholder', st.session_state.language),
            help="💡 **Best Practice**: Choose a clear, engaging topic that can be visually represented. Examples: 'The Future of AI', 'Top 5 Travel Destinations', 'How to Make Coffee'. The AI will generate a complete video script based on your topic."
        )

        # Custom script option
        use_custom_script = st.checkbox(
            "Use custom script (optional)",
            value=False,
            help="✍️ Enable this to write your own video narration instead of AI-generated script. Useful for branded content or specific messaging."
        )
        custom_script = None
        if use_custom_script:
            custom_script = st.text_area(
                "Custom Script",
                placeholder="Enter your custom video script here...",
                height=150,
                help="📝 Write your complete video narration here. The AI will match video clips to your script. Keep it concise and engaging for best results."
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            # Aspect ratio selection
            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                options=['16:9', '9:16'],
                format_func=lambda x: f"{x} ({'Horizontal' if x == '16:9' else 'Vertical'})",
                help="📱 **16:9 (Horizontal)**: Best for YouTube, traditional platforms, landscape viewing\n\n📲 **9:16 (Vertical)**: Optimized for TikTok, Instagram Reels, mobile-first content"
            )

        with col2:
            # Quality selection
            quality = st.selectbox(
                get_text('video.quality', st.session_state.language),
                options=['basic', 'hd', 'premium'],
                format_func=lambda x: get_text(f'video.{x}', st.session_state.language),
                help="🎬 **Basic**: Fast rendering, good for testing\n\n📺 **HD**: High quality, recommended for most content\n\n⭐ **Premium**: Best quality, slower rendering, ideal for professional content"
            )

        with col3:
            # Duration selection
            duration = st.slider(
                get_text('video.duration', st.session_state.language),
                min_value=15,
                max_value=180,
                value=60,
                step=15,
                help="⏱️ **Recommended**: 30-90 seconds for social media. Shorter videos (15-60s) have higher engagement. Longer videos (90-180s) better for educational content."
            )

        # Advanced options
        with st.expander(get_text('video.advanced', st.session_state.language)):
            col1, col2 = st.columns(2)

            with col2:
                clip_duration = st.slider(
                    "Clip Duration (seconds)",
                    min_value=2,
                    max_value=10,
                    value=5,
                    step=1,
                    help="🎞️ **Clip Switching Frequency**: How long each video scene appears before switching.\n\n• **2-3s**: Fast-paced, high energy (TikTok style)\n• **5-6s**: Balanced, recommended for most content\n• **8-10s**: Slower pace, cinematic feel"
                )

            # Background music settings
            music_enabled = st.checkbox(
                get_text('video.music', st.session_state.language),
                value=False,
                help="🎵 Add background music to enhance your video. Music will be automatically mixed with voiceover narration."
            )

            if music_enabled:
                col3, col4 = st.columns(2)

                with col3:
                    music_file = st.file_uploader(
                        "Upload Background Music (MP3)",
                        type=['mp3'],
                        help="📁 Upload your own royalty-free background music in MP3 format. Choose instrumental tracks that complement your content without overpowering the narration."
                    )

                with col4:
                    music_volume = st.slider(
                        "Music Volume",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.2,
                        step=0.1,
                        help="🔊 **Recommended**: 0.1-0.3 for subtle background music. Lower values ensure voiceover remains clear and audible."
                    )
            else:
                music_file = None
                music_volume = 0.0

            subtitle_position = st.selectbox(
                get_text('video.subtitle_position', st.session_state.language),
                options=['bottom', 'top', 'center'],
                help="💬 **Subtitle Position**:\n\n• **Bottom**: Standard for most platforms\n• **Top**: Good for videos with bottom-screen CTAs\n• **Center**: Maximum visibility, use for key messages"
            )

        # Submit button
        submitted = st.form_submit_button(
            get_text('video.create', st.session_state.language),
            use_container_width=True
        )

        if submitted:
            if not topic and not custom_script:
                st.error(get_text('video.topic_required', st.session_state.language))
            elif music_enabled and not music_file:
                st.error("Please upload a music file or disable background music.")
            else:
                generate_video(
                    topic=topic,
                    quality=quality,
                    duration=duration,
                    voice=st.session_state.selected_voice,
                    music_enabled=music_enabled,
                    music_volume=music_volume,
                    music_file=music_file,
                    subtitle_position=subtitle_position,
                    aspect_ratio=aspect_ratio,
                    clip_duration=clip_duration,
                    custom_script=custom_script
                )

    # Display generated video outside the form (to allow download button)
    if 'generated_video' in st.session_state and st.session_state.generated_video:
        video_data = st.session_state.generated_video

        st.divider()

        # Show success message
        if video_data.get('used_free_trial'):
            st.success("🎁 Free trial video generated successfully!")
        else:
            st.success(get_text('video.success', st.session_state.language))

        # Display video player
        if os.path.exists(video_data['path']):
            st.video(video_data['path'])

            # Download button outside form
            try:
                with open(video_data['path'], 'rb') as f:
                    video_bytes = f.read()
                    st.download_button(
                        label=get_text('video.download', st.session_state.language),
                        data=video_bytes,
                        file_name=f"nanotik_{video_data['topic'][:20].replace(' ', '_')}.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error reading video file: {str(e)}")
        else:
            st.error(f"Video file not found at: {video_data['path']}")

        # Clear button
        if st.button("Generate Another Video", use_container_width=True):
            del st.session_state.generated_video
            st.rerun()


def generate_video(topic, quality, duration, voice, music_enabled, music_volume,
                   music_file, subtitle_position, aspect_ratio, clip_duration, custom_script=None):
    """Generate video based on user input"""
    # Check for free trial - get user from database
    if st.session_state.get('authenticated'):
        db_user = db.get_user_by_google_id(st.session_state.google_id)
    else:
        db_user = db.get_user_by_session(st.session_state.user_session.session_id)

    has_free_trial = db_user and not db_user.get('has_used_trial', False)

    # Calculate credit cost
    cost_map = {'basic': 1, 'hd': 2, 'premium': 3}
    cost = cost_map[quality]

    # Check if user can afford (has credits OR has free trial)
    if not has_free_trial and st.session_state.credits < cost:
        st.error(get_text('credits.insufficient', st.session_state.language))
        return

    # Create payment invoice for 0.01 XNO
    try:
        payment_result = payment_service.create_video_payment_invoice(
            user_id=st.session_state.user_id
        )

        if not payment_result['success']:
            st.error(f"Failed to create payment: {payment_result.get('error', 'Unknown error')}")
            return

        # Store payment info in session
        st.session_state.pending_video_payment = payment_result
        st.session_state.pending_video_params = {
            'topic': topic,
            'quality': quality,
            'duration': duration,
            'voice': voice,
            'music_enabled': music_enabled,
            'music_volume': music_volume,
            'music_file': music_file,
            'subtitle_position': subtitle_position,
            'aspect_ratio': aspect_ratio,
            'clip_duration': clip_duration,
            'custom_script': custom_script
        }

        # Show payment dialog
        st.rerun()

    except Exception as e:
        st.error(f"Payment error: {str(e)}")
        return


def process_video_generation():
    """Process video generation after payment is verified"""
    params = st.session_state.pending_video_params

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Progress callback function
    def update_progress(progress, message):
        progress_bar.progress(progress / 100)
        status_text.text(message)

    # Get video params and user info
    topic = params['topic']
    quality = params['quality']
    duration = params['duration']
    voice = params['voice']
    music_enabled = params['music_enabled']
    music_volume = params['music_volume']
    music_file = params['music_file']
    subtitle_position = params['subtitle_position']
    aspect_ratio = params['aspect_ratio']
    clip_duration = params['clip_duration']
    custom_script = params['custom_script']

    # Check for free trial
    if st.session_state.get('authenticated'):
        db_user = db.get_user_by_google_id(st.session_state.google_id)
    else:
        db_user = db.get_user_by_session(st.session_state.user_session.session_id)

    has_free_trial = db_user and not db_user.get('has_used_trial', False)

    # Calculate credit cost
    cost_map = {'basic': 1, 'hd': 2, 'premium': 3}
    cost = cost_map[quality]

    try:
        # Save uploaded music file temporarily if provided
        music_path = None
        if music_enabled and music_file:
            import tempfile
            temp_music = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_music.write(music_file.read())
            temp_music.close()
            music_path = temp_music.name

        # Step 1: Generate or use custom script
        if custom_script:
            update_progress(10, "Using custom script...")
            # Parse custom script into expected format
            script = {
                'narration': custom_script,
                'scenes': [{'description': topic or 'Custom video', 'narration': custom_script}],
                'scene_count': 1,
                'language': st.session_state.language
            }
        else:
            update_progress(10, get_text('video.generating_script', st.session_state.language))
            script = video_service.generate_script(topic, duration, st.session_state.language)
            script['language'] = st.session_state.language

        # Step 2: Generate voiceover
        update_progress(30, get_text('video.generating_voice', st.session_state.language))

        audio_path = video_service.generate_voiceover(script, voice, st.session_state.language)

        # Step 3: Search for video clips
        update_progress(50, get_text('video.searching_clips', st.session_state.language))

        clips = video_service.search_video_clips(script)

        # Step 4: Compose video (with detailed progress updates)
        update_progress(60, get_text('video.composing', st.session_state.language))

        video_path = video_service.compose_video(
            clips=clips,
            audio_path=audio_path,
            script=script,
            subtitle_position=subtitle_position,
            quality=quality,
            music_enabled=music_enabled,
            music_volume=music_volume,
            music_path=music_path,
            aspect_ratio=aspect_ratio,
            clip_duration=clip_duration,
            progress_callback=update_progress
        )

        # Step 5: Finalize
        progress_bar.progress(100)
        status_text.text(get_text('video.complete', st.session_state.language))

        # Handle payment: free trial or credits
        success = False
        used_free_trial = False
        if has_free_trial:
            # Mark free trial as used
            db.use_free_trial(st.session_state.user_id)
            success = True
            used_free_trial = True
        else:
            # Deduct credits from database
            if db.deduct_credits(st.session_state.user_id, cost):
                st.session_state.credits -= cost
                success = True

        if success:
            # Save video to database
            video_record = db.create_video(st.session_state.user_id, {
                'title': topic[:100],
                'topic': topic,
                'file_path': video_path,
                'duration': duration,
                'quality': quality,
                'language': st.session_state.language,
                'status': 'completed'
            })

            # Store video in session state for display outside form
            st.session_state.generated_video = {
                'path': video_path,
                'topic': topic,
                'used_free_trial': used_free_trial
            }

            # Clean up video payment params
            if 'pending_video_params' in st.session_state:
                del st.session_state.pending_video_params

            # Rerun to display the video outside the form
            st.rerun()
        else:
            st.error("Unable to deduct credits. Please try again.")

    except Exception as e:
        st.error(f"{get_text('video.error', st.session_state.language)}: {str(e)}")
        status_text.text("")
        progress_bar.empty()
    finally:
        # Clean up temporary music file
        if music_path and os.path.exists(music_path):
            try:
                os.unlink(music_path)
            except:
                pass


def render_gallery():
    """Render user's video gallery from database"""
    st.header(get_text('gallery.title', st.session_state.language))
    
    videos = db.get_user_videos(st.session_state.user_id, limit=30)
    
    if not videos:
        st.info(get_text('gallery.empty', st.session_state.language))
        return
    
    cols = st.columns(3)
    for idx, video in enumerate(videos):
        with cols[idx % 3]:
            if os.path.exists(video['file_path']):
                st.video(video['file_path'])
                st.caption(video['title'])
                st.caption(f"{get_text('gallery.created', st.session_state.language)}: {video['created_at'].strftime('%Y-%m-%d %H:%M')}")


def main():
    """Main application entry point"""
    # Temporarily disable Google authentication - allow anonymous access
    # if not st.session_state.get('authenticated'):
    #     # Show login page for unauthenticated users
    #     render_login_page()
    #     return

    # Show main app (anonymous or authenticated)
    render_header()
    render_sidebar()

    # Show payment dialog if pending (for credit purchase)
    if 'pending_payment' in st.session_state:
        show_payment_dialog()

    # Show payment error if exists
    if 'payment_error' in st.session_state:
        st.error(st.session_state.payment_error)
        del st.session_state.payment_error

    # Show video payment dialog if pending
    if 'pending_video_payment' in st.session_state:
        show_video_payment_dialog()

    # Process video generation if payment verified
    if 'payment_verified' in st.session_state and st.session_state.payment_verified:
        st.success("✅ Payment confirmed! Starting video generation...")
        st.session_state.payment_verified = False
        process_video_generation()
        return

    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        get_text('tabs.create', st.session_state.language),
        get_text('tabs.gallery', st.session_state.language),
        get_text('tabs.about', st.session_state.language)
    ])

    with tab1:
        render_video_generator()

    with tab2:
        render_gallery()

    with tab3:
        st.markdown(get_text('about.content', st.session_state.language))

        # Feature list
        st.subheader(get_text('about.features', st.session_state.language))
        features = [
            'about.feature1',
            'about.feature2',
            'about.feature3',
            'about.feature4',
            'about.feature5'
        ]
        for feature in features:
            st.write(f"- {get_text(feature, st.session_state.language)}")

    # Footer
    st.divider()
    st.caption(get_text('footer.text', st.session_state.language))


if __name__ == "__main__":
    main()
