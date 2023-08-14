import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from time_utils import *


data = pd.read_csv('data/color_frequencies.csv', index_col="ms")
df = pd.DataFrame(data)

# uses the column headers as area colors
area_colors = tuple(data.columns)
# creates stacked area plot with custom colors, no legend and 0 line width
ax = df.plot.area(title="Use of colors over time", color=area_colors, legend=False, lw=0)
plt.tight_layout()

# draw y lines below graph
ax.grid(axis='y')
ax.set_axisbelow(True)


def format_large_number(y, pos):
    return f'{y:,.0f}'

def format_time(y, pos):
    return datetime.fromtimestamp(y * 0.001 + PLACE_START).strftime("%d.%#m.  %#I%p")


# convert x ticks from ms to datetime
ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_large_number))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1e6 / 2))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1e5))
# set ticks at every datafrane x value and make label vertical
plt.xticks(df.index, rotation=90)

ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
ax.xaxis.set_major_locator(ticker.MultipleLocator(time_to_ms(6)))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(time_to_ms(1)))

plt.xlabel('Time')
plt.ylabel('Placed pixels')

# highlight every nth tick (maybe highlight new days?)
for label in ax.get_xticklabels()[3::4]:
    label.set_fontweight('bold')


# add black hatch to white, set line width back to 1
white_area = ax.collections[-1]
white_area.set_linewidth(1)
white_area.set_edgecolor('#000')
white_area.set_hatch("xx")

plt.show()