import struct
import time
import numpy as np
from PIL import Image
import pdb

from color_utils import *
import csv_bin_reader as bin_r
from moderation import *


format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack
pack_pixel = struct.Struct(format).pack

if __name__ == "__main__":
	start = time.time()
	generate_circles(25)

	pixel_array = np.zeros((2000, 3000), dtype=np.uint8)
	frequency_array = np.zeros((2000, 3000), dtype=np.uint32)

	#file_path = "./data/2023_place_canvas_history_2i2hB.bin"
	file_path = "data/test_dataset.bin"

	with open(file_path, 'rb') as binary_file:
		while True:
			#read in the next 13 bytes for the next pixel
			packed_data = binary_file.read(buffer_size)
			# stops if nothing read anymore
			if not packed_data:
				break
			# unpack pixel data with predefined format
			timestamp, user_id, x, y, x2, y2, color_id = unpack_pixel(packed_data)

			if x2 == 0:
				pixel_array[y + 1000, x + 1500] = color_id
				frequency_array[y + 1000, x + 1500] += 1
			else:
				place_moderation(pixel_array, x, y, x2, y2, color_id)
				

	image_array = convert_index_to_image_array(pixel_array)
	brightness_scale = bin_r.count_placed_pixels(file_path, buffer_size) / 6000000 * 0.7
	frequency_array = frequency_array / (frequency_array + brightness_scale)
	stacked_frequency_array = np.repeat(frequency_array [:, :, None], 3, axis=2) 
	heat_map = (image_array * stacked_frequency_array).astype(np.uint8)
	canvas = Image.fromarray(heat_map)

	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()

	canvas.show()