import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
URL = os.environ["TARGET_URL"]

def notify_discord(message: str):
    requests.post(WEBHOOK, json={"content": message})

def check_resale():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    no_ticket = soup.find(string=lambda s: "現在販売中のチケット情報はありません" in s)

    if no_ticket:
        print("No resale tickets.")
        return

    notify_discord(f"🎫 リセール在庫が出たよ！\n{URL}")
    print("Resale ticket found!")

if __name__ == "__main__":
    check_resale()
