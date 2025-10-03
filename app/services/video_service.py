"""
Video Service for video generation and composition
Handles script generation, voiceover, video clips, and final composition
"""

import os
from typing import Dict, Any, List
from pathlib import Path
import tempfile
import requests
import azure.cognitiveservices.speech as speechsdk
from pexels_api import API as PexelsAPI
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configure MoviePy to use imageio-ffmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = ""  # Let imageio-ffmpeg auto-detect
import imageio_ffmpeg
os.environ["FFMPEG_BINARY"] = imageio_ffmpeg.get_ffmpeg_exe()
logger.info(f"Using ffmpeg: {imageio_ffmpeg.get_ffmpeg_exe()}")

from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video import fx as vfx
from contextlib import ExitStack
from .llm_service import LLMService
from .subtitle_service import SubtitleService, SubtitleItem
import random


class VideoService:
    """Service for video generation operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm_service = LLMService(config)
        self.output_dir = Path(config['video'].get('output_dir', './output'))
        self.temp_dir = Path(config['video'].get('temp_dir', './temp'))

        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Pexels API
        pexels_keys = self.config['app'].get('pexels_api_keys', [])
        self.pexels_api = PexelsAPI(pexels_keys[0]) if pexels_keys else None

        # Initialize Azure Speech
        speech_key = self.config['azure'].get('speech_key', '')
        speech_region = self.config['azure'].get('speech_region', 'eastus')
        if speech_key:
            self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
            self.subtitle_service = SubtitleService(self.speech_config)
        else:
            self.speech_config = None
            self.subtitle_service = None
    
    def generate_script(self, topic: str, duration: int, language: str = 'en') -> Dict[str, Any]:
        """
        Generate video script using LLM
        
        Args:
            topic: Video topic
            duration: Target duration in seconds
            language: Language code
        
        Returns:
            Script data with scenes and narration
        """
        return self.llm_service.generate_script(topic, duration, language)
    
    def generate_voiceover(self, script: Dict[str, Any], voice: str, language: str = 'en') -> str:
        """
        Generate voiceover audio from script using Azure TTS

        Args:
            script: Script data with narration
            voice: Voice ID (e.g., 'en-US-JennyNeural') or legacy type (male, female, neutral)
            language: Language code (used for legacy voice selection)

        Returns:
            Path to generated audio file
        """
        audio_file = self.temp_dir / f"voiceover_{os.urandom(8).hex()}.wav"

        if not self.speech_config:
            raise Exception("Azure Speech Services not configured. Please add AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.")

        try:
            # Check if voice is a full voice ID (contains 'Neural') or legacy type
            if 'Neural' in voice or '-' in voice:
                # Modern voice ID format (e.g., 'en-US-JennyNeural')
                selected_voice = voice
            else:
                # Legacy format: male/female/neutral
                voice_map = {
                    'en': {'male': 'en-US-GuyNeural', 'female': 'en-US-JennyNeural', 'neutral': 'en-US-AriaNeural'},
                    'zh': {'male': 'zh-CN-YunxiNeural', 'female': 'zh-CN-XiaoxiaoNeural', 'neutral': 'zh-CN-YunyangNeural'},
                    'ar': {'male': 'ar-SA-HamedNeural', 'female': 'ar-SA-ZariyahNeural', 'neutral': 'ar-SA-HamedNeural'}
                }
                selected_voice = voice_map.get(language, voice_map['en']).get(voice, voice_map['en']['neutral'])

            self.speech_config.speech_synthesis_voice_name = selected_voice
            logger.info(f"Using voice: {selected_voice}")
            
            # Configure audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=str(audio_file))
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
            
            # Generate speech
            narration_text = script.get('narration', '')
            if not narration_text:
                raise Exception("No narration text found in script")
            
            result = synthesizer.speak_text_async(narration_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return str(audio_file)
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                # Clean up partial file
                if audio_file.exists():
                    audio_file.unlink()
                raise Exception(f"Speech synthesis canceled: {cancellation.reason}. Error: {cancellation.error_details}")
            else:
                # Clean up partial file
                if audio_file.exists():
                    audio_file.unlink()
                raise Exception(f"Speech synthesis failed with reason: {result.reason}")
        except Exception as e:
            # Clean up on any error
            if audio_file.exists():
                audio_file.unlink()
            raise
    
    def search_video_clips(self, script: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for video clips based on script scenes using Pexels REST API
        
        Args:
            script: Script data with scenes
        
        Returns:
            List of video clip metadata with download URLs
        """
        clips = []
        
        # Get API key from config
        pexels_keys = self.config['app'].get('pexels_api_keys', [])
        if not pexels_keys:
            raise Exception("Pexels API not configured. Please add PEXELS_API_KEYS.")
        
        api_key = pexels_keys[0]
        base_url = "https://api.pexels.com/videos/search"
        
        for idx, scene in enumerate(script.get('scenes', [])):
            query = scene.get('description', '')[:100]  # Limit query length
            if not query:
                continue
            
            try:
                # Search for videos using Pexels REST API
                headers = {'Authorization': api_key}
                params = {
                    'query': query,
                    'per_page': 3,
                    'page': 1,
                    'orientation': 'landscape'
                }
                
                response = requests.get(base_url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                videos = data.get('videos', [])
                
                if videos:
                    # Try each video until we find one with valid files
                    for video in videos:
                        video_files = video.get('video_files', [])
                        
                        if not video_files:
                            continue
                        
                        # Find the best quality video file (prefer HD, highest bitrate)
                        best_file = None
                        best_score = 0
                        
                        for vf in video_files:
                            width = vf.get('width', 0)
                            quality = vf.get('quality', '')
                            
                            # Score: HD quality + higher resolution
                            score = (1000 if quality == 'hd' else 0) + width
                            
                            if score > best_score and width >= 1280:
                                best_file = vf
                                best_score = score
                        
                        # Fallback to first available file if no HD found
                        if not best_file and video_files:
                            best_file = video_files[0]
                        
                        if best_file:
                            clip = {
                                'id': video.get('id', f"clip_{idx}"),
                                'url': best_file.get('link', ''),
                                'description': query,
                                'duration': video.get('duration', 5),
                                'width': best_file.get('width', 1920),
                                'height': best_file.get('height', 1080),
                                'source': 'pexels'
                            }
                            
                            if clip['url']:
                                clips.append(clip)
                                break  # Found a good clip for this scene
                        
            except Exception as e:
                print(f"Warning: Failed to fetch clip for scene {idx}: {str(e)}")
                continue
        
        if not clips:
            raise Exception("Could not find any suitable video clips for the script scenes")
        
        return clips
    
    def compose_video(
        self,
        clips: List[Dict[str, Any]],
        audio_path: str,
        script: Dict[str, Any],
        subtitle_position: str = 'bottom',
        quality: str = 'basic',
        music_enabled: bool = True,
        music_volume: float = 0.2,
        music_path: str = None,
        aspect_ratio: str = '16:9',
        clip_duration: int = 5,
        progress_callback=None
    ) -> str:
        """
        Compose final video from clips and audio using MoviePy

        Args:
            clips: List of video clip data with URLs
            audio_path: Path to voiceover audio file
            script: Script data (unused for now)
            subtitle_position: Subtitle position (unused for now)
            quality: Video quality setting (basic, hd, premium)
            music: Background music flag (unused for now)
            progress_callback: Optional callback function to report progress (progress, message)

        Returns:
            Path to final video file
        """
        output_file = self.output_dir / f"video_{os.urandom(8).hex()}.mp4"
        downloaded_clips = []

        logger.info(f"Starting video composition with {len(clips)} clips")

        with ExitStack() as stack:
            try:
                # Step 1: Download video clips
                logger.info("Step 1: Downloading video clips...")
                if progress_callback:
                    progress_callback(61, f"Downloading {len(clips)} video clips...")

                for i, clip in enumerate(clips):
                    clip_path = self.temp_dir / f"clip_{i}_{os.urandom(4).hex()}.mp4"
                    try:
                        logger.info(f"Downloading clip {i+1}/{len(clips)} from {clip['url'][:50]}...")
                        if progress_callback:
                            progress_callback(61 + (i * 3 // len(clips)), f"Downloading clip {i+1}/{len(clips)}...")

                        response = requests.get(clip['url'], stream=True, timeout=30)
                        response.raise_for_status()

                        with open(clip_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)

                        logger.info(f"Downloaded clip {i+1} to {clip_path} ({clip_path.stat().st_size} bytes)")
                        downloaded_clips.append(clip_path)
                    except Exception as e:
                        logger.warning(f"Failed to download clip {i}: {str(e)}")
                        continue

                if not downloaded_clips:
                    raise Exception("Failed to download any video clips")

                # Step 2: Load audio to get duration
                logger.info("Step 2: Loading audio file...")
                if progress_callback:
                    progress_callback(65, "Loading audio file...")

                audio_clip = stack.enter_context(AudioFileClip(audio_path))
                total_audio_duration = audio_clip.duration
                logger.info(f"Audio loaded. Duration: {total_audio_duration}s")

                # Step 3: Load and process video clips
                # Set resolution based on aspect ratio and quality
                if aspect_ratio == '9:16':
                    # Vertical (portrait)
                    target_resolution = (1080, 1920) if quality in ['hd', 'premium'] else (720, 1280)
                else:
                    # Horizontal (landscape) - default 16:9
                    target_resolution = (1920, 1080) if quality in ['hd', 'premium'] else (1280, 720)

                video_clips = []

                logger.info(f"Step 3: Loading {len(downloaded_clips)} video clips...")
                if progress_callback:
                    progress_callback(68, f"Loading and processing {len(downloaded_clips)} video clips...")

                for idx, clip_path in enumerate(downloaded_clips):
                    try:
                        logger.info(f"Loading clip {idx+1}/{len(downloaded_clips)}: {clip_path} ({clip_path.stat().st_size} bytes)")
                        if progress_callback:
                            progress_callback(68 + (idx * 5 // len(downloaded_clips)), f"Processing clip {idx+1}/{len(downloaded_clips)}...")

                        video = stack.enter_context(VideoFileClip(str(clip_path)))
                        logger.info(f"Clip {idx+1} loaded. Duration: {video.duration}s, Size: {video.size}")
                        # Resize to target resolution
                        logger.info(f"Resizing clip {idx+1} to {target_resolution}...")
                        video = video.resized(target_resolution)
                        video_clips.append(video)
                        logger.info(f"Clip {idx+1} resized successfully")
                    except Exception as e:
                        logger.error(f"Failed to load clip {clip_path}: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        continue

                if not video_clips:
                    raise Exception(f"Failed to load any video clips. Downloaded {len(downloaded_clips)} files but none could be loaded by MoviePy.")

                # Step 4: Adjust clip durations to match audio
                logger.info("Step 4: Adjusting clip durations...")
                if progress_callback:
                    progress_callback(74, "Adjusting clip durations...")

                # Use user-specified clip duration (with bounds)
                target_clip_duration = max(2, min(clip_duration, total_audio_duration / len(video_clips)))
                clips_needed = int(total_audio_duration / target_clip_duration) + 1
                logger.info(f"Target clip duration: {target_clip_duration}s, clips needed: {clips_needed}")

                adjusted_clips = []
                clip_index = 0

                # Cycle through available clips to fill the duration
                for i in range(clips_needed):
                    video = video_clips[clip_index % len(video_clips)]
                    clip_index += 1

                    logger.info(f"Adjusting clip {i+1}/{clips_needed} (current duration: {video.duration}s)")
                    if progress_callback:
                        progress_callback(74 + (i * 3 // clips_needed), f"Adjusting clip {i+1}/{clips_needed}...")

                    if video.duration > target_clip_duration:
                        # Trim if too long
                        adjusted = video.subclipped(0, target_clip_duration)
                        logger.info(f"Trimmed clip {i+1} to {target_clip_duration}s")
                    else:
                        # Loop if too short - manually concatenate copies
                        loops_needed = int(target_clip_duration / video.duration) + 1
                        logger.info(f"Looping clip {i+1} {loops_needed} times")
                        looped = concatenate_videoclips([video] * loops_needed)
                        adjusted = looped.subclipped(0, target_clip_duration)
                        logger.info(f"Looped and trimmed clip {i+1} to {target_clip_duration}s")

                    adjusted_clips.append(adjusted)

                # Step 5: Concatenate all clips
                logger.info(f"Step 5: Concatenating {len(adjusted_clips)} clips...")
                if progress_callback:
                    progress_callback(78, f"Combining {len(adjusted_clips)} clips together...")

                final_video = concatenate_videoclips(adjusted_clips, method="compose")
                logger.info("Clips concatenated successfully")

                # Step 6: Add audio
                logger.info("Step 6: Adding audio to video...")
                if progress_callback:
                    progress_callback(82, "Adding voiceover audio...")

                # Mix voiceover with background music if enabled
                if music_enabled and music_volume > 0 and music_path:
                    try:
                        logger.info(f"Adding background music from: {music_path}")

                        # Load music and adjust to video duration
                        music_clip = stack.enter_context(AudioFileClip(music_path))

                        # Loop or trim music to match video duration
                        if music_clip.duration < total_audio_duration:
                            # Loop music
                            loops = int(total_audio_duration / music_clip.duration) + 1
                            music_clip = music_clip.loop(n=loops)

                        music_clip = music_clip.subclipped(0, total_audio_duration)

                        # Reduce music volume and mix with voiceover
                        music_clip = music_clip.with_volume_scaled(music_volume)

                        # Composite audio: voiceover + background music
                        mixed_audio = CompositeAudioClip([audio_clip, music_clip])
                        final_video = final_video.with_audio(mixed_audio)
                        logger.info("Background music added successfully")

                    except Exception as e:
                        logger.warning(f"Failed to add background music: {e}. Using voiceover only.")
                        final_video = final_video.with_audio(audio_clip)
                else:
                    final_video = final_video.with_audio(audio_clip)

                logger.info("Audio added successfully")

                # Step 6.5: Generate and add subtitles
                subtitle_provider = self.config.get('video', {}).get('subtitle_provider', 'edge')
                if subtitle_provider and self.subtitle_service:
                    logger.info("Step 6.5: Generating subtitles...")
                    if progress_callback:
                        progress_callback(83, "Generating subtitles...")

                    try:
                        # Generate subtitles from audio
                        # Map language names to codes
                        language_map = {'en': 'en', 'zh': 'zh', 'ar': 'ar', 'english': 'en', 'chinese': 'zh', 'arabic': 'ar'}
                        lang = script.get('language', 'en').lower()
                        lang_code = language_map.get(lang, 'en')
                        subtitles = self.subtitle_service.generate_subtitles(audio_path, lang_code)

                        if subtitles:
                            logger.info(f"Generated {len(subtitles)} subtitle segments")
                            if progress_callback:
                                progress_callback(84, "Adding subtitles to video...")

                            # Add subtitle overlays to video
                            final_video = self._add_subtitles_to_video(final_video, subtitles, subtitle_position)
                            logger.info("Subtitles added successfully")
                    except Exception as e:
                        logger.warning(f"Failed to generate subtitles: {e}")
                        # Continue without subtitles

                # Step 7: Set quality parameters
                quality_settings = {
                    'basic': {'bitrate': '1000k', 'audio_bitrate': '128k'},
                    'hd': {'bitrate': '2500k', 'audio_bitrate': '192k'},
                    'premium': {'bitrate': '5000k', 'audio_bitrate': '256k'}
                }

                settings = quality_settings.get(quality, quality_settings['basic'])

                # Step 8: Write output file
                logger.info(f"Step 7: Writing video to: {output_file}")
                logger.info(f"Quality settings: {settings}")
                logger.info("This may take a few minutes depending on video length and quality...")
                if progress_callback:
                    progress_callback(85, "Encoding final video (this may take a few minutes)...")

                final_video.write_videofile(
                    str(output_file),
                    codec='libx264',
                    audio_codec='aac',
                    bitrate=settings['bitrate'],
                    audio_bitrate=settings['audio_bitrate'],
                    fps=24,
                    preset='ultrafast',  # Changed from 'medium' to 'ultrafast' for faster encoding
                    threads=4,  # Increased from 2 to 4 for faster processing
                    logger='bar'  # Show progress bar
                )
                logger.info("Video file written successfully")

                # Clean up adjusted clips and final video
                for clip in adjusted_clips:
                    try:
                        clip.close()
                    except:
                        pass

                try:
                    final_video.close()
                except:
                    pass

                # Verify the file was created
                if not output_file.exists():
                    raise Exception(f"Video file was not created at {output_file}")

                logger.info(f"Video successfully created at: {output_file} (size: {output_file.stat().st_size} bytes)")
                return str(output_file)

            finally:
                # Always clean up downloaded temp files
                for clip_path in downloaded_clips:
                    try:
                        clip_path.unlink()
                    except:
                        pass

    def _add_subtitles_to_video(self, video_clip, subtitles: List[SubtitleItem], position: str = 'bottom'):
        """
        Add subtitle overlays to video

        Args:
            video_clip: MoviePy VideoClip
            subtitles: List of SubtitleItem objects
            position: Subtitle position ('bottom', 'top', 'center')

        Returns:
            VideoClip with subtitles overlaid
        """
        # Get subtitle styling from config
        subtitle_config = self.config.get('video', {}).get('subtitle', {})
        font = subtitle_config.get('font', 'Arial')
        font_size = subtitle_config.get('font_size', 60)
        text_color = subtitle_config.get('text_color', 'white')
        stroke_color = subtitle_config.get('stroke_color', 'black')
        stroke_width = subtitle_config.get('stroke_width', 2)

        # Calculate position
        video_width, video_height = video_clip.size

        if position == 'bottom':
            y_pos = video_height - 150
        elif position == 'top':
            y_pos = 100
        else:  # center
            y_pos = video_height / 2

        # Create text clips for each subtitle
        text_clips = []

        for subtitle in subtitles:
            try:
                # Create text clip with styling
                text_clip = TextClip(
                    text=subtitle.text,
                    font=font,
                    font_size=font_size,
                    color=text_color,
                    stroke_color=stroke_color,
                    stroke_width=stroke_width,
                    method='caption',
                    size=(video_width - 100, None),
                    text_align='center'
                )

                # Set timing and position
                text_clip = text_clip.with_start(subtitle.start).with_duration(subtitle.end - subtitle.start)
                text_clip = text_clip.with_position(('center', y_pos))

                text_clips.append(text_clip)

            except Exception as e:
                logger.warning(f"Failed to create subtitle clip: {e}")
                continue

        # Composite video with subtitles
        if text_clips:
            logger.info(f"Adding {len(text_clips)} subtitle clips to video")
            final_clip = CompositeVideoClip([video_clip] + text_clips)
            return final_clip
        else:
            logger.warning("No subtitle clips created")
            return video_clip
