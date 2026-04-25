FROM python:3.11-slim

# Dépendances système pour Chromium + Xvfb
RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates \
    xvfb \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Installer Playwright + Chromium
RUN pip install playwright && playwright install chromium

# Copier le code
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

# Lancer Xvfb + ton script
CMD xvfb-run -s "-screen 0 1280x720x24" python app.py
