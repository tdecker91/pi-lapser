# pi-lapser
Time lapse utility for the raspberry pi.

## Installation
This must be installed on a raspberry pi with a camera module attached.
Clone or download this repository. Go into the pi-lapser directory.

Install dependecies using pip `sudo pip install -r requirements.txt`

## Configuration
Edit the pi-lapser.ini file to change any defaults. 
```
  [web-server]
  port=80 
  
  [snapshotter]
  autostart=false
  interval=10
  width=1920
  height=1080
```
|Setting|Description|
|---|---|
|port|the port the webserver front end listens on|
|autostart|true if you want to immediately start taking pictures when starting pi-lapser|
|interval|time in seconds in between each picture|
|width|horizontal size of the pictures|
|height|vertical size of the picture|

## Running
Start the app by running the web-server.py file. `sudo python web-server.py`

Open `http://raspberrypi:{{ port }}` in a web browser to see the controll page.

If you want pi-lapser to start when the raspberry pi boots up you can install supervisor.

`sudo apt-get install supervisor`

create a supervisor config file for pi lapser `vi /etc/supervisor/conf.d/pi-lapser.conf` and add the following contents
```
[program:pi-lapser]
directory=[path to pi lapser dir]/pi-lapser
command=python web-server.py
autostart=true
autorestart=false
```

## Making the time lapse

All of the images are saved in the snapshots directory. You can complete the time lapse using image magick to make a gif or something like mencoder to make a video file