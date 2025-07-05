from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = 'uAhfHg9zcm9gHk3'

@app.route("/", methods=["GET", "POST", "HEAD"])
def webhook():
    if request.method == "HEAD":
        return '', 200

    if request.method == "GET":
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        elif mode or token or challenge:
            return 'Verification token mismatch', 403
        else:
            return 'Webhook is live and ready to receive POST requests from Facebook!', 200

    if request.method == "POST":
        data = request.get_json()
        print("Webhook received:", data)
        return 'EVENT_RECEIVED', 200

if __name__ == "__main__":
    app.run()
