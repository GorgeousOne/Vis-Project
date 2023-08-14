import os
import struct
import time

def count_placed_pixels(file_path, pixel_byte_count):
	file_size = os.path.getsize(file_path)
	return file_size // pixel_byte_count


def create_test_dataset(binary_file):
	"""saves 1% of that 132,000,000 entries"""
	with open("./data/test_dataset.bin", "wb") as out_file:
		while True:
			data = binary_file.read(buffer_size)
			if not data:
				break
			out_file.write(data)
			binary_file.seek(99 * buffer_size, 1)

# precompile unpacking formats
# list of format characters: https://docs.python.org/3/library/struct.html#format-characters
format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack
pack_pixel = struct.Struct(format).pack

if __name__ == "__main__":
	start = time.time()
	file_path = "./data/2023_place_canvas_history_2I4hB.bin"
	#file_path = "./data/test_dataset.bin"


	with open(file_path, 'rb') as in_file:
		create_test_dataset(in_file)
		exit()
		#while True:
		for i in range (10):
			#read in the next 13 bytes for the next pixel
			packed_data = in_file.read(buffer_size)
			# stops if nothing read anymore
			if not packed_data:
				break
			# unpack pixel data with predefined format
			timestamp, user_id, x, y, color_id = unpack_pixel(packed_data)
			print(timestamp, user_id, x, y, color_id)

	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()
