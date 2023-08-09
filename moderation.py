import numpy as np

circle_pixels = {}

def generate_circle(r):
	pixels = []
	for y in range(-r, r):
		for x in range(-r,r):
			if y * y + x * x < r * r:
				pixels.append((y, x))
	circle_pixels[r] = np.array(pixels)

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
	if radius not in circle_pixels:
		generate_circle(radius)
	for dy, dx in circle_pixels[radius]:
		try:
			canvas[y + dy, x + dx] = color_id
		except:
			None
