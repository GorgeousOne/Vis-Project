import numpy as np
from PIL import Image


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

index_to_color_hex = {
    0: '#FFFFFF',
    1: '#000000',
    2: '#FF4500',
    3: '#FFA800',
    4: '#FFD635',
    5: '#00A368',
    6: '#3690EA',
    7: '#B44AC0',
    8: '#D4D7D9',
    9: '#898D90',
    10: '#7EED56',
    11: '#2450A4',
    12: '#51E9F4',
    13: '#811E9F',
    14: '#FF99AA',
    15: '#9C6926',
    16: '#BE0039',
    17: '#00CC78',
    18: '#00756F',
    19: '#009EAA',
    20: '#493AC1',
    21: '#6A5CFF',
    22: '#FF3881',
    23: '#6D482F',
    24: '#515252',
    25: '#6D001A',
    26: '#FFF8B8',
    27: '#00CCC0',
    28: '#94B3FF',
    29: '#E4ABFF',
    30: '#DE107F',
    31: '#FFB470'
}

index_to_color_rgb = {
    0: (255, 255, 255),
    1: (0, 0, 0),
    2: (255, 69, 0),
    3: (255, 168, 0),
    4: (255, 214, 53),
    5: (0, 163, 104),
    6: (54, 144, 234),
    7: (180, 74, 192),
    8: (212, 215, 217),
    9: (137, 141, 144),
    10: (126, 237, 86),
    11: (36, 80, 164),
    12: (81, 233, 244),
    13: (129, 30, 159),
    14: (255, 153, 170),
    15: (156, 105, 38),
    16: (190, 0, 57),
    17: (0, 204, 120),
    18: (0, 117, 111),
    19: (0, 158, 170),
    20: (73, 58, 193),
    21: (106, 92, 255),
    22: (255, 56, 129),
    23: (109, 72, 47),
    24: (81, 82, 82),
    25: (109, 0, 26),
    26: (255, 248, 184),
    27: (0, 204, 192),
    28: (148, 179, 255),
    29: (228, 171, 255),
    30: (222, 16, 127),
    31: (255, 180, 112)
}
