from flask import Flask, request
import requests

app = Flask(__name__)


VERIFY_TOKEN = "uAhfHg9zcm9gHk3"
PAGE_ACCESS_TOKEN = "EAAKWPfYeZCaoBPAZC79fz7h8ybLZCJm76XNXp50dTHN4r0TXu9RU6EKHV0esgW9uu8WcBPlTfomdCrk9qZAWLZB8PlwXbZC2aAxw4iZBAXtRrVhrhaUm4dTEOlytqFQz06t8folw2QZCjLjgXDnZCUAku5fXXJtWzX9lGRtLZCG4DdzGcww1NsbbRZAAvZA5dNEErM4He0aIlVk8gZCdqFc5AFZCG1eQZDZD"  


SITE_URL = "https://tonsite.tn"  

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


@app.route("/", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Unauthorized", 403

# 📩 Receive Message (POST)
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "entry" in data:
        for entry in data["entry"]:
            for message_event in entry["messaging"]:
                sender_id = message_event["sender"]["id"]

                if "message" in message_event and "text" in message_event["message"]:
                    user_message = message_event["message"]["text"]
                    reply = get_tunisian_reply(user_message)
                    send_message(sender_id, reply)

    return "ok", 200


def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, params=params, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
