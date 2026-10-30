import os
import time
from collections import defaultdict
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
allowed = [s.strip() for s in os.getenv('ALLOWED_ORIGINS','').split(',') if s.strip()]
CORS(app, resources={r'/api/chat': {'origins': allowed or []}})
requests_by_ip = defaultdict(list)

@app.get('/health')
def health():
    return jsonify(ok=True)

@app.post('/api/chat')
def chat():
    origin = request.headers.get('Origin','')
    if not allowed or origin not in allowed:
        return jsonify(error='Origin not allowed'), 403
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or '').split(',')[0].strip()
    now = time.time()
    requests_by_ip[ip] = [t for t in requests_by_ip[ip] if now-t<3600]
    if len(requests_by_ip[ip]) >= 20:
        return jsonify(error='Hourly limit exceeded'), 429
    requests_by_ip[ip].append(now)
    data = request.get_json(silent=True) or {}
    msg = str(data.get('message',''))[:3000].strip()
    context = str(data.get('context',{}))[:2000]
    if not msg:
        return jsonify(error='Missing message'), 400
    api_key = os.getenv('OPENAI_API_KEY','')
    if not api_key:
        return jsonify(error='AI not configured'), 503
    try:
        r = requests.post('https://api.openai.com/v1/chat/completions',headers={'Authorization':'Bearer '+api_key,'Content-Type':'application/json'},json={'model':os.getenv('OPENAI_MODEL','gpt-4.1-mini'),'messages':[{'role':'system','content':'أنت مساعد تربوي باللغة العربية. حضّر دروسًا مناسبة للمرحلة المتوسطة مع الأهداف والتهيئة والأنشطة والتقويم ومراعاة الفروق الفردية. لا تدّع مطابقة منهج محدد دون نصه. تجنب جمع بيانات شخصية عن الطالبات.'},{'role':'user','content':msg+'\nالسياق: '+context}],'max_tokens':1300},timeout=40)
        r.raise_for_status()
        return jsonify(reply=r.json()['choices'][0]['message']['content'])
    except Exception:
        return jsonify(error='AI service unavailable'), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT','10000')))
