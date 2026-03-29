#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Meta-AI Kod Yazıcı</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; height: 100px; margin: 10px 0; }
        input { width: 100%; padding: 10px; margin: 10px 0; }
        button { background: #0066cc; color: white; padding: 15px 30px; border: none; cursor: pointer; }
        pre { background: #f4f4f4; padding: 20px; border-radius: 5px; overflow-x: auto; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>🧠 Meta-AI Kod Yazıcı</h1>
    <form method="POST">
        <input type="password" name="api_key" placeholder="Kimi API Key" required>
        <textarea name="prompt" placeholder="Ne kodu yazalım? (Örn: Python hesap makinesi)" required></textarea>
        <button type="submit">🚀 Kod Üret</button>
    </form>
    {% if result %}
        {% if error %}
            <p class="error">{{ result }}</p>
        {% else %}
            <p class="success">✅ Kod hazır!</p>
            <pre>{{ result }}</pre>
            <a href="data:text/plain;charset=utf-8,{{ result | urlencode }}" download="kod.py">
                <button>📥 İndir</button>
            </a>
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = False
    
    if request.method == "POST":
        api_key = request.form.get("api_key", "").strip()
        prompt = request.form.get("prompt", "").strip()
        
        if not api_key or not prompt:
            result = "❌ API key ve prompt gerekli!"
            error = True
        else:
            try:
                response = requests.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": "kimi-k2-5",
                        "messages": [
                            {"role": "system", "content": "Sen kod yazıcısısın."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.2,
                        "max_tokens": 2000
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data['choices'][0]['message']['content']
                else:
                    result = f"❌ API Hatası: {response.status_code}"
                    error = True
                    
            except Exception as e:
                result = f"❌ Hata: {str(e)}"
                error = True
    
    return render_template_string(HTML, result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
