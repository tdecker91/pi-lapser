import time
import threading
from camera import Camera
from events import RepeatingEvent

MIN_INTERVAL = 5
DEFAULT_INTERVAL = 60
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080

class Snapshotter(object):

	def __init__(self, interval=DEFAULT_INTERVAL, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
		self.camera = Camera(width, height)
		self.interval = interval
		self.started_at = 0
		self.next = 0

	def start(self):
		if self.is_running():
			print "Snapshotter already running"
			return

		self.started_at = time.time()
		self.thread = threading.Thread(target=self.run)
		self.repeater = RepeatingEvent(self.started_at, self.interval)

		print "Starting snapshotter at {}".format(self.started_at)
		self.thread.start()

	def stop(self):
		if self.is_running():
			print "Stopping snapshotter"
			self.started_at = 0
			self.next = 0
			self.thread.join()

	def is_running(self):
		return self.started_at > 0

	def get_next_time(self):
		if self.next > 0:
			return time.ctime(int(self.next))
		else:
			return "n/a"

	def save_snapshot(self):
		filepath = "snapshots/{}.jpg".format(time.strftime("%Y%m%d-%H%M%S"))
		self.camera.take_picture(filepath)

	def wait_for_next_snapshot(self):
		while time.time() < self.next:

			if not self.is_running():
				break

			time_until_next = self.next - time.time()

			if time_until_next < MIN_INTERVAL:
				time.sleep(time_until_next)
			else:
				time.sleep(MIN_INTERVAL)

	def run(self):
		while self.is_running():
			self.save_snapshot()

			self.next = self.repeater.next()
			self.wait_for_next_snapshot()

		print "snapshot loop exiting"

if __name__ == "__main__":
	snapshotter = Snapshotter()
	snapshotter.start()