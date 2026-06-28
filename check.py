import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URLS = [
    "https://t.pia.jp/pia/ticketInformation.do?eventCd=2604917&rlsCd=001",
    "https://t.pia.jp/pia/ticketInformation.do?eventCd=2604917&rlsCd=002",
]

KEYWORD = "リセール情報"

def notify_discord(message: str):
    requests.post(WEBHOOK, json={"content": message})

def check_resale():
    found = False
    found_urls = []

    for url in URLS:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # ページ内にキーワードがあるかチェック
        if soup.find(string=lambda s: KEYWORD in s):
            found = True
            found_urls.append(url)

    if found:
        msg = "🎫 リセールチケットが見つかったよ！\n"
        for u in found_urls:
            msg += f"- {u}\n"
        notify_discord(msg)
        print("Resale ticket found!")
    else:
        print("No resale tickets.")

if __name__ == "__main__":
    check_resale()
