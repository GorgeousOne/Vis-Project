import os
import struct
import time
import csv

from color_utils import *
from time_utils import *

format = "2I4hB"
buffer_size = struct.calcsize(format)
unpack_pixel = struct.Struct(format).unpack

if __name__ == "__main__":
	start = time.time()
	file_path = "./data/2023_place_canvas_history_2I4hB.bin"
	# file_path = "./data/test_dataset.bin"
	out_path = "./data/color_frequencies.csv"

	if os.path.getsize(out_path) != 0:
		print(f"won't write to {out_path} unless file is empty. for your safety.")
		exit()

	frequencies = {color_to_index[hex]: 0 for hex in colors_hex_sorted}
	interval = time_to_ms(1)
	interval_limit = interval

	with open(out_path, "w", newline="") as out_file:
		csv_writer = csv.writer(out_file,)
		csv_writer.writerow(["ms"] + colors_hex_sorted)

		with open(file_path, 'rb') as in_file:
			while True:
				packed_data = in_file.read(buffer_size)
				if not packed_data:
					break
				timestamp, user_id, x, y, x2, y2, color_id = unpack_pixel(packed_data)

				if timestamp >= interval_limit:
					csv_writer.writerow([interval_limit] + list(frequencies.values()))
					for i in frequencies:
						frequencies[i] = 0
					interval_limit += interval

				if x2 == 0:
					frequencies[color_id] += 1

		csv_writer.writerow([timestamp] + list(frequencies.values()))
	print(f"iteration time {(time.time() - start):.1f}")
