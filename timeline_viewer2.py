import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image

# Define the folder containing images
image_folder = 'data/real_timeline'

# Get a list of image file names in the folder
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

# Initialize variables
current_index = 0
num_images = len(image_files)

# Create a function to update the displayed image
def update_image(val):
    global current_index
    current_index = int(val)
    img_path = os.path.join(image_folder, image_files[current_index])
    img = Image.open(img_path)
    ax.imshow(img)
    fig.canvas.draw()

# Create the figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Load and display the initial image
initial_img_path = os.path.join(image_folder, image_files[current_index])
initial_img = Image.open(initial_img_path)
ax.imshow(initial_img)

# Create a slider
ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Image', 0, num_images - 1, valinit=current_index, valstep=1)
slider.on_changed(update_image)

# Display the plot
plt.show()