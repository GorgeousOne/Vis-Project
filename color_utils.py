import numpy as np
import colorsys
from PIL import Image

def thermal_color_mapping(value):
    hue = (262 - ((262 - 255) * value)) / 360.0
    return colorsys.hsv_to_rgb(hue, 1.0, 1.0)

def replace_with_thermal_colors(input_array):
    height, width, depth = input_array.shape
    result_array = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(0, height, 3):
        for j in range(0, width, 3):
            r, g, b = thermal_color_mapping(input_array[i, j, 0])
            result_array[i:i+3, j:j+3, 0] = int(r * 255)
            result_array[i:i+3, j:j+3, 1] = int(g * 255)
            result_array[i:i+3, j:j+3, 2] = int(b * 255)

    return result_array

def save_as_image_paletted(pixel_array, path):
	canvas = Image.fromarray(pixel_array, mode="P")
	canvas.putpalette(list(sum(index_to_color_rgb, ())))
	canvas.save(path)
	

def save_as_image(pixel_array, path):
	image_array = convert_index_to_image_array(pixel_array)
	canvas = Image.fromarray(image_array)
	canvas.save(path)


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


color_to_index = {
	# day 1
	"#FFFFFF": 0,
	"#000000": 1,
	"#FF4500": 2,
	"#FFA800": 3,
	"#FFD635": 4,
	"#00A368": 5,
	"#3690EA": 6,
	"#B44AC0": 7,
	# day 2
	"#D4D7D9": 8,
	"#898D90": 9,
	"#7EED56": 10,
	"#2450A4": 11,
	"#51E9F4": 12,
	"#811E9F": 13,
	"#FF99AA": 14,
	"#9C6926": 15,
	# day 3
	"#BE0039": 16,
	"#00CC78": 17,
	"#00756F": 18,
	"#009EAA": 19,
	"#493AC1": 20,
	"#6A5CFF": 21,
	"#FF3881": 22,
	"#6D482F": 23,
	# day 4, 5, 6
	"#515252": 24,
	"#6D001A": 25,
	"#FFF8B8": 26,
	"#00CCC0": 27,
	"#94B3FF": 28,
	"#E4ABFF": 29,
	"#DE107F": 30,
	"#FFB470": 31,
}

index_to_color_hex = [
	'#FFFFFF',
	'#000000',
	'#FF4500',
	'#FFA800',
	'#FFD635',
	'#00A368',
	'#3690EA',
	'#B44AC0',
	'#D4D7D9',
	'#898D90',
	'#7EED56',
	'#2450A4',
	'#51E9F4',
	'#811E9F',
	'#FF99AA',
	'#9C6926',
	'#BE0039',
	'#00CC78',
	'#00756F',
	'#009EAA',
	'#493AC1',
	'#6A5CFF',
	'#FF3881',
	'#6D482F',
	'#515252',
	'#6D001A',
	'#FFF8B8',
	'#00CCC0',
	'#94B3FF',
	'#E4ABFF',
	'#DE107F',
	'#FFB470'
]

colors_hex_sorted = [
	"#6D001A",
	"#BE0039",
	"#FF4500",
	"#FFA800",
	"#FFD635",
	"#FFF8B8",
	"#7EED56",
	"#00CC78",
	"#00A368",
	"#00756F",
	"#009EAA",
	"#00CCC0",
	"#51E9F4",
	"#3690EA",
	"#2450A4",
	"#493AC1",
	"#6A5CFF",
	"#94B3FF",
	"#811E9F",
	"#B44AC0",
	"#E4ABFF",
	"#DE107F",
	"#FF3881",
	"#FF99AA",
	"#6D482F",
	"#9C6926",
	"#FFB470",
	"#000000",
	"#515252",
	"#898D90",
	"#D4D7D9",
	"#FFFFFF"
]

index_to_color_rgb = [
	(255, 255, 255),
	(0, 0, 0),
	(255, 69, 0),
	(255, 168, 0),
	(255, 214, 53),
	(0, 163, 104),
	(54, 144, 234),
	(180, 74, 192),
	(212, 215, 217),
	(137, 141, 144),
	(126, 237, 86),
	(36, 80, 164),
	(81, 233, 244),
	(129, 30, 159),
	(255, 153, 170),
	(156, 105, 38),
	(190, 0, 57),
	(0, 204, 120),
	(0, 117, 111),
	(0, 158, 170),
	(73, 58, 193),
	(106, 92, 255),
	(255, 56, 129),
	(109, 72, 47),
	(81, 82, 82),
	(109, 0, 26),
	(255, 248, 184),
	(0, 204, 192),
	(148, 179, 255),
	(228, 171, 255),
	(222, 16, 127),
	(255, 180, 112)
]
