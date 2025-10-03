"""
LLM Service for script generation
Supports multiple AI providers: OpenAI, DeepSeek, Moonshot, OpenRouter
"""

import os
from typing import Dict, Any, List
import openai
from openai import OpenAI


class LLMService:
    """Service for interacting with Large Language Models"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config['app'].get('llm_provider', 'openrouter')
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate LLM client based on provider"""
        if self.provider == 'openrouter':
            api_key = self.config['app'].get('openrouter_api_key')
            self.client = OpenAI(
                api_key=api_key,
                base_url='https://openrouter.ai/api/v1'
            )
            self.model = self.config['app'].get('openrouter_model_name', 'google/gemini-2.0-flash-001')

        elif self.provider == 'openai':
            api_key = self.config['app'].get('openai_api_key')
            base_url = self.config['app'].get('openai_base_url', 'https://api.openai.com/v1')
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = self.config['app'].get('openai_model_name', 'gpt-4')

        elif self.provider == 'deepseek':
            api_key = self.config['app'].get('deepseek_api_key')
            self.client = OpenAI(
                api_key=api_key,
                base_url='https://api.deepseek.com/v1'
            )
            self.model = 'deepseek-chat'

        elif self.provider == 'moonshot':
            api_key = self.config['app'].get('moonshot_api_key')
            self.client = OpenAI(
                api_key=api_key,
                base_url='https://api.moonshot.cn/v1'
            )
            self.model = 'moonshot-v1-8k'

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def generate_script(self, topic: str, duration: int, language: str = 'en') -> Dict[str, Any]:
        """
        Generate a video script based on topic and duration
        
        Args:
            topic: The video topic
            duration: Target duration in seconds
            language: Language code (en, zh, ar)
        
        Returns:
            Dictionary with script, scenes, and metadata
        """
        prompt = self._build_script_prompt(topic, duration, language)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(language)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            if content is None:
                raise Exception("No content received from LLM")
            return self._parse_script_response(content)
        
        except Exception as e:
            raise Exception(f"Failed to generate script: {str(e)}")
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on language"""
        prompts = {
            'en': "You are a professional video script writer. Create engaging, informative scripts for short-form videos.",
            'zh': "你是一位专业的视频脚本作家。为短视频创作引人入胜、信息丰富的脚本。",
            'ar': "أنت كاتب محترف لنصوص الفيديو. قم بإنشاء نصوص جذابة ومفيدة لمقاطع الفيديو القصيرة."
        }
        return prompts.get(language, prompts['en'])
    
    def _build_script_prompt(self, topic: str, duration: int, language: str) -> str:
        """Build the prompt for script generation"""
        word_count = duration * 2  # Approximate 2 words per second
        
        prompts = {
            'en': f"""Create a {duration}-second video script about: {topic}

Requirements:
- Approximately {word_count} words
- Include 5-7 distinct scenes
- Each scene should have a description and narration
- Make it engaging and informative
- Include visual suggestions for each scene

Format your response as:
Scene 1: [Visual description]
Narration: [What to say]

Scene 2: [Visual description]
Narration: [What to say]
...""",
            'zh': f"""创建一个{duration}秒的视频脚本，主题：{topic}

要求：
- 大约{word_count}字
- 包含5-7个不同的场景
- 每个场景应有描述和旁白
- 内容引人入胜且信息丰富
- 为每个场景提供视觉建议

按以下格式回复：
场景1：[视觉描述]
旁白：[要说的内容]

场景2：[视觉描述]
旁白：[要说的内容]
...""",
            'ar': f"""أنشئ نص فيديو مدته {duration} ثانية حول: {topic}

المتطلبات:
- حوالي {word_count} كلمة
- يشمل 5-7 مشاهد متميزة
- يجب أن يكون لكل مشهد وصف وسرد
- اجعله جذابًا وغنيًا بالمعلومات
- قدم اقتراحات بصرية لكل مشهد

صيغة الرد:
المشهد 1: [الوصف البصري]
السرد: [ما يجب قوله]

المشهد 2: [الوصف البصري]
السرد: [ما يجب قوله]
..."""
        }
        
        return prompts.get(language, prompts['en'])
    
    def _parse_script_response(self, content: str) -> Dict[str, Any]:
        """Parse the LLM response into structured script data"""
        scenes = []
        current_scene = None
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for scene markers in multiple languages
            if any(marker in line.lower() for marker in ['scene', '场景', 'المشهد']):
                if current_scene:
                    scenes.append(current_scene)
                current_scene = {'description': '', 'narration': ''}
                # Extract scene description
                if ':' in line:
                    current_scene['description'] = line.split(':', 1)[1].strip()
            
            elif any(marker in line.lower() for marker in ['narration', '旁白', 'السرد']):
                if current_scene and ':' in line:
                    current_scene['narration'] = line.split(':', 1)[1].strip()
        
        # Add the last scene
        if current_scene:
            scenes.append(current_scene)
        
        # Compile full narration
        full_narration = ' '.join([scene['narration'] for scene in scenes if scene.get('narration')])
        
        return {
            'scenes': scenes,
            'narration': full_narration,
            'scene_count': len(scenes)
        }
