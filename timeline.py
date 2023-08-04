import struct
import time
import numpy as np
from PIL import Image

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
	file_path = "data/test_dataset.bin"

	interval = time_to_ms(8)
	interval_limit = interval
	pixel_array = np.zeros((2000, 3000), dtype=np.uint8)
	generate_circles(25)
	print(interval_limit)
	
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
				save_as_image(pixel_array, f"data/timeline/place_{interval_limit}.png")
				interval_limit += interval
				
			if x2 == 0:
				pixel_array[y + 1000, x + 1500] = color_id
			else:
				place_moderation(pixel_array, x, y, x2, y2, color_id)


	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()

	
if __name__ == "__main__":
	main()
