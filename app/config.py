"""
Configuration management for NanoTik
Loads settings from environment variables and config files
"""

import os
import toml
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables and config file
    Priority: Environment variables > config.toml > config.example.toml
    """
    config = {}
    
    # Try to load from config.toml first
    config_path = Path('config.toml')
    example_config_path = Path('config.example.toml')
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
    elif example_config_path.exists():
        with open(example_config_path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
    
    # Override with environment variables
    config['app'] = config.get('app', {})
    config['azure'] = config.get('azure', {})
    config['video'] = config.get('video', {})
    config['payment'] = config.get('payment', {})
    
    # LLM Configuration
    config['app']['llm_provider'] = os.getenv('LLM_PROVIDER', config['app'].get('llm_provider', 'openrouter'))

    # OpenRouter Configuration
    config['app']['openrouter_api_key'] = os.getenv('OPENROUTER_API_KEY', config['app'].get('openrouter_api_key', ''))
    config['app']['openrouter_model_name'] = os.getenv('OPENROUTER_MODEL_NAME', config['app'].get('openrouter_model_name', 'google/gemini-2.0-flash-001'))

    # OpenAI Configuration
    config['app']['openai_api_key'] = os.getenv('OPENAI_API_KEY', config['app'].get('openai_api_key', ''))
    config['app']['deepseek_api_key'] = os.getenv('DEEPSEEK_API_KEY', config['app'].get('deepseek_api_key', ''))
    config['app']['moonshot_api_key'] = os.getenv('MOONSHOT_API_KEY', config['app'].get('moonshot_api_key', ''))
    config['app']['openai_base_url'] = os.getenv('OPENAI_BASE_URL', config['app'].get('openai_base_url', 'https://api.openai.com/v1'))
    config['app']['openai_model_name'] = os.getenv('OPENAI_MODEL_NAME', config['app'].get('openai_model_name', 'gpt-4'))
    
    # Azure Speech Configuration
    config['azure']['speech_key'] = os.getenv('AZURE_SPEECH_KEY', config['azure'].get('speech_key', ''))
    config['azure']['speech_region'] = os.getenv('AZURE_SPEECH_REGION', config['azure'].get('speech_region', 'eastus'))
    
    # Video Source Configuration
    pexels_keys = os.getenv('PEXELS_API_KEYS', '')
    if pexels_keys:
        config['app']['pexels_api_keys'] = pexels_keys.split(',')
    else:
        config['app']['pexels_api_keys'] = config['app'].get('pexels_api_keys', [])
    
    pixabay_keys = os.getenv('PIXABAY_API_KEYS', '')
    if pixabay_keys:
        config['app']['pixabay_api_keys'] = pixabay_keys.split(',')
    else:
        config['app']['pixabay_api_keys'] = config['app'].get('pixabay_api_keys', [])
    
    # Payment Configuration
    config['payment']['nano_mcp_url'] = os.getenv('NANO_MCP_URL', config['payment'].get('nano_mcp_url', 'https://nano-mcp.replit.app'))
    config['payment']['nano_wallet_address'] = os.getenv('NANO_WALLET_ADDRESS', config['payment'].get('nano_wallet_address', ''))
    
    # Video Configuration
    config['video']['output_dir'] = os.getenv('VIDEO_OUTPUT_DIR', config['video'].get('output_dir', './output'))
    config['video']['temp_dir'] = os.getenv('VIDEO_TEMP_DIR', config['video'].get('temp_dir', './temp'))
    config['video']['max_duration'] = int(os.getenv('VIDEO_MAX_DURATION', config['video'].get('max_duration', 180)))
    config['video']['default_resolution'] = os.getenv('VIDEO_DEFAULT_RESOLUTION', config['video'].get('default_resolution', '1920x1080'))
    
    return config


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a configuration value by key with dot notation
    Example: get_config_value('app.openai_api_key')
    """
    config = load_config()
    keys = key.split('.')
    value = config
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default
    
    return value if value is not None else default


def validate_config() -> tuple[bool, list[str]]:
    """
    Validate that required configuration is present
    Returns: (is_valid, list_of_errors)
    """
    config = load_config()
    errors = []
    
    # Check LLM API keys
    llm_provider = config['app'].get('llm_provider', 'openrouter')
    if llm_provider == 'openrouter' and not config['app'].get('openrouter_api_key'):
        errors.append("OpenRouter API key is required when using OpenRouter as LLM provider")
    elif llm_provider == 'openai' and not config['app'].get('openai_api_key'):
        errors.append("OpenAI API key is required when using OpenAI as LLM provider")
    elif llm_provider == 'deepseek' and not config['app'].get('deepseek_api_key'):
        errors.append("DeepSeek API key is required when using DeepSeek as LLM provider")
    
    # Check video source API keys
    if not config['app'].get('pexels_api_keys') and not config['app'].get('pixabay_api_keys'):
        errors.append("At least one video source API key (Pexels or Pixabay) is required")
    
    # Check Azure Speech key for voice synthesis
    if not config['azure'].get('speech_key'):
        errors.append("Azure Speech API key is required for voice synthesis")
    
    return len(errors) == 0, errors
