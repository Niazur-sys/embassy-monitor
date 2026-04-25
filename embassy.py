import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8625488979:AAGwF_5XYrYt-F63gn3x1WkhNhbXHrM27b4"
CHAT_ID = 8557488441
URL = "https://broneering.mfa.ee/en/"

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

def check_slots():
    try:
        response = requests.get(URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        no_slot_keywords = ["no available", "no free", "unfortunately"]
        slot_keywords = ["select a time", "choose a time", "pick a date"]

        has_slot = any(k in text for k in slot_keywords)
        no_slot = any(k in text for k in no_slot_keywords)

        if has_slot and not no_slot:
            send_telegram(
                "🚨 SLOT FOUND!\n\n"
                "Estonian Embassy Beijing has a slot!\n\n"
                "👉 BOOK NOW:\n"
                f"{URL}"
            )
            print("🚨 SLOT FOUND! Telegram alert sent!")
        else:
            print(f"No slots yet... {time.strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"Error: {e}")

send_telegram(
    "✅ Embassy Monitor ACTIVE!\n"
    "⚡ Peak hour: 3AM-4AM BD time (every 30 sec)\n"
    "🕐 Normal time: every 2 minutes\n"
    f"🔗 {URL}"
)

print("Monitor started! Check your Telegram.")

while True:
    current_hour = int(time.strftime('%H'))
    if current_hour == 3:
        print(f"⚡ PEAK HOUR 3AM! Checking every 30 seconds...")
        check_slots()
        time.sleep(30)
    else:
        check_slots()
        time.sleep(120)
