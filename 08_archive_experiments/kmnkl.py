import requests

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_alert(ph, status):

    if status == "ABNORMAL":

        message = (
            "⚠️ WATER QUALITY ALERT\n\n"
            f"pH: {ph}\n"
            f"Status: {status}\n"
            "Water quality requires attention."
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        requests.post(url, data=data)
        status = model.predict([[ph]])[0]

send_alert(ph, status)
data = [[ph, turbidity, tds, temperature]]

status = model.predict(data)[0]

send_alert(ph, status)