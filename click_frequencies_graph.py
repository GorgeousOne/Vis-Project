import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib import ticker

import os
import click_frequencies_count

input_path = "data/pixel_frequencies_7_24_17-18.txt"

if not os.path.exists(input_path):
	print("generating click frequency...")
	click_frequencies_count.main()

# Define the function to fit
def zipfsLaw(x, c, a, b):
	return c / (x + b) ** a

# Generate example data
frequencies = np.loadtxt(input_path, dtype=np.uint32)
y_data = np.sort(frequencies.flatten())[-250:][::-1]
x_data = np.arange(len(y_data)) + 1

# Initial guess for the parameters
#initial_guess = [600, 0.3, 0]
initial_guess = [600, 0.3, 0]

# Perform the fit
params, covariance = curve_fit(zipfsLaw, x_data, y_data, p0=initial_guess)

# Extract the fitted parameters
c_fit, a_fit, b_fit = params

#print(f"Fitted c: {c_fit}")
#print(f"Fitted a: {a_fit}")
#print(f"Fitted b: {b_fit}")

# Create a plot to visualize the fit
y_fit = c_fit / (x_data + b_fit)**a_fit
plt.scatter(x_data, y_data, label='r/place data', s=2)
plt.plot(x_data, y_fit, label="fitted Zipf's Law curve", color='red', alpha=0.7)

left, right = plt.xlim()
plt.xlim((0, right))

plt.minorticks_on()
ticks = list(plt.xticks()[0])
ticks.remove(0)
ticks.append(1)
plt.xticks(ticks)
#ax = plt.gca()
#ticks = ax.get_xticks()
#print(ticks.toList())

plt.title("Most popular pixels during 1 hour of r/place")
plt.xlabel('Rank of most popular pixels')
plt.ylabel('Number of clicks on pixels')
plt.legend()
plt.show()
