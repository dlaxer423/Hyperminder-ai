#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Kod Yazıcı
Yapay zeka destekli kod üretim uygulaması
Kimi K2.5 API ile çalışır

Author: ÖMER
Date: 2012/05/04
Version: 9.0.0
"""

import streamlit as st
import requests
import os


# -*- coding: utf-8 -*-
"""
META-AI KOD YAZICI
Kimi + Gemini + Claude + Araştırma | Ücretsiz Tier
"""

import streamlit as st
import requests
import os

# ============================================
# SAYFA AYARLARI
# ============================================

st.set_page_config(
    page_title="Meta-AI Kod Yazıcı",
    page_icon="🧠",
    layout="wide"
)

# ============================================
# API KEY YÖNETİMİ
# ============================================

def get_api_keys():
    """Streamlit secrets veya çevre değişkeninden key al"""
    return {
        'kimi': st.secrets.get("KIMI_API_KEY", "") or os.getenv("KIMI_API_KEY", ""),
        'gemini': st.secrets.get("GEMINI_KEY", "") or os.getenv("GEMINI_KEY", ""),
        'openrouter': st.secrets.get("OPENROUTER_KEY", "") or os.getenv("OPENROUTER_KEY", ""),
    }

API_KEYS = get_api_keys()

# ============================================
# AI FONKSİYONLARI
# ============================================

def kimi_generate(prompt: str, api_key: str) -> str:
    """Kimi K2.5 - Ana kod üretici"""
    
    try:
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "kimi-k2-5",
                "messages": [
                    {"role": "system", "content": "Sen uzman yazılımcısın. Temiz, çalışan kod yaz."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 2000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Kimi Hatası: {response.status_code}"
            
    except Exception as e:
        return f"Kimi Bağlantı Hatası: {str(e)}"

def gemini_generate(prompt: str, api_key: str) -> str:
    """Google Gemini - Alternatif kod"""
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        response = requests.post(
            url,
            json={
                "contents": [{
                    "parts": [{"text": f"Kod yaz: {prompt}"}]
                }]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Gemini Hatası: {response.status_code}"
            
    except Exception as e:
        return f"Gemini Bağlantı Hatası: {str(e)}"

def claude_generate(prompt: str, api_key: str) -> str:
    """Claude via OpenRouter - Kod review"""
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://meta-ai-app.streamlit.app",
                "X-Title": "Meta-AI"
            },
            json={
                "model": "anthropic/claude-3-haiku",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Claude Hatası: {response.status_code}"
            
    except Exception as e:
        return f"Claude Bağlantı Hatası: {str(e)}"

# ============================================
# ANA ARAYÜZ
# ============================================

def main():
    # Header
    st.title("🧠 Meta-AI Kod Yazıcı")
    st.markdown("*Kimi + Gemini + Claude | Ücretsiz Tier*")
    
    # API Key Kontrol
    missing = [k for k, v in API_KEYS.items() if not v]
    
    if missing:
        with st.expander("🔑 API Key Gir (En az biri)", expanded=True):
            st.info("""
            **Ücretsiz Key Al:**
            - Kimi: platform.moonshot.cn
            - Gemini: aistudio.google.com/app/apikey  
            - OpenRouter: openrouter.ai/keys
            """)
            
            for key in missing:
                API_KEYS[key] = st.text_input(
                    f"{key.upper()} Key",
                    type="password",
                    key=f"input_{key}"
                )
    
    # Kullanıcı Girdisi
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prompt = st.text_area(
            "Ne kodu yazalım?",
            height=120,
            placeholder="Python FastAPI ile JWT authentication sistemi yaz..."
        )
    
    with col2:
        mode = st.radio(
            "Mod Seç",
            ["⚡ Hızlı (Kimi)", "🔥 Güçlü (Hepsi)"],
            index=0
        )
        st.markdown("---")
        st.caption("Hızlı: 3-5 sn\nGüçlü: 10-15 sn, daha iyi kalite")
    
    # Kod Üret Butonu
    if st.button("🚀 KOD ÜRET", use_container_width=True, type="primary"):
        if not prompt:
            st.error("❌ Prompt gir!")
            return
        
        available = [k for k, v in API_KEYS.items() if v]
        if not available:
            st.error("❌ En az bir API key gir!")
            return
        
        # Progress
        progress = st.progress(0)
        status = st.empty()
        result_area = st.empty()
        
        try:
            if mode == "⚡ Hızlı (Kimi)":
                # Sadece Kimi
                status.text("🚀 Kimi çalışıyor...")
                progress.progress(50)
                
                code = kimi_generate(prompt, API_KEYS['kimi'])
                progress.progress(100)
                
                if not code.startswith("Hata"):
                    result_area.code(code, language='python')
                    status.success("✅ Tamamlandı!")
                    
                    # İndirme
                    st.download_button(
                        "📥 Python Dosyası İndir",
                        code,
                        file_name="kod.py",
                        mime="text/plain"
                    )
                else:
                    st.error(code)
                    
            else:
                # Güçlü mod - Hepsi
                results = {}
                
                # 1. Kimi
                if API_KEYS['kimi']:
                    status.text("🚀 Kimi: Kod üretiyor...")
                    progress.progress(25)
                    results['kimi'] = kimi_generate(prompt, API_KEYS['kimi'])
                
                # 2. Gemini
                if API_KEYS['gemini']:
                    status.text("🔥 Gemini: Alternatif üretiyor...")
                    progress.progress(50)
                    results['gemini'] = gemini_generate(prompt, API_KEYS['gemini'])
                
                # 3. Claude - Birleştir
                if API_KEYS['openrouter'] and len(results) > 0:
                    status.text("🧠 Claude: En iyisini seçiyor...")
                    progress.progress(75)
                    
                    merge_prompt = f"""
                    En iyi kodu seç ve iyileştir:
                    
                    SEÇENEK 1 (Kimi):
                    {results.get('kimi', '')[:800]}
                    
                    SEÇENEK 2 (Gemini):
                    {results.get('gemini', '')[:800]}
                    
                    Görev: Hataları düzelt, optimize et, tek kod döndür.
                    """
                    
                    final_code = claude_generate(merge_prompt, API_KEYS['openrouter'])
                else:
                    final_code = results.get('kimi', results.get('gemini', 'Kod üretilemedi'))
                
                progress.progress(100)
                
                if not final_code.startswith("Hata"):
                    result_area.code(final_code, language='python')
                    status.success("✅ Tüm AI'lar tamamlandı!")
                    
                    st.download_button(
                        "📥 Python Dosyası İndir",
                        final_code,
                        file_name="meta_ai_kod.py",
                        mime="text/plain"
                    )
                else:
                    st.error(final_code)
                    
        except Exception as e:
            st.error(f"❌ Sistem Hatası: {str(e)}")
    
    # Sidebar Bilgi
    with st.sidebar:
        st.header("ℹ️ Hakkında")
        st.markdown("""
        **Meta-AI Sistemi:**
        
        🚀 **Kimi K2.5**
        - Ana kod üretici
        - 15 istek/dakika ücretsiz
        
        🔥 **Gemini 1.5 Flash**
        - Alternatif yaklaşım
        - 60 istek/dakika ücretsiz
        
        🧠 **Claude 3 Haiku**
        - Kod review & birleştirme
        - OpenRouter ücretsiz tier
        
        **Modlar:**
        - **Hızlı**: Tek AI, 3-5 saniye
        - **Güçlü**: Paralel AI, 10-15 saniye
        """)

if __name__ == "__main__":
    main()
 ...
 