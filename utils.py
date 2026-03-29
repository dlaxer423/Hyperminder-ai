def validate_inputs(api_key: str, prompt: str) -> bool:
    """Input doğrulama"""
    import streamlit as st
    
    if not api_key:
        st.error("❌ API key gir!")
        return False
    
    if not prompt or len(prompt.strip()) < 3:
        st.error("❌ Prompt çok kısa!")
        return False
    
    return True

def format_code(code: str) -> str:
    """Kodu formatla"""
    # Başlangıç ve sondaki boşlukları temizle
    return code.strip()

def estimate_complexity(code: str) -> str:
    """Kod karmaşıklığını tahmin et"""
    lines = len(code.split('\n'))
    if lines < 20:
        return "Basit"
    elif lines < 100:
        return "Orta"
    else:
        return "Karmaşık"
