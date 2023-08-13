import os
from PIL import Image
import numpy as np
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
mplstyle.use('fast')


class TimelineViewer:

	def __init__(self, image_folder):
		self.image_folder = image_folder
		self.image_files = []
		self.current_index = 0
		self.canvas = None

		self._preload_images()
		self._show()

	def _preload_images(self):
		# Get a list of image file names in the folder
		self.image_files = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if f.lower().endswith(('.png'))]
		print("loaded images")
	
	# Create a function to update the displayed image
	def update_image(self, val):
		self.current_index = int(val)
		img_array = np.asarray(Image.open(self.image_files[self.current_index]).convert("RGBA"))
		#set canvas' internal image data bypassing some expensive checks
		self.canvas._A = img_array
		self.canvas._imcache = img_array

	def _show(self):
		fig, ax = plt.subplots()
		plt.subplots_adjust(bottom=0.25)
		plt.tight_layout()
		
		# display the initial image
		img_array = np.asarray(Image.open(self.image_files[self.current_index]).convert("RGBA"))
		self.canvas = ax.imshow(img_array, interpolation="none")

		# Create a slider
		num_images = len(self.image_files)
		ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
		slider = Slider(ax_slider, 'Image', 0, num_images - 1, valinit=self.current_index, valstep=1)
		slider.on_changed(self.update_image)

		# Display the plot
		plt.show()


if __name__ == "__main__":
	TimelineViewer("data/real_timeline")