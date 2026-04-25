docker build -t creality-snapshot .
docker run -d --name snapshot -p 5000:5000 creality-snapshot


docker run -d -e CAM_URL="http://192.168.3.85:8000/" -e INTERVAL=5 -p 5000:5000 creality-snapshot
