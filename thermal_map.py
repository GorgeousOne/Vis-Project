import struct
import time
import numpy as np
from PIL import Image
import pdb

from color_utils import *
from time_utils import *
import csv_bin_reader as bin_r
from moderation import *


format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack
pack_pixel = struct.Struct(format).pack


def save_thermal_image(pixel_array, frequency_array, path, brightness_scale):
	minimum_brightness = 0.0
	#image_array = convert_index_to_image_array(pixel_array)	
	frequency_array = (frequency_array / (frequency_array + brightness_scale)) * (1 - minimum_brightness) + minimum_brightness
	#stacked_frequency_array = frequency_array * 255
	#thermal_map = stacked_frequency_array.astype(np.uint8)
	thermal_map = replace_with_thermal_colors(frequency_array)
	canvas = Image.fromarray(thermal_map)
	canvas.save(path)

def main():
	start = time.time()

	pixel_array = np.zeros((2000, 3000), dtype=np.uint8)
	frequency_array = np.zeros((2000, 3000), dtype=np.uint32)

	file_path = "./data/2023_place_canvas_history_2I4hB.bin"
	#file_path = "data/test_dataset.bin"

	interval = time_to_ms(0, 5)
	interval_limit = interval

	#brightness_scale = bin_r.count_placed_pixels(file_path, buffer_size) / 6000000 * 0.2
	brightness_scale = 2

	with open(file_path, 'rb') as binary_file:
		while True:
			#read in the next 13 bytes for the next pixel
			packed_data = binary_file.read(buffer_size)
			# stops if nothing read anymore
			if not packed_data:
				break
			# unpack pixel data with predefined format
			timestamp, user_id, x, y, x2, y2, color_id = unpack_pixel(packed_data)

			if timestamp >= interval_limit:
				# print(current_max_time)
				save_thermal_image(pixel_array, frequency_array, f"data/thermal_map/thermal_{timestamp_to_str(interval_limit)}.png", brightness_scale)
				interval_limit += interval
				frequency_array.fill(0)

			if x2 == 0:
				pixel_array[y + 1000, x + 1500] = color_id
				frequency_array[y + 1000, x + 1500] += 1
			else:
				place_moderation(pixel_array, x, y, x2, y2, color_id)	


	save_thermal_image(pixel_array, frequency_array, f"data/thermal_map/thermal_{timestamp_to_str(interval_limit)}.png", brightness_scale)
	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()

if __name__ == "__main__":
	main()