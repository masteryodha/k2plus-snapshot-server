import threading
import time
import os
from flask import Flask, send_file
from playwright.sync_api import sync_playwright

# Lire les variables d'environnement
CAM_URL = os.getenv("CAM_URL", "http://192.168.3.85:8000/")
INTERVAL = int(os.getenv("INTERVAL", "5"))

SNAPSHOT_PATH = "snapshot.jpg"
TEMP_PATH = "temp.jpg"
MIN_VALID_SIZE = 50 * 1024  # 50 KB

app = Flask(__name__)

def snapshot_loop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(CAM_URL)
        time.sleep(3)

        while True:
            try:
                page.locator("#remoteVideos").screenshot(path=TEMP_PATH)
                size = os.path.getsize(TEMP_PATH)

                if size < MIN_VALID_SIZE:
                    print("Frame manquée (image trop petite).", flush=True)
                else:
                    os.replace(TEMP_PATH, SNAPSHOT_PATH)
                    print(f"Snapshot mis à jour ({size/1024:.1f} KB)", flush=True)

            except Exception as e:
                print("Erreur snapshot :", e)

            time.sleep(INTERVAL)

@app.route("/snapshot.jpg")
def serve_snapshot():
    return send_file(SNAPSHOT_PATH, mimetype="image/jpeg")

if __name__ == "__main__":
    t = threading.Thread(target=snapshot_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)
