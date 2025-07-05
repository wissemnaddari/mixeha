from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "uAhfHg9zcm9gHk3"
PAGE_ACCESS_TOKEN = "EAAKWPfYeZCaoBPAZC79fz7h8ybLZCJm76XNXp50dTHN4r0TXu9RU6EKHV0esgW9uu8WcBPlTfomdCrk9qZAWLZB8PlwXbZC2aAxw4iZBAXtRrVhrhaUm4dTEOlytqFQz06t8folw2QZCjLjgXDnZCUAku5fXXJtWzX9lGRtLZCG4DdzGcww1NsbbRZAAvZA5dNEErM4He0aIlVk8gZCdqFc5AFZCG1eQZDZD"
SITE_URL = "https://tonsite.tn"

@app.route("/", methods=["GET"])
def handle_get():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified")
        return challenge, 200

    return """
    <h3>👋 Welcome to Mixeha Bot Webhook</h3>
    <p>This endpoint is running and ready to receive messages from Facebook Messenger.</p>
    <p>If you see this page, the bot is deployed correctly ✅</p>
    """

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Received webhook data:", data)

    if "entry" in data:
        for entry in data["entry"]:
            messaging_events = entry.get("messaging", [])
            for event in messaging_events:
                sender_id = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    user_message = event["message"]["text"]
                    reply = get_tunisian_reply(user_message)
                    send_message(sender_id, reply)

    return "ok", 200

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    print(f"📤 Sent message to {recipient_id}: {message_text}")
    print("📡 Facebook response:", response.status_code, response.text)

def get_tunisian_reply(message_text):
    text = message_text.lower()

    if any(word in text for word in ["سعر", "قداه", "بشحال", "prix", "الميكسور"]):
        return f"الميكسور بـ50 دينار 🇹🇳 تشوف التفاصيل وتعمل commande من الموقع: {SITE_URL} 🛍️"

    elif any(word in text for word in ["نحب نشري", "نطلب", "commande", "أوردر", "أطلب"]):
        return f"باش تشري، تنجم تعمل commande من هنا: {SITE_URL} 📦"

    elif any(word in text for word in ["توصيل", "توصلكم", "livraison"]):
        return "نوصّلو لكل بلاصة في تونس 🇹🇳 بعد ما تعمل commande من الموقع متاعنا ✨"

    elif any(word in text for word in ["سلام", "هلا", "مرحبا", "خويا", "أختي"]):
        return "مرحبا بيك في Mixeha 😄 تحب تعرف على الميكسور ولا تعمل commande؟"

    elif any(word in text for word in ["شكرا", "مرسي", "thx", "merci", "يعطيك الصحة"]):
        return "يعطيك الصحة 🙌 تلوج على حاجة أخرى؟"

    else:
        return f"ما فهمتش سؤالك 😅 أما تنجم تلقى كل شي في موقعنا: {SITE_URL}"

if __name__ == "__main__":
    app.run(debug=True)
