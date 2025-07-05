from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "uA4h6p9z2m@rk3"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Invalid token", 403

    elif request.method == 'POST':
        data = request.json
        print("Received:", data)
        return "Webhook received", 200

if __name__ == '__main__':
    app.run()
