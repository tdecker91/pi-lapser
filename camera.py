#from picamera import PiCamera

class Camera:

	def __init__(self, width, height):
		#self.camera = PiCamera()
		#self.camera.resolution = (width, height)
		print "Camera created {} x {}".format(width, height)

	def take_picture(self, file):
		#self.camera.capture(file)
		print "Picture saved to {}".format(file)