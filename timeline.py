import struct
import time
import numpy as np
from PIL import Image

from color_palette import *
from moderation import *


def time_to_ms(hours, minutes=0, seconds=0):
	return ((((hours * 60) + minutes) * 60) + seconds) * 1000
	

format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack
pack_pixel = struct.Struct(format).pack

def main():
	start = time.time()

	#file_path = "./data/2023_place_canvas_history_2i2hB.bin"
	file_path = "data/test_dataset.bin"

	interval = time_to_ms(8)
	current_max_time = interval
	pixel_array = np.zeros((2000, 3000), dtype=np.uint8)
	generate_circles(20)
	print(current_max_time)
	
	with open(file_path, 'rb') as binary_file:
		while True:
			#read in the next 13 bytes for the next pixel
			packed_data = binary_file.read(buffer_size)
			# stops if nothing read anymore
			if not packed_data:
				break
			# unpack pixel data with predefined format
			timestamp, user_id, x, y, x2, y2, color_id = unpack_pixel(packed_data)

			if timestamp >= current_max_time:
				print(current_max_time)
				image_array = convert_index_to_image_array(pixel_array)
				canvas = Image.fromarray(image_array)
				canvas.save(f"data/timeline/place_{current_max_time}.png")
				current_max_time += interval
				
			if x2 == 0:
				pixel_array[y + 1000, x + 1500] = color_id
			else:
				place_moderation(pixel_array, x, y, x2, y2, color_id)


	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()

	
if __name__ == "__main__":
	main()
