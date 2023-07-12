import requests
import time
import json
import os

# Discord Webhook URL
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

# Store the previous product data
previous_data = None

# Endpoint URL
url = "https://www.lttstore.com/collections/all/products.json"

# Interval between checks (in seconds)
interval = 60  # Adjust as needed

def send_discord_notification(product):
    message = {
        "content": "Price Change Detected",
        "embeds": [
            {
                "title": "Product Price Change",
                "description": f"Product: [{product['title']}]({product['url']})\n\nOld Price: {previous_product['price']}\nNew Price: {product['price']}",
                "color": 15746887
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(message), headers=headers)
    if response.status_code != 204:
        print("Failed to send Discord notification.")

def check_price_changes():
    global previous_data

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Check if data has changed
        if previous_data is not None and data != previous_data:
            # Compare the prices
            for product in data["products"]:
                previous_product = next(
                    (p for p in previous_data["products"] if p["id"] == product["id"]),
                    None,
                )
                if previous_product and previous_product["price"] != product["price"]:
                    send_discord_notification(product)

        # Update previous_data
        previous_data = data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

while True:
    check_price_changes()
    time.sleep(interval)
