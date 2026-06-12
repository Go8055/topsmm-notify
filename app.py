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


# ─────────────────────────────────────────
#  ORDERS WEBHOOK  →  /webhook
# ─────────────────────────────────────────
@app.route('/webhook', methods=['POST'])
def order_webhook():
    data = request.json
    if not data:
        return "No data", 400

    orders = data.get('orders', [data])

    for order in orders:
        message = (
            "🛒 *New Order Received!*\n"
            f"🆔 Order ID: `{order.get('id', 'N/A')}`\n"
            f"📦 Service ID: `{order.get('service_id', 'N/A')}`\n"
            f"🔢 Quantity: `{order.get('quantity', 'N/A')}`\n"
            f"🔗 Link: `{order.get('link', 'N/A')}`\n"
            f"📅 Date: `{order.get('date', 'N/A')}`\n"
            f"📊 Status: `{order.get('status', 'N/A')}`"
        )
        send_telegram(message)

    return "OK", 200


# ─────────────────────────────────────────
#  PAYMENTS WEBHOOK  →  /payment
# ─────────────────────────────────────────
@app.route('/payment', methods=['POST'])
def payment_webhook():
    data = request.json
    if not data:
        return "No data", 400

    # Payload comes as {"payments": [...]}
    payments = data.get('payments', [data])

    for payment in payments:
        # status: 1 = Success, 0 = Pending, rest = Unknown
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
            f"🔖 Reference: `{payment.get('reference', 'N/A')}`\n"
            f"💳 Method: `{payment.get('method_id', 'N/A')}`\n"
            f"💵 Amount: `${payment.get('amount', 'N/A')}`\n"
            f"🏦 Old Balance: `${payment.get('old_balance', 'N/A')}`\n"
            f"📅 Date: `{payment.get('date', 'N/A')}`\n"
            f"📊 Status: {status_label}\n"
            f"📝 Details: `{payment.get('details', 'N/A')}`\n"
            f"🖥️ Server Response: `{payment.get('server_response', 'N/A')}`"
        )
        send_telegram(message)

    return "OK", 200


# ─────────────────────────────────────────
#  TASKS WEBHOOK  →  /tasks
# ─────────────────────────────────────────
@app.route('/tasks', methods=['POST'])
def tasks_webhook():
    data = request.json
    if not data:
        return "No data", 400

    # Payload comes as {"tasks": [...]}
    tasks = data.get('tasks', [data])

    for task in tasks:
        method  = task.get('method', 'N/A').upper()
        status  = task.get('status', 'N/A')

        # Emoji for method
        if method == 'REFILL':
            method_emoji = "🔄"
        elif method == 'CANCEL':
            method_emoji = "❌"
        else:
            method_emoji = "⚙️"

        # Emoji for status
        status_lower = str(status).lower()
        if 'complet' in status_lower:
            status_emoji = "✅"
        elif 'progress' in status_lower:
            status_emoji = "⏳"
        elif 'pending' in status_lower:
            status_emoji = "🕐"
        elif 'cancel' in status_lower:
            status_emoji = "🚫"
        else:
            status_emoji = "📊"

        refill_id = task.get('refill_order_id', '') or 'N/A'

        message = (
            f"{method_emoji} *Task Notification — {method}*\n"
            f"🆔 Task ID: `{task.get('task_id', 'N/A')}`\n"
            f"📋 Order ID: `{task.get('order_id', 'N/A')}`\n"
            f"👤 User: `{task.get('username', 'N/A')}` (ID: `{task.get('user_id', 'N/A')}`)\n"
            f"📦 Service: `{task.get('service', 'N/A')}`\n"
            f"🔢 Quantity: `{task.get('quantity', 'N/A')}`\n"
            f"🚀 Start Count: `{task.get('start', 'N/A')}`\n"
            f"🔗 Link: `{task.get('link', 'N/A')}`\n"
            f"🏷️ Type: `{task.get('type', 'N/A')}`\n"
            f"🔁 Refill Order ID: `{refill_id}`\n"
            f"📅 Date: `{task.get('date', 'N/A')}`\n"
            f"{status_emoji} Status: `{status}`"
        )
        send_telegram(message)

    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
