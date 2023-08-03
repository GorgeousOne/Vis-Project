import numpy as np

circle_pixels = {}


def generate_circles(max_radius):
    for i in range(1, max_radius):
        pixels = []

        for y in range(-i, i):
            for x in range(-i,i):
                if y * y + x * x < i * i:
                    pixels.append((y, x))
        circle_pixels[i] = np.array(pixels)


def place_moderation(canvas: np.ndarray, x1, y1, x2, y2, color_id):
    if y2 == 0:
        place_circle(canvas, x1, y1, x1, color_id)
    else:
        place_rectangle(canvas, x1, y2, x2, y2, color_id)


def place_rectangle(canvas: np.ndarray, x_min, y_min, x_max, y_max, color_id) -> None:
    canvas[y_min+1000:y_max+1000, x_min+1500:x_max+1500] = color_id


def place_circle(canvas: np.ndarray, x, y, radius, color_id) -> None:
    for dy, dx in circle_pixels[radius]:
        canvas[y+1000 + dy, x+1500 + dx] = color_id
