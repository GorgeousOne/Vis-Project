import struct
import time
import numpy as np
from PIL import Image
import pdb

from color_utils import *
from time_utils import *
import csv_bin_reader as bin_r
from moderation import *
import os

format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack
pack_pixel = struct.Struct(format).pack


def save_thermal_image(frequency_array, path):
	thermal_map = replace_with_thermal_colors(frequency_array)
	canvas = Image.fromarray(thermal_map)
	canvas.save(path)

def main():
	start = time.time()

	frequency_stack = []
	frequency_array = np.zeros((2000, 3000), dtype=np.uint32)
	frequency_sum = np.zeros((2000, 3000), dtype=np.uint32)

	file_path = "./data/2023_place_canvas_history_2I4hB.bin"
	target = "data/thermal_map2"

	if not os.path.exists(target):
		os.makedirs(target)

	interval = time_to_ms(0, 5)
	interval_limit = interval

	#brightness_scale = bin_r.count_placed_pixels(file_path, buffer_size) / 6000000 * 0.2
	i = 0

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
				print(f"{i/1543 * 100:.2f}%, {(time.time() - start):.1f}s")
				i += 1
				interval_limit += interval
				frequency_sum += frequency_array
				frequency_stack.append(frequency_array.copy())

				if (len(frequency_stack) > 12):
					frequency_sum -= frequency_stack.pop(0)

				save_thermal_image(frequency_sum, f"{target}/thermal_{timestamp_to_str(interval_limit)}.png")
				frequency_array.fill(0)

			if x2 == 0:
				frequency_array[y + 1000, x + 1500] += 1

	save_thermal_image(frequency_array, f"{target}/thermal_{timestamp_to_str(interval_limit)}.png")
	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()

if __name__ == "__main__":
	main()