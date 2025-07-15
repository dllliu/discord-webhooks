import time
import requests
from bs4 import BeautifulSoup
import os

PRODUCT_SHIRT_URL = "https://usstore.coldplay.com/products/2025-music-of-the-spheres-world-tour-heart-logo-tee?variant=44220174303285"

PRODUCT_HOODIE_URL = "https://usstore.coldplay.com/products/2025-music-of-the-spheres-world-tour-heart-hoodie-copy?variant=44220174073909"

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

TIMEOUT = 600  # in seconds

def is_medium_available(PRODUCT_URL):
    try:
        response = requests.get(PRODUCT_URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for the correct submit button by ID or class
        button = soup.find("button",
                           id=lambda x:
                           x and "ProductSubmitButton" in x)
        if button:
            is_disabled = 'disabled' in button.attrs
            button_text = button.get_text(strip=True).upper()

            if not is_disabled and "SOLD OUT" not in button_text:
                return True  # Medium is in stock
        return False  # Sold out
    except Exception as e:
        print(f"❌ Error checking product: {e}")
        return False

def send_discord_message(message):
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            # Only print errors to console as fallback
            print("Discord error:", response.status_code, response.text)
    except Exception as e:
        # Only print errors to console as fallback
        print("Error sending Discord message:", e)

def send_discord_alert(PRODUCT_URL):
    send_discord_message(
        f"🚨 **@everyone Product is BACK IN STOCK!** [Buy it here]({PRODUCT_URL})"
    )

def send_status_message(message):
    send_discord_message(f"📦 {message}")

if __name__ == "__main__":
    # send_status_message(
    #     "🔍 Stock monitoring started for Coldplay Medium T-shirt and Hoodie.")

    if is_medium_available(PRODUCT_SHIRT_URL):
        print("Shirt is in stock! Sending Discord alert...")
        send_discord_alert(PRODUCT_SHIRT_URL)
    else:
        print(
            f"Product still out of stock. Checking again in {TIMEOUT/60} minutes..."
        )
    if is_medium_available(PRODUCT_HOODIE_URL):
        print("Hoodie is in stock! Sending Discord alert...")
        send_discord_alert(PRODUCT_HOODIE_URL)
    else:
        print(
            f"Product still out of stock. Checking again in {TIMEOUT/60} minutes..."
        )

