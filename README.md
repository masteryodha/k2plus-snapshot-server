# Introduction 

The K2 camera is such a pain to be able to view it everywhere (browser, creatlity print on android) and I wanted to show the camera in home assistant.  This docker / python script is able with playwrigth to open the camera feed in a browser and than take a snapshot.

# Build the docker

'''
docker build -t k2plus-snapshot-server:1.0 .

docker login
docker push mikamap/k2plus-snapshot-server:1.0

'''

# Usage

'''
docker run -d -e CAM_URL="http://192.168.3.85:8000/" -e INTERVAL=5 -p 5011:5000 k2plus-snapshot-server:1.0

'''

| Parameters | Mandatory |  Description |
|:-----|:--------:|:--------:|
| CAM_URL   | Yes | URL of the creality K2 plus camera.  Default value = 192.168.3.85:8000/ |
| INTERVAL  | No |  Refresh rate of the snapshot.  Default value = 5  |

# Output

The snapshot is serve on http://IP:5000/snapshot.jpg

# Home assistant

To show the snapshot in home assistant, you need to add the "generic camera" intergration with the snapshot URL.