"""
Internationalization utilities for multi-language support
Supports English, Chinese (Simplified), and Arabic
"""

from typing import Dict, Any, Optional

SUPPORTED_LANGUAGES = {
    'en': '🇬🇧 English',
    'zh': '🇨🇳 简体中文',
    'ar': '🇸🇦 العربية'
}

TRANSLATIONS = {
    'en': {
        'app.subtitle': 'AI-Powered Video Generator with Nano Payments',
        'language.select': 'Language',
        'credits.balance': 'Credits',
        'credits.name': 'credits',
        'credits.bonus': 'bonus',
        'credits.buy': '💰 Buy Credits',
        'credits.purchase': 'Purchase',
        'credits.info': '💡 Credits are used to generate videos. Different quality levels require different amounts of credits.',
        'credits.costs': 'Credit Costs',
        'credits.insufficient': '⚠️ Insufficient credits. Please purchase more credits to continue.',
        'credits.buy_prompt': '👉 Use the sidebar to purchase credits with Nano cryptocurrency.',
        'payment.processing': 'Processing payment...',
        'payment.success': '✅ Payment successful! Credits added to your account.',
        'payment.failed': '❌ Payment failed. Please try again.',
        'payment.error': 'Payment error',
        'video.generate': '🎬 Generate Video',
        'video.topic': 'Video Topic',
        'video.topic_placeholder': 'Enter the topic for your video...',
        'video.topic_required': 'Please enter a video topic.',
        'video.quality': 'Video Quality',
        'video.duration': 'Duration (seconds)',
        'video.advanced': '⚙️ Advanced Options',
        'video.voice': 'Voice Type',
        'video.music': 'Add Background Music',
        'video.subtitle_position': 'Subtitle Position',
        'video.create': '🚀 Create Video',
        'video.basic': 'Basic (1 credit)',
        'video.hd': 'HD (2 credits)',
        'video.premium': 'Premium (3 credits)',
        'video.generating_script': 'Generating script with AI...',
        'video.generating_voice': 'Creating voiceover...',
        'video.searching_clips': 'Searching for video clips...',
        'video.composing': 'Composing final video...',
        'video.complete': 'Video generation complete!',
        'video.success': '🎉 Your video is ready!',
        'video.download': '📥 Download Video',
        'video.error': 'Video generation error',
        'gallery.title': '🎞️ My Videos',
        'gallery.empty': 'No videos yet. Create your first video!',
        'gallery.created': 'Created',
        'tabs.create': '🎬 Create',
        'tabs.gallery': '🎞️ Gallery',
        'tabs.about': 'ℹ️ About',
        'about.content': '''
## About NanoTik

NanoTik is an AI-powered video generator that uses cutting-edge technology to create professional videos from simple text prompts.

### How It Works
1. **Choose a Topic**: Tell us what your video should be about
2. **AI Script Generation**: Our AI creates an engaging script
3. **Automated Production**: We generate voiceovers, find clips, and compose your video
4. **Download & Share**: Get your professional video in minutes
        ''',
        'about.features': '✨ Features',
        'about.feature1': '🤖 AI-powered script generation',
        'about.feature2': '💰 Instant Nano cryptocurrency payments',
        'about.feature3': '🌍 Multi-language support (English, Chinese, Arabic)',
        'about.feature4': '📱 Responsive design for all devices',
        'about.feature5': '🎨 Professional quality output',
        'footer.text': '© 2025 NanoTik - Built with ❤️ using Streamlit'
    },
    'zh': {
        'app.subtitle': '基于AI的视频生成器，支持Nano支付',
        'language.select': '语言',
        'credits.balance': '积分',
        'credits.name': '积分',
        'credits.bonus': '奖励',
        'credits.buy': '💰 购买积分',
        'credits.purchase': '购买',
        'credits.info': '💡 积分用于生成视频。不同的质量级别需要不同数量的积分。',
        'credits.costs': '积分消费',
        'credits.insufficient': '⚠️ 积分不足。请购买更多积分以继续。',
        'credits.buy_prompt': '👉 使用侧边栏通过Nano加密货币购买积分。',
        'payment.processing': '正在处理付款...',
        'payment.success': '✅ 付款成功！积分已添加到您的账户。',
        'payment.failed': '❌ 付款失败。请重试。',
        'payment.error': '付款错误',
        'video.generate': '🎬 生成视频',
        'video.topic': '视频主题',
        'video.topic_placeholder': '输入您的视频主题...',
        'video.topic_required': '请输入视频主题。',
        'video.quality': '视频质量',
        'video.duration': '时长（秒）',
        'video.advanced': '⚙️ 高级选项',
        'video.voice': '语音类型',
        'video.music': '添加背景音乐',
        'video.subtitle_position': '字幕位置',
        'video.create': '🚀 创建视频',
        'video.basic': '基础（1积分）',
        'video.hd': '高清（2积分）',
        'video.premium': '专业版（3积分）',
        'video.generating_script': '正在使用AI生成脚本...',
        'video.generating_voice': '正在创建配音...',
        'video.searching_clips': '正在搜索视频片段...',
        'video.composing': '正在合成最终视频...',
        'video.complete': '视频生成完成！',
        'video.success': '🎉 您的视频已准备就绪！',
        'video.download': '📥 下载视频',
        'video.error': '视频生成错误',
        'gallery.title': '🎞️ 我的视频',
        'gallery.empty': '还没有视频。创建您的第一个视频！',
        'gallery.created': '创建于',
        'tabs.create': '🎬 创建',
        'tabs.gallery': '🎞️ 画廊',
        'tabs.about': 'ℹ️ 关于',
        'about.content': '''
## 关于NanoTik

NanoTik是一款由AI驱动的视频生成器，使用尖端技术从简单的文本提示创建专业视频。

### 工作原理
1. **选择主题**：告诉我们您的视频主题
2. **AI脚本生成**：我们的AI创建引人入胜的脚本
3. **自动制作**：我们生成配音、查找片段并合成您的视频
4. **下载和分享**：几分钟内获得专业视频
        ''',
        'about.features': '✨ 特点',
        'about.feature1': '🤖 AI驱动的脚本生成',
        'about.feature2': '💰 即时Nano加密货币支付',
        'about.feature3': '🌍 多语言支持（英语、中文、阿拉伯语）',
        'about.feature4': '📱 适用于所有设备的响应式设计',
        'about.feature5': '🎨 专业质量输出',
        'footer.text': '© 2025 NanoTik - 使用Streamlit构建，充满❤️'
    },
    'ar': {
        'app.subtitle': 'مولد فيديو مدعوم بالذكاء الاصطناعي مع مدفوعات نانو',
        'language.select': 'اللغة',
        'credits.balance': 'الأرصدة',
        'credits.name': 'أرصدة',
        'credits.bonus': 'مكافأة',
        'credits.buy': '💰 شراء الأرصدة',
        'credits.purchase': 'شراء',
        'credits.info': '💡 تُستخدم الأرصدة لإنشاء مقاطع الفيديو. تتطلب مستويات الجودة المختلفة كميات مختلفة من الأرصدة.',
        'credits.costs': 'تكاليف الأرصدة',
        'credits.insufficient': '⚠️ أرصدة غير كافية. يرجى شراء المزيد من الأرصدة للمتابعة.',
        'credits.buy_prompt': '👉 استخدم الشريط الجانبي لشراء الأرصدة باستخدام عملة نانو المشفرة.',
        'payment.processing': 'جاري معالجة الدفع...',
        'payment.success': '✅ تم الدفع بنجاح! تمت إضافة الأرصدة إلى حسابك.',
        'payment.failed': '❌ فشل الدفع. يرجى المحاولة مرة أخرى.',
        'payment.error': 'خطأ في الدفع',
        'video.generate': '🎬 إنشاء فيديو',
        'video.topic': 'موضوع الفيديو',
        'video.topic_placeholder': 'أدخل موضوع الفيديو الخاص بك...',
        'video.topic_required': 'يرجى إدخال موضوع الفيديو.',
        'video.quality': 'جودة الفيديو',
        'video.duration': 'المدة (بالثواني)',
        'video.advanced': '⚙️ خيارات متقدمة',
        'video.voice': 'نوع الصوت',
        'video.music': 'إضافة موسيقى خلفية',
        'video.subtitle_position': 'موضع الترجمة',
        'video.create': '🚀 إنشاء فيديو',
        'video.basic': 'أساسي (رصيد واحد)',
        'video.hd': 'عالي الدقة (رصيدان)',
        'video.premium': 'متميز (3 أرصدة)',
        'video.generating_script': 'جاري إنشاء النص باستخدام الذكاء الاصطناعي...',
        'video.generating_voice': 'جاري إنشاء التعليق الصوتي...',
        'video.searching_clips': 'جاري البحث عن مقاطع الفيديو...',
        'video.composing': 'جاري تركيب الفيديو النهائي...',
        'video.complete': 'اكتمل إنشاء الفيديو!',
        'video.success': '🎉 الفيديو الخاص بك جاهز!',
        'video.download': '📥 تحميل الفيديو',
        'video.error': 'خطأ في إنشاء الفيديو',
        'gallery.title': '🎞️ مقاطع الفيديو الخاصة بي',
        'gallery.empty': 'لا توجد مقاطع فيديو بعد. أنشئ أول فيديو لك!',
        'gallery.created': 'تم الإنشاء',
        'tabs.create': '🎬 إنشاء',
        'tabs.gallery': '🎞️ المعرض',
        'tabs.about': 'ℹ️ حول',
        'about.content': '''
## حول NanoTik

NanoTik هو مولد فيديو مدعوم بالذكاء الاصطناعي يستخدم أحدث التقنيات لإنشاء مقاطع فيديو احترافية من مطالبات نصية بسيطة.

### كيف يعمل
1. **اختر موضوعًا**: أخبرنا عما يجب أن يكون عليه الفيديو الخاص بك
2. **إنشاء النص بالذكاء الاصطناعي**: ينشئ الذكاء الاصطناعي لدينا نصًا جذابًا
3. **الإنتاج الآلي**: ننشئ التعليقات الصوتية ونجد المقاطع ونركب الفيديو الخاص بك
4. **التنزيل والمشاركة**: احصل على الفيديو الاحترافي الخاص بك في دقائق
        ''',
        'about.features': '✨ الميزات',
        'about.feature1': '🤖 إنشاء النصوص بالذكاء الاصطناعي',
        'about.feature2': '💰 مدفوعات فورية بعملة نانو المشفرة',
        'about.feature3': '🌍 دعم متعدد اللغات (الإنجليزية، الصينية، العربية)',
        'about.feature4': '📱 تصميم متجاوب لجميع الأجهزة',
        'about.feature5': '🎨 إخراج بجودة احترافية',
        'footer.text': '© 2025 NanoTik - بُني بـ❤️ باستخدام Streamlit'
    }
}

_current_language = 'en'


def get_text(key: str, language: Optional[str] = None) -> str:
    """
    Get translated text for a given key
    
    Args:
        key: Translation key in dot notation (e.g., 'app.subtitle')
        language: Language code (defaults to current language)
    
    Returns:
        Translated text or the key if not found
    """
    lang = language if language is not None else _current_language
    
    if lang not in TRANSLATIONS:
        lang = 'en'
    
    return TRANSLATIONS[lang].get(key, key)


def set_language(language: str):
    """Set the current application language"""
    global _current_language
    if language in SUPPORTED_LANGUAGES:
        _current_language = language
