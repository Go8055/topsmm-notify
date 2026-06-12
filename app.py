from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    )

@app.route('/payment', methods=['POST'])
def payment_webhook():
    data = request.json
    if not data:
        return "No data", 400

    payments = data.get('payments', [data])

    for payment in payments:
        raw_status = payment.get('status', 'N/A')
        if raw_status == 1:
            status_label = "✅ Success"
        elif raw_status == 0:
            status_label = "⏳ Pending"
        else:
            status_label = f"❓ {raw_status}"

        message = (
            "💰 *New Payment Received!*\n"
            f"🆔 Payment ID: `{payment.get('id', 'N/A')}`\n"
            f"👤 User: `{payment.get('user_name', 'N/A')}` (ID: `{payment.get('user_id', 'N/A')}`)\n"
            f"💳 Method: `{payment.get('method_id', 'N/A')}`\n"
            f"💵 Amount: `₹{payment.get('amount', 'N/A')}`\n"
            f"🏦 Old Balance: `₹{payment.get('old_balance', 'N/A')}`\n"
            f"📅 Date: `{payment.get('date', 'N/A')}`\n"
            f"📊 Status: {status_label}\n"
            f"📝 Details: `{payment.get('details', 'N/A')}`\n"
        )
        send_telegram(message)

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
