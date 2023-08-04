import numpy as np

circle_pixels = {}


def generate_circles(max_radius):
    for i in range(1, max_radius + 1):
        pixels = []

        for y in range(-i, i):
            for x in range(-i,i):
                if y * y + x * x < i * i:
                    pixels.append((y, x))
        circle_pixels[i] = np.array(pixels)


def place_moderation(canvas: np.ndarray, x1, y1, x2, y2, color_id):
    if y2 == 0:
        place_circle(canvas, x1, y1, x2, color_id)
    else:
        place_rectangle(canvas, x1, y1, x2, y2, color_id)


def place_rectangle(canvas: np.ndarray, x_min, y_min, dx, dy, color_id) -> None:
    x = x_min + 1500
    y = y_min + 1000
    canvas[y:y+dy, x:x+dx] = color_id


def place_circle(canvas: np.ndarray, x_min, y_min, radius, color_id) -> None:
    x = x_min + 1500
    y = y_min + 1000
    for dy, dx in circle_pixels[radius]:
        try:
            canvas[y + dy, x + dx] = color_id
        except:
            None
