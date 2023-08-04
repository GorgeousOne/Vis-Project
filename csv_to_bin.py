
"""script to change the original format
	timestamp,base64_user_id,coordinate,pixel_color
	2023-07-20 18:09:49.658 UTC,1Gwttcp+9HC4YLaERXOAmAtfpBj/lD3Da9sLQSyonii/ObMqzWHbyVWVXeVvWVF3qPVIR0xB3TzYC5mOX/UL+A==,"477,268",#3690EA
to a binary format with a 
	4byte delta timestamp in ms, 
	4byte integer id, 
	2x2 byte (short) coordinates, 
	1byte char as color index
	-> 13 bytes per row
"""


from color_palette import color_to_index

from datetime import datetime
import csv
import os
import struct
import time


#precompile pack method to eliminate repeated compiling?
pack_pixel = struct.Struct("2I4hB").pack
#pack_moderation = struct.Struct("qi4hB").pack

def pixel_to_bin(row, mapped_user_ids, old_user_id_list):
	timestamp, user_id, color_id = get_timestamp_user_color(row, mapped_user_ids, old_user_id_list)
	x, y, *_ = row[2].split(",")
	#return pack_pixel(timestamp, user_id, int(x), int(y), color_id)
	return pack_pixel(timestamp, user_id, int(x), int(y), 0, 0, color_id)

def moderation_to_bin(row, mapped_user_ids, old_user_id_list):
	timestamp, user_id, color_id = get_timestamp_user_color(row, mapped_user_ids, old_user_id_list)
	coords = row[2]
	
	if coords[0] == "{":
		numbers = [int(num[3:]) for num in coords[1:-1].split(",")] + [0]
	else:
		numbers = [int(num) for num in coords.split(",")]
		numbers[2] -= numbers[0]
		numbers[3] -= numbers[1]

	return pack_pixel(timestamp, user_id, *numbers, color_id)


time_format = "%Y-%m-%d %H:%M:%S.%f %Z"
time_format_seconds = "%Y-%m-%d %H:%M:%S %Z"

def get_timestamp_user_color(row, mapped_user_ids, old_user_id_list):
	try:
		place_time = datetime.strptime(row[0], time_format)
	except ValueError:
		place_time = datetime.strptime(row[0], time_format_seconds)

	#timestamp = int(place_time.timestamp() * 1000)
	timestamp = int((place_time.timestamp() - 1689850800) * 1000)

	user_id = get_short_index(row[1], mapped_user_ids, old_user_id_list)
	color_id = color_to_index[row[3]]
	return timestamp, user_id, color_id

def get_short_index(long_id, mapped_user_ids, old_user_id_list):
	"""get a short index mapped to each long base_64 id"""
	if long_id not in mapped_user_ids:
		mapped_user_ids[long_id] = len(mapped_user_ids)
		old_user_id_list.append(long_id)
	return mapped_user_ids[long_id]


def read_existing_user_ids(file):
	"""reads list of all used long ids from a file
	in case the program crashes somewhere in the middle"""
	mapped_user_ids = dict()
	old_user_id_list = []
	for line in file.read().splitlines():
		mapped_user_ids[line] = len(old_user_id_list)
		old_user_id_list.append(line)
	return mapped_user_ids, old_user_id_list


# def test_xD():
# 	pixel_to_bin(['2023-07-20 13:00:26.088 UTC','no+8HEIDjbdx7/LxH9Xr+h4lyoar0MRTYugWKrGdQOg7dFg0rU9STehlIqsje1kc48U/BQqB/0J8sHQzXJBDFA==','-199,-235','#FFFFFF'], user_ids)
# 	moderation_to_bin(['2023-07-20 13:25:13.883 UTC','UJgZrjNi8XJ9UBsHPJTeU9xqeVB59ccxGwfcyx0gANwQWmkLSG9eeYV+UXZWB+tErQ9xQVIQRdrCLstfRrs6tQ==','{X: 425, Y: 441, R: 2}','#FFFFFF'], user_ids)
# 	moderation_to_bin(['2023-07-20 13:38:20.579 UTC','P/sXyJqzOHNfJwRTDEdkPGbSbbP3js5YBe7mx9aMrFE211tywcJIsZYkUV1S4CTvzswofkbRQdU4TiR1qExOhQ==','165,461,166,461','#FFD635'], user_ids)


if __name__ == "__main__":
	origin = "data/csv/"
	destination = "data/"

	# read already found user ids in case of program crash in the middle
	with open(destination + "user_ids.txt", "r") as f:
		user_ids, long_user_ids = read_existing_user_ids(f)

	# user_ids = dict()
	# long_user_ids = []

	filenames = sorted(os.listdir(origin))

	# read all csv files in firectory
	for fname in filenames[0:]:
		print(fname)
		start = time.time()

		binary_pixels = []
		binary_moderations = []
		prevous_long_id_count = len(long_user_ids)

		# convert all lines in file to binary
		with open(origin + fname) as infile:
			datareader = csv.reader(infile, delimiter=',', quotechar='"')
			for row in datareader:
				if row[0][0] == "t":
					continue
				if row[2].count(",") > 1:
					# binary_moderations.append(moderation_to_bin(row, user_ids, long_user_ids))
					binary_pixels.append(moderation_to_bin(row, user_ids, long_user_ids))
				else:
					binary_pixels.append(pixel_to_bin(row, user_ids, long_user_ids))

		# appennd binary of placed pixels
		with open(destination + '2023_place_canvas_history2I4hB.bin', 'ab') as outfile:
			for pixel in binary_pixels:
				outfile.write(pixel)
		# append binary of moderations
		# with open(destination + '2023_place_canvas_history_moderation.bin', 'ab') as outfile_mod:
		# 	for moderation in binary_moderations:
		# 		outfile_mod.write(moderation)
		# append list of found user ids in case of program crash
		with open(destination + 'user_ids.txt', 'a') as outfile_ids:
			for id in long_user_ids[prevous_long_id_count:]:
				outfile_ids.write(id + "\n")

		print(f"{(time.time() - start):.2f}s")
