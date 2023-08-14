import pandas as pd
import matplotlib.pyplot as plt
from time_utils import *
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker

data = pd.read_csv('data/color_frequencies.csv', index_col="ms")
df = pd.DataFrame(data)

# uses the column headers as area colors
area_colors = tuple(data.columns)
# creates stacked area plot with custom colors, no legend and 0 line width
ax = df.plot.area(title="Use of colors over time", color=area_colors, legend=False, lw=0)

# set ticks at every datafrane x value and make label vertical
plt.xticks(df.index, rotation=90)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1e6))
plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(1e5))

def format_large_number(y, pos):
    return f'{y:,.0f}'

ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_large_number))

plt.tight_layout()

# convert x ticks from ms to datetime
formatter = FuncFormatter(timestamp_to_str)
ax.xaxis.set_major_formatter(formatter)

# highlight every nth tick (maybe highlight new days?)
n = 24
for i, label in enumerate(ax.get_xticklabels()):
    if (i + 1) % n == 0:  # +1 to account for 0-based indexing
        label.set_fontweight('bold')

# add black hatch to white, set line width back to 1
white_area = ax.collections[-1]
white_area.set_linewidth(1)
white_area.set_edgecolor('#000')
white_area.set_hatch("xx")

plt.show()