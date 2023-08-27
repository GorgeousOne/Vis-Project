import struct
import time
import numpy as np
from PIL import Image

from time_utils import *
import csv_bin_reader as bin_r
from moderation import *
from datetime import timezone

format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack
pack_pixel = struct.Struct(format).pack

def main():
	start = time.time()
	frequency_array = np.zeros((2000, 3000), dtype=np.uint32)

	file_path = "./data/2023_place_canvas_history_2I4hB.bin"
	#file_path = "data/test_dataset.bin"

	start = get_timestamp(datetime(2023, 7, 24, hour=17, tzinfo=timezone.utc))
	end = get_timestamp(datetime(2023, 7, 24, hour=18, tzinfo=timezone.utc))

	with open(file_path, 'rb') as binary_file:
		binary_file.seek(98571987 * buffer_size)
		while True:
			packed_data = binary_file.read(buffer_size)
			if not packed_data:
				break
			timestamp, user_id, x, y, x2, y2, color_id = unpack_pixel(packed_data)

			if timestamp < start:
				continue
			
			frequency_array[y][x] += 1
			if timestamp >= end:
				np.savetxt("data/pixel_frequencies_7_24_17-18.txt", frequency_array, fmt='%i')
				exit()

	print(f"iteration time {(time.time() - start):.1f}")

if __name__ == "__main__":
	main()