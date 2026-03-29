# API Yapılandırması
API_CONFIG = {
    "url": "https://api.moonshot.cn/v1/chat/completions",
    "model": "kimi-k2-5",
    "timeout": 30
}

# Model Limitleri (Ücretsiz Tier)
LIMITS = {
    "kimi": {"rpm": 15, "description": "15 istek/dakika"},
    "gemini": {"rpm": 60, "description": "60 istek/dakika"},
    "openrouter": {"daily": 20, "description": "20 istek/gün"}
}

# Varsayılan Promptlar
DEFAULT_PROMPTS = {
    "python": "Python ile {task} yaz",
    "flask": "Flask ile {task} API'si yaz",
    "react": "React ile {task} komponenti yaz"
}
