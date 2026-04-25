# Introduction 

The K2 camera is such a pain to be able to view it everywhere (browser, creatlity print on android) and I wanted to show the camera in home assistant.  This docker / python script is able with playwrigth to open the camera feed in a browser and than take a snapshot.

# Build the docker

'''
docker build -t creality-snapshot .
'''

# Usage

'''
docker run -d -e CAM_URL="http://192.168.3.85:8000/" -e INTERVAL=5 -p 5000:5000 creality-snapshot
'''

# Output

The snapshot is serve on http://IP:5000/snapshot.jpg

# Home assistant

To show the snapshot in home assistant, you need to add the "generic camera" intergration with the snapshot URL.