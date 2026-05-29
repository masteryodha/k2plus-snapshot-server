# K2Plus Snapshot Server

Un micro‑service Docker permettant de capturer automatiquement des snapshots depuis l’interface Web de la **Creality K2 Plus** (ou tout autre flux WebRTC/HTTP) et de les exposer sous forme d’image JPEG statique.  
Ce service permet une intégration stable dans Home Assistant, go2rtc, Frigate ou tout autre système domotique.

---

## Pourquoi

La caméra de la K2 plus ne propose pas de flux RTSP, donc, très difficle à intégrer dans les outils de domotique.  Pour mon utilisation personnelle j'avais besoin d'afficher une image de la caméra dans Home Assistant, mais les intégrations actuelles ne fonctionnaient pas toujours.  

---

## 🚀 Fonctionnalités

- Capture automatique d’un snapshot depuis la caméra Web de la K2 Plus  
- Filtrage des frames blanches/grises  
- Serveur Flask exposant `/snapshot.jpg`  
- Image “loading” par défaut au démarrage  
- Compatible Home Assistant, go2rtc, Frigate, MotionEye, etc.  
- Conteneur Docker autonome  
- Configuration simple via variables d’environnement  

---

## 🧱 Architecture

Le conteneur utilise :

- **Playwright + Chromium headless** pour charger la page caméra  
- **Xvfb** pour simuler un affichage virtuel  
- **Flask** pour servir l’image  
- Un thread Python qui :
  - charge la page
  - capture un snapshot toutes les X secondes
  - remplace `snapshot.jpg` si l’image est valide

---

## ⚙️ Variables d’environnement

| Variable     | Description |
|--------------|-------------|
| `CAM_URL`    | URL de la caméra (ex: `http://192.168.3.85:8000/`) |
| `INTERVAL`   | Intervalle en secondes entre deux captures (ex: `5`) |

---

## 📡 Endpoint exposé

Le conteneur expose une seule route HTTP : http://IP:5000/snapshot.jpg
Cette image est mise à jour automatiquement selon l’intervalle configuré.

---

## 🔧 Build manuel

### Build local

```bash
docker build -t mikamap/k2plus-snapshot-server:X.X .
```

### Pousser vers DockerHub

```bash
docker login
docker push mikamap/k2plus-snapshot-server:X.X
```

---

## 🐳 Utilisation avec Docker Compose

Exemple de `docker-compose.yml` :

```yaml
version: "3.9"

services:
  snapshot:
    build: .
    image: mikamap/k2plus-snapshot-server:1.0
    container_name: k2plus-snapshot-server
    environment:
      CAM_URL: "http://192.168.3.85:8000/"
      INTERVAL: 5
    ports:
      - "5011:5000"
    restart: unless-stopped
```

---

## 🐳 Utilisation avec docker local

```bash
docker run -d -e CAM_URL="http://192.168.3.85:8000/" -e INTERVAL=5 -p 5011:5000 mikamap/k2plus-snapshot-server:1.0
```

---


## 📦 Structure du projet

```
.
├── app.py
├── Dockerfile
├── requirements.txt
├── snapshot.jpg        # image loading par défaut
└── README.md
```

## 🏠 Intégration Home Assistant

```yaml
camera:
  - platform: generic
    name: K2Plus Snapshot
    still_image_url: "http://192.168.3.50:5011/snapshot.jpg"
    content_type: image/jpeg
```