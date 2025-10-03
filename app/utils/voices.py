"""
Azure TTS Voice Catalog
Complete list of available voices from Azure Cognitive Services
"""

# Voice data: {voice_id: {'name': display_name, 'language': lang_code, 'gender': M/F}}
VOICE_CATALOG = {
    # English - United States
    'en-US-AnaNeural': {'name': 'Ana (US, Female)', 'language': 'en-US', 'gender': 'F'},
    'en-US-AndrewNeural': {'name': 'Andrew (US, Male)', 'language': 'en-US', 'gender': 'M'},
    'en-US-AriaNeural': {'name': 'Aria (US, Female)', 'language': 'en-US', 'gender': 'F'},
    'en-US-AvaNeural': {'name': 'Ava (US, Female)', 'language': 'en-US', 'gender': 'F'},
    'en-US-BrianNeural': {'name': 'Brian (US, Male)', 'language': 'en-US', 'gender': 'M'},
    'en-US-ChristopherNeural': {'name': 'Christopher (US, Male)', 'language': 'en-US', 'gender': 'M'},
    'en-US-EmmaNeural': {'name': 'Emma (US, Female)', 'language': 'en-US', 'gender': 'F'},
    'en-US-EricNeural': {'name': 'Eric (US, Male)', 'language': 'en-US', 'gender': 'M'},
    'en-US-GuyNeural': {'name': 'Guy (US, Male)', 'language': 'en-US', 'gender': 'M'},
    'en-US-JennyNeural': {'name': 'Jenny (US, Female)', 'language': 'en-US', 'gender': 'F'},
    'en-US-MichelleNeural': {'name': 'Michelle (US, Female)', 'language': 'en-US', 'gender': 'F'},
    'en-US-RogerNeural': {'name': 'Roger (US, Male)', 'language': 'en-US', 'gender': 'M'},
    'en-US-SteffanNeural': {'name': 'Steffan (US, Male)', 'language': 'en-US', 'gender': 'M'},

    # English - United Kingdom
    'en-GB-RyanNeural': {'name': 'Ryan (UK, Male)', 'language': 'en-GB', 'gender': 'M'},
    'en-GB-SoniaNeural': {'name': 'Sonia (UK, Female)', 'language': 'en-GB', 'gender': 'F'},
    'en-GB-LibbyNeural': {'name': 'Libby (UK, Female)', 'language': 'en-GB', 'gender': 'F'},
    'en-GB-AbbiNeural': {'name': 'Abbi (UK, Female)', 'language': 'en-GB', 'gender': 'F'},
    'en-GB-AlfieNeural': {'name': 'Alfie (UK, Male)', 'language': 'en-GB', 'gender': 'M'},
    'en-GB-BellaNeural': {'name': 'Bella (UK, Female)', 'language': 'en-GB', 'gender': 'F'},
    'en-GB-ElliotNeural': {'name': 'Elliot (UK, Male)', 'language': 'en-GB', 'gender': 'M'},
    'en-GB-EthanNeural': {'name': 'Ethan (UK, Male)', 'language': 'en-GB', 'gender': 'M'},
    'en-GB-HollieNeural': {'name': 'Hollie (UK, Female)', 'language': 'en-GB', 'gender': 'F'},
    'en-GB-MaisieNeural': {'name': 'Maisie (UK, Female)', 'language': 'en-GB', 'gender': 'F'},
    'en-GB-NoahNeural': {'name': 'Noah (UK, Male)', 'language': 'en-GB', 'gender': 'M'},
    'en-GB-OliverNeural': {'name': 'Oliver (UK, Male)', 'language': 'en-GB', 'gender': 'M'},
    'en-GB-OliviaNeural': {'name': 'Olivia (UK, Female)', 'language': 'en-GB', 'gender': 'F'},
    'en-GB-ThomasNeural': {'name': 'Thomas (UK, Male)', 'language': 'en-GB', 'gender': 'M'},

    # English - Australia
    'en-AU-NatashaNeural': {'name': 'Natasha (AU, Female)', 'language': 'en-AU', 'gender': 'F'},
    'en-AU-WilliamNeural': {'name': 'William (AU, Male)', 'language': 'en-AU', 'gender': 'M'},
    'en-AU-AnnetteNeural': {'name': 'Annette (AU, Female)', 'language': 'en-AU', 'gender': 'F'},
    'en-AU-CarlyNeural': {'name': 'Carly (AU, Female)', 'language': 'en-AU', 'gender': 'F'},
    'en-AU-DarrenNeural': {'name': 'Darren (AU, Male)', 'language': 'en-AU', 'gender': 'M'},
    'en-AU-DuncanNeural': {'name': 'Duncan (AU, Male)', 'language': 'en-AU', 'gender': 'M'},
    'en-AU-ElsieNeural': {'name': 'Elsie (AU, Female)', 'language': 'en-AU', 'gender': 'F'},
    'en-AU-FreyaNeural': {'name': 'Freya (AU, Female)', 'language': 'en-AU', 'gender': 'F'},
    'en-AU-JoanneNeural': {'name': 'Joanne (AU, Female)', 'language': 'en-AU', 'gender': 'F'},
    'en-AU-KenNeural': {'name': 'Ken (AU, Male)', 'language': 'en-AU', 'gender': 'M'},
    'en-AU-KimNeural': {'name': 'Kim (AU, Female)', 'language': 'en-AU', 'gender': 'F'},
    'en-AU-NeilNeural': {'name': 'Neil (AU, Male)', 'language': 'en-AU', 'gender': 'M'},
    'en-AU-TimNeural': {'name': 'Tim (AU, Male)', 'language': 'en-AU', 'gender': 'M'},
    'en-AU-TinaNeural': {'name': 'Tina (AU, Female)', 'language': 'en-AU', 'gender': 'F'},

    # English - Canada
    'en-CA-ClaraNeural': {'name': 'Clara (CA, Female)', 'language': 'en-CA', 'gender': 'F'},
    'en-CA-LiamNeural': {'name': 'Liam (CA, Male)', 'language': 'en-CA', 'gender': 'M'},

    # English - India
    'en-IN-NeerjaNeural': {'name': 'Neerja (IN, Female)', 'language': 'en-IN', 'gender': 'F'},
    'en-IN-PrabhatNeural': {'name': 'Prabhat (IN, Male)', 'language': 'en-IN', 'gender': 'M'},

    # Chinese - Mandarin (Simplified)
    'zh-CN-XiaoxiaoNeural': {'name': 'Xiaoxiao (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-YunxiNeural': {'name': 'Yunxi (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},
    'zh-CN-YunjianNeural': {'name': 'Yunjian (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},
    'zh-CN-XiaoyiNeural': {'name': 'Xiaoyi (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-YunyangNeural': {'name': 'Yunyang (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},
    'zh-CN-XiaochenNeural': {'name': 'Xiaochen (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaohanNeural': {'name': 'Xiaohan (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaomengNeural': {'name': 'Xiaomeng (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaomoNeural': {'name': 'Xiaomo (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaoqiuNeural': {'name': 'Xiaoqiu (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaoruiNeural': {'name': 'Xiaorui (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaoshuangNeural': {'name': 'Xiaoshuang (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaoxuanNeural': {'name': 'Xiaoxuan (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaoyanNeural': {'name': 'Xiaoyan (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaoyouNeural': {'name': 'Xiaoyou (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-XiaozhenNeural': {'name': 'Xiaozhen (CN, Female)', 'language': 'zh-CN', 'gender': 'F'},
    'zh-CN-YunfengNeural': {'name': 'Yunfeng (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},
    'zh-CN-YunhaoNeural': {'name': 'Yunhao (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},
    'zh-CN-YunxiaNeural': {'name': 'Yunxia (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},
    'zh-CN-YunyeNeural': {'name': 'Yunye (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},
    'zh-CN-YunzeNeural': {'name': 'Yunze (CN, Male)', 'language': 'zh-CN', 'gender': 'M'},

    # Arabic - Saudi Arabia
    'ar-SA-ZariyahNeural': {'name': 'Zariyah (SA, Female)', 'language': 'ar-SA', 'gender': 'F'},
    'ar-SA-HamedNeural': {'name': 'Hamed (SA, Male)', 'language': 'ar-SA', 'gender': 'M'},

    # Arabic - Egypt
    'ar-EG-SalmaNeural': {'name': 'Salma (EG, Female)', 'language': 'ar-EG', 'gender': 'F'},
    'ar-EG-ShakirNeural': {'name': 'Shakir (EG, Male)', 'language': 'ar-EG', 'gender': 'M'},

    # Arabic - UAE
    'ar-AE-FatimaNeural': {'name': 'Fatima (AE, Female)', 'language': 'ar-AE', 'gender': 'F'},
    'ar-AE-HamdanNeural': {'name': 'Hamdan (AE, Male)', 'language': 'ar-AE', 'gender': 'M'},

    # Spanish - Spain
    'es-ES-ElviraNeural': {'name': 'Elvira (ES, Female)', 'language': 'es-ES', 'gender': 'F'},
    'es-ES-AlvaroNeural': {'name': 'Alvaro (ES, Male)', 'language': 'es-ES', 'gender': 'M'},

    # Spanish - Mexico
    'es-MX-DaliaNeural': {'name': 'Dalia (MX, Female)', 'language': 'es-MX', 'gender': 'F'},
    'es-MX-JorgeNeural': {'name': 'Jorge (MX, Male)', 'language': 'es-MX', 'gender': 'M'},

    # French - France
    'fr-FR-DeniseNeural': {'name': 'Denise (FR, Female)', 'language': 'fr-FR', 'gender': 'F'},
    'fr-FR-HenriNeural': {'name': 'Henri (FR, Male)', 'language': 'fr-FR', 'gender': 'M'},

    # German - Germany
    'de-DE-KatjaNeural': {'name': 'Katja (DE, Female)', 'language': 'de-DE', 'gender': 'F'},
    'de-DE-ConradNeural': {'name': 'Conrad (DE, Male)', 'language': 'de-DE', 'gender': 'M'},

    # Italian - Italy
    'it-IT-ElsaNeural': {'name': 'Elsa (IT, Female)', 'language': 'it-IT', 'gender': 'F'},
    'it-IT-DiegoNeural': {'name': 'Diego (IT, Male)', 'language': 'it-IT', 'gender': 'M'},

    # Japanese - Japan
    'ja-JP-NanamiNeural': {'name': 'Nanami (JP, Female)', 'language': 'ja-JP', 'gender': 'F'},
    'ja-JP-KeitaNeural': {'name': 'Keita (JP, Male)', 'language': 'ja-JP', 'gender': 'M'},

    # Korean - Korea
    'ko-KR-SunHiNeural': {'name': 'SunHi (KR, Female)', 'language': 'ko-KR', 'gender': 'F'},
    'ko-KR-InJoonNeural': {'name': 'InJoon (KR, Male)', 'language': 'ko-KR', 'gender': 'M'},

    # Portuguese - Brazil
    'pt-BR-FranciscaNeural': {'name': 'Francisca (BR, Female)', 'language': 'pt-BR', 'gender': 'F'},
    'pt-BR-AntonioNeural': {'name': 'Antonio (BR, Male)', 'language': 'pt-BR', 'gender': 'M'},

    # Russian - Russia
    'ru-RU-SvetlanaNeural': {'name': 'Svetlana (RU, Female)', 'language': 'ru-RU', 'gender': 'F'},
    'ru-RU-DmitryNeural': {'name': 'Dmitry (RU, Male)', 'language': 'ru-RU', 'gender': 'M'},

    # Hindi - India
    'hi-IN-SwaraNeural': {'name': 'Swara (IN, Female)', 'language': 'hi-IN', 'gender': 'F'},
    'hi-IN-MadhurNeural': {'name': 'Madhur (IN, Male)', 'language': 'hi-IN', 'gender': 'M'},

    # Turkish - Turkey
    'tr-TR-EmelNeural': {'name': 'Emel (TR, Female)', 'language': 'tr-TR', 'gender': 'F'},
    'tr-TR-AhmetNeural': {'name': 'Ahmet (TR, Male)', 'language': 'tr-TR', 'gender': 'M'},

    # Dutch - Netherlands
    'nl-NL-ColetteNeural': {'name': 'Colette (NL, Female)', 'language': 'nl-NL', 'gender': 'F'},
    'nl-NL-MaartenNeural': {'name': 'Maarten (NL, Male)', 'language': 'nl-NL', 'gender': 'M'},

    # Polish - Poland
    'pl-PL-ZofiaNeural': {'name': 'Zofia (PL, Female)', 'language': 'pl-PL', 'gender': 'F'},
    'pl-PL-MarekNeural': {'name': 'Marek (PL, Male)', 'language': 'pl-PL', 'gender': 'M'},

    # Swedish - Sweden
    'sv-SE-SofieNeural': {'name': 'Sofie (SE, Female)', 'language': 'sv-SE', 'gender': 'F'},
    'sv-SE-MattiasNeural': {'name': 'Mattias (SE, Male)', 'language': 'sv-SE', 'gender': 'M'},
}


def get_voices_by_language(language_code: str = None):
    """
    Get voices filtered by language code

    Args:
        language_code: Language code like 'en-US', 'zh-CN', 'ar-SA'. If None, returns all voices.

    Returns:
        Dictionary of voices matching the language
    """
    if not language_code:
        return VOICE_CATALOG

    return {
        voice_id: info
        for voice_id, info in VOICE_CATALOG.items()
        if info['language'].startswith(language_code[:2])
    }


def get_default_voice(language_code: str):
    """
    Get default voice for a language

    Args:
        language_code: Language code like 'en', 'zh', 'ar'

    Returns:
        Default voice ID for the language
    """
    defaults = {
        'en': 'en-US-JennyNeural',
        'zh': 'zh-CN-XiaoxiaoNeural',
        'ar': 'ar-SA-ZariyahNeural',
        'es': 'es-ES-ElviraNeural',
        'fr': 'fr-FR-DeniseNeural',
        'de': 'de-DE-KatjaNeural',
        'it': 'it-IT-ElsaNeural',
        'ja': 'ja-JP-NanamiNeural',
        'ko': 'ko-KR-SunHiNeural',
        'pt': 'pt-BR-FranciscaNeural',
        'ru': 'ru-RU-SvetlanaNeural',
        'hi': 'hi-IN-SwaraNeural',
        'tr': 'tr-TR-EmelNeural',
        'nl': 'nl-NL-ColetteNeural',
        'pl': 'pl-PL-ZofiaNeural',
        'sv': 'sv-SE-SofieNeural',
    }

    return defaults.get(language_code, 'en-US-JennyNeural')
