import threading
import time
import os
from flask import Flask, send_file
from playwright.sync_api import sync_playwright

# Lire les variables d'environnement
# URL de la caméra K2 Plus par défaut (http://IPADDRESS:8000/)
# URL de fluidd par défaut (http://IPADDRESS/camera.html)
CAM_URL = os.getenv("CAM_URL", "	http://192.168.3.85/camera.html")
INTERVAL = int(os.getenv("INTERVAL", "5"))

SNAPSHOT_PATH = "snapshot.jpg"
TEMP_PATH = "temp.jpg"
MIN_VALID_SIZE = 50 * 1024  # 50 KB

app = Flask(__name__)

def print_ts(*args, **kwargs):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]", *args, **kwargs)

def snapshot_loop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(CAM_URL)
        time.sleep(3)

        missed_frames = 0
        while True:
            try:
                page.locator("#remoteVideos").screenshot(path=TEMP_PATH)
                size = os.path.getsize(TEMP_PATH)

                if size < MIN_VALID_SIZE:
                    missed_frames += 1
                    print_ts(f"Frame manquée (image trop petite). Consécutives: {missed_frames}", flush=True)
                    if missed_frames >= 5:
                        print_ts("Trop de frames manquées, rafraîchissement de la page...", flush=True)
                        page.reload()
                        time.sleep(3)
                        missed_frames = 0
                else:
                    missed_frames = 0
                    os.replace(TEMP_PATH, SNAPSHOT_PATH)
                    print_ts(f"Snapshot mis à jour ({size/1024:.1f} KB)", flush=True)

            except Exception as e:
                missed_frames += 1
                print_ts("Erreur snapshot :", e, flush=True)
                if missed_frames >= 5:
                    print_ts("Trop d'erreurs de snapshot, rafraîchissement de la page...", flush=True)
                    try:
                        page.reload()
                        time.sleep(3)
                    except Exception as reload_error:
                        print_ts("Erreur lors du rechargement de la page :", reload_error, flush=True)
                    missed_frames = 0

            time.sleep(INTERVAL)

@app.route("/snapshot.jpg")
def serve_snapshot():
    return send_file(SNAPSHOT_PATH, mimetype="image/jpeg")

if __name__ == "__main__":
    t = threading.Thread(target=snapshot_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)
