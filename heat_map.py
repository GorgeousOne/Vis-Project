import struct
import time
import numpy as np
from PIL import Image
import pdb

from color_palette import *
import csv_bin_reader as bin_r

def convert_index_to_image_array(index_array):
	# Get the dimensions of the input_array
    rows, cols = index_array.shape
    
    # Create an all white RGB array to store the final result
    rgb_array = np.full((rows, cols, 3), 255, dtype=np.uint8)
    
    # Iterate through each index in the input array and map it to RGB
    for i in range(rows):
        for j in range(cols):
            index = index_array[i, j]
            rgb_array[i, j] = index_to_color_rgb[index]
    
    return rgb_array

unpack_pixel = struct.Struct("2i2hB").unpack
unpack_moderation = struct.Struct("qi4hB").unpack

if __name__ == "__main__":
	start = time.time()

	pixel_array = np.zeros((2000, 3000), dtype=np.uint8)
	frequency_array = np.zeros((2000, 3000), dtype=np.uint32)

	#file_path = "./data/2023_place_canvas_history_2i2hB.bin"
	file_path = "data/test_dataset.bin"

	with open(file_path, 'rb') as binary_file:
		while True:
			#read in the next 13 bytes for the next pixel
			packed_data = binary_file.read(13)
			# stops if nothing read anymore
			if not packed_data:
				break
			# unpack pixel data with predefined format
			timestamp, user_id, x, y, color_id = unpack_pixel(packed_data)
			pixel_array[y + 1000, x + 1500] = color_id
			frequency_array[y + 1000, x + 1500] += 1

	image_array = convert_index_to_image_array(pixel_array)
	brightness_scale = bin_r.count_placed_pixels(file_path, 13) / 6000000 * 0.7
	frequency_array = frequency_array / (frequency_array + brightness_scale)
	stacked_frequency_array = np.repeat(frequency_array [:, :, None], 3, axis=2) 
	heat_map = (image_array * stacked_frequency_array).astype(np.uint8)
	canvas = Image.fromarray(heat_map)

	print(f"iteration time {(time.time() - start):.1f}")
	start = time.time()

	canvas.show()