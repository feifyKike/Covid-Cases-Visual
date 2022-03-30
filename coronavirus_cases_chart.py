import csv
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
import requests

link = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
r = requests.get(link)
decoded_content = r.content.decode('utf-8')
csv_data = csv.reader(decoded_content.splitlines(), delimiter=',')
header = next(csv_data)
my_list = list(csv_data)
ask = input("Compare United States Total Cases to ")

dates, c_cases, us_cases, us_deaths, c_deaths = [], [], [], [], []
for row in my_list:
    if row[1] == 'US':
        dates.append(row[0])
        us_cases.append(int(row[5]))
        us_deaths.append(int(row[7]))
    elif row[2].lower() == ask.lower():
        c_cases.append(int(row[5]))
        c_deaths.append(int(row[7]))

# dpi=130, figsize=(10, 6)
fig, ax = plt.subplots(2)
ax[0].plot(dates[::30], us_cases[::30], c='red', label="US Cases", marker="^")
ax[0].plot(dates[::30], c_cases[::30], c='blue', label=ask + " Cases", marker="s")

ax[1].plot(dates[::30], us_deaths[::30], c='red', label="US Cases", marker="^")
ax[1].plot(dates[::30], c_deaths[::30], c='blue', label=ask + " Cases", marker="s")

annot = ax[0].annotate(
    "", 
    xy=(0,0), 
    xytext=(-40,40), 
    textcoords="offset points",
    bbox=dict(boxstyle='round', fc="white", ec='k', lw=1),
    arrowprops=dict(arrowstyle='-|>')
)
annot2 = ax[1].annotate(
    "", 
    xy=(0,0), 
    xytext=(-40,40), 
    textcoords="offset points",
    bbox=dict(boxstyle='round', fc="white", ec='k', lw=1),
    arrowprops=dict(arrowstyle='-|>')
)
annot.set_visible(False)
annot2.set_visible(False)

def onclick(event):
    x = event.xdata
    y = event.ydata
    formatted = "{:,}".format(y)
    if event.inaxes == ax[0]:
        annot.xy = (x, y)
        annot.set_text(formatted[:formatted.index(".")])
        annot.set_visible(True)
    elif event.inaxes == ax[1]:
        annot2.xy = (x, y)
        annot2.set_text(formatted[:formatted.index(".")])
        annot2.set_visible(True)
    fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', onclick)

# Format the plot
fig.set_size_inches(10, 6)
plt.legend()

ax[0].set_title("Total cases in the United States vs. " + ask.title())
ax[1].set_title("COVID-19 Deaths in the United States vs. " + ask.title())

ax[0].set(xlabel="", ylabel="Cases (in 10s of millions)")
ax[1].set(xlabel="Dates", ylabel="Deaths")
ax[0].label_outer()
fig.autofmt_xdate()

ax[0].grid(True)
ax[1].grid(True)

ax[0].fill_between(dates[::30], us_cases[::30], c_cases[::30], alpha=0.2)
ax[1].fill_between(dates[::30], us_deaths[::30], c_deaths[::30], alpha=0.2)
fig.canvas.manager.set_window_title('COVID-19 Dashboard')

plt.show()
