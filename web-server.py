import os.path
import sys
import signal
import configparser

from flask import Flask, redirect, Response, render_template
from flask_autoindex import AutoIndex
from snapshotter import Snapshotter

app = Flask(__name__)
idx = AutoIndex(app, os.path.join(os.path.curdir, 'snapshots'), add_url_rules=False)

snapshotter = None

@app.route('/snapshots')
@app.route('/snapshots/<path:path>')
def autoindex(path='.'):
        return idx.render_autoindex(path)

@app.route('/')
def index():
	return render_template('index.html', snapping=snapshotter.is_running(), interval=snapshotter.interval, next=snapshotter.get_next_time())

@app.route('/snapshotter/start')
def start():
	snapshotter.start()
	return redirect('/')

@app.route('/snapshotter/stop')
def stop():
	snapshotter.stop()
	return redirect('/')

def sigint_handler(signal, frame):
	snapshotter.stop()
	sys.exit(0)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)

	config = configparser.ConfigParser()
	config.read('pi-lapser.ini')

	interval = config.getint('snapshotter', 'interval')
	width = config.getint('snapshotter', 'width')
	height = config.getint('snapshotter', 'height')

	snapshotter = Snapshotter(interval=interval, width=width, height=height)

	if config.getboolean('snapshotter', 'autostart'):
		snapshotter.start()

	app.run(host='0.0.0.0', port=config.getint('web-server', 'port'))