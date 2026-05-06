import os
import requests
from bs4 import BeautifulSoup

stocks = ["1101", "2330"]

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

headers = {
    "User-Agent": "Mozilla/5.0"
}

messages = []

for stockid in stocks:
    try:
        url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        price = price_tag.text if price_tag else "抓不到"

        messages.append(f"{stockid}: {price}")

    except Exception:
        messages.append(f"{stockid}: 錯誤")

msg = "📊 股價更新\n" + "\n".join(messages)

res = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": msg}
)

print(res.status_code)
print(res.text)
