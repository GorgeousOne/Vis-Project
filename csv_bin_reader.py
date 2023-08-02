import os
import struct
import time
from datetime import datetime

from color_palette import color_to_index


def timestamp_to_datetime(timestamp):
	return datetime.fromtimestamp(timestamp * 0.001)


def count_placed_pixels(file_path, pixel_byte_count):
	file_size = os.path.getsize(file_path)
	return file_size // pixel_byte_count


def get_color_frequency(binary_file):
	occurences = [0 for i in range(len(color_to_index))]
	unpack_color = struct.Struct("B").unpack_from
	
	while True:
		packed_data = binary_file.read(13)

		if not packed_data:
			break
		color_idx = unpack_color(packed_data, 12)[0]
		occurences[color_idx] += 1
	print(occurences)


def create_test_dataset(binary_file):
	"""saves 1% of that 132,000,000 entries"""
	with open("./data/test_dataset.bin", "wb") as out_file:
		while True:
			data = binary_file.read(13)
			if not data:
				break
			out_file.write(data)
			binary_file.seek(1287, 1)

# precompile unpacking formats
# list of format characters: https://docs.python.org/3/library/struct.html#format-characters
unpack_pixel = struct.Struct("2i2hB").unpack
unpack_moderation = struct.Struct("qi4hB").unpack

pack_pixel = struct.Struct("2i2hB").pack

if __name__ == "__main__":
	start = time.time()

	#with open("./data/2023_place_canvas_history_2i2hB.bin", 'rb') as in_file:
	with open("./data/test_dataset.bin", 'rb') as in_file:
		#while True:
		for i in range (10):
			#read in the next 13 bytes for the next pixel
			packed_data = in_file.read(13)
			# stops if nothing read anymore
			if not packed_data:
				break
			# unpack pixel data with predefined format
			timestamp, user_id, x, y, color_id = unpack_pixel(packed_data)			
			print(timestamp, user_id, x, y, color_id)

	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()
