import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

class TimelineViewer:

	def __init__(self, image_folder):
		self.image_folder = image_folder
		self.image_arrays = []
		self.current_index = 0
		self.canvas = None

		self._preload_images()
		self._show()

	def _preload_images(self):
		# Get a list of image file names in the folder
		image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png'))]
		self.image_arrays = [Image.open(os.path.join(self.image_folder, f)) for f in image_files]
		print("loaded images")

	# Create a function to update the displayed image
	def update_image(self, val):
		self.current_index = int(val)
		self.canvas.set_data(self.image_arrays[self.current_index])

	def _show(self):
		fig, ax = plt.subplots()
		plt.subplots_adjust(bottom=0.25)

		# display the initial image
		self.canvas = ax.imshow(self.image_arrays[self.current_index])
		# Create a slider
		num_images = len(self.image_arrays)
		ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
		slider = Slider(ax_slider, 'Image', 0, num_images - 1, valinit=self.current_index, valstep=1)
		slider.on_changed(self.update_image)

		# Display the plot
		plt.show()


if __name__ == "__main__":
	TimelineViewer("data/real_timeline")