import struct
import time
import numpy as np
import os

from color_utils import *
from time_utils import *
from moderation import *


format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack
pack_pixel = struct.Struct(format).pack

def main():
	start = time.time()

	#file_path = "./data/2023_place_canvas_history_2i2hB.bin"
	file_path = "data/2023_place_canvas_history_2I4hB.bin"
	target = "data/real_timeline2"

	if not os.path.exists(target):
		os.makedirs(target)

	interval = time_to_ms(1)
	interval_limit = interval
	pixel_array = np.zeros((2000, 3000), dtype=np.uint8)
	

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
				print(interval_limit)
				save_as_image_paletted(pixel_array, f"{target}/place_{timestamp_to_str(interval_limit)}.png")
				interval_limit += interval

			if x2 == 0:
				pixel_array[y + 1000, x + 1500] = color_id
			else:
				place_moderation(pixel_array, x, y, x2, y2, color_id)

	save_as_image_paletted(pixel_array, f"{target}/place_{timestamp_to_str(interval_limit)}.png")
	print(f"iteration time {(time.time() - start):.1f}")


if __name__ == "__main__":
	main()
