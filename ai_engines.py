import requests
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class AIResponse:
    content: str
    source: str
    success: bool

class AIManager:
    """Kimi, Gemini, Claude yönetimi"""
    
    def __init__(self, keys: Dict[str, str]):
        self.keys = keys
        self.usage = {"kimi": 0, "gemini": 0, "claude": 0}
    
    def kimi_generate(self, prompt: str) -> AIResponse:
        """Kimi K2.5"""
        try:
            response = requests.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.keys.get('kimi', '')}"},
                json={
                    "model": "kimi-k2-5",
                    "messages": [
                        {"role": "system", "content": "Sen uzman yazılımcısın."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.usage["kimi"] += 1
                return AIResponse(
                    data['choices'][0]['message']['content'],
                    "kimi",
                    True
                )
            return AIResponse(f"Hata: {response.status_code}", "kimi", False)
            
        except Exception as e:
            return AIResponse(str(e), "kimi", False)
    
    def gemini_generate(self, prompt: str) -> AIResponse:
        """Google Gemini"""
        key = self.keys.get('gemini', '')
        if not key:
            return AIResponse("API key yok", "gemini", False)
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            response = requests.post(
                url,
                json={"contents": [{"parts": [{"text": f"Kod yaz: {prompt}"}]}]},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.usage["gemini"] += 1
                return AIResponse(
                    data['candidates'][0]['content']['parts'][0]['text'],
                    "gemini",
                    True
                )
            return AIResponse(f"Hata: {response.status_code}", "gemini", False)
            
        except Exception as e:
            return AIResponse(str(e), "gemini", False)
    
    def claude_generate(self, prompt: str) -> AIResponse:
        """Claude via OpenRouter"""
        key = self.keys.get('openrouter', '')
        if not key:
            return AIResponse("API key yok", "claude", False)
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "HTTP-Referer": "https://meta-ai-app.streamlit.app"
                },
                json={
                    "model": "anthropic/claude-3-haiku",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self.usage["claude"] += 1
                return AIResponse(
                    data['choices'][0]['message']['content'],
                    "claude",
                    True
                )
            return AIResponse(f"Hata: {response.status_code}", "claude", False)
            
        except Exception as e:
            return AIResponse(str(e), "claude", False)
    
    def get_best_code(self, prompt: str) -> str:
        """En iyi kodu seç"""
        # Paralel çalıştır (sırayla)
        results = []
        
        # Kimi dene
        kimi_result = self.kimi_generate(prompt)
        if kimi_result.success:
            results.append(kimi_result)
        
        # Gemini dene
        gemini_result = self.gemini_generate(prompt)
        if gemini_result.success:
            results.append(gemini_result)
        
        # En uzun kodu döndür (genellikle daha iyi)
        if results:
            best = max(results, key=lambda x: len(x.content))
            return f"// Kaynak: {best.source}\n\n{best.content}"
        
        return "❌ Tüm AI'lar başarısız"
