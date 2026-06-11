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

@app.route('/webhook', methods=['POST'])
def order_webhook():
    data = request.json
    if not data:
        return "No data", 400
    
    orders = data.get('orders', [data])
    
    for order in orders:
        message = f"""
🛒 *Naya Order Aaya!*

🆔 Order ID: `{order.get('id', 'N/A')}`
📦 Service ID: `{order.get('service_id', 'N/A')}`
🔢 Quantity: `{order.get('quantity', 'N/A')}`
🔗 Link: `{order.get('link', 'N/A')}`
🔑 External ID: `{order.get('external_id', 'N/A')}`
📅 Date: `{order.get('date', 'N/A')}`
📊 Status: `{order.get('status', 'N/A')}`
"""
        send_telegram(message)
    return "OK", 200

@app.route('/payment', methods=['POST'])
def payment_webhook():
    data = request.json
    if not data:
        return "No data", 400
    message = f"""
💰 *Naya Payment Aaya!*

👤 User: `{data.get('user', 'N/A')}`
💵 Amount: `{data.get('amount', 'N/A')}`
💳 Method: `{data.get('method', 'N/A')}`
📅 Date: `{data.get('date', 'N/A')}`
✅ Status: `{data.get('status', 'N/A')}`
"""
    send_telegram(message)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
