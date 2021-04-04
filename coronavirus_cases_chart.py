import csv
from datetime import datetime
from matplotlib import pyplot as plt
import requests

link = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
r = requests.get(link)
decoded_content = r.content.decode('utf-8')
csv_data = csv.reader(decoded_content.splitlines(), delimiter=',')
header = next(csv_data)
my_list = list(csv_data)
ask = input("Compare United States Total Cases to ")

dates, c_cases, us_cases = [], [], []
for row in my_list:
    if row[1] == 'US':
        us_cases.append(int(row[5]))
        dates.append(row[0])
    elif row[2].lower() == ask.lower():
        c_cases.append(int(row[5]))

fig = plt.figure(dpi=130, figsize=(10, 6))
plt.plot(dates[::30], us_cases[::30], c='red', label="US Cases", marker="^")
plt.plot(dates[::30], c_cases[::30], c='blue', label=ask + " Cases", marker="s")

# Format the plot
plt.title("Total cases in the United States vs. " + ask.title())
plt.xlabel("Date", fontsize = 14)
fig.autofmt_xdate()
plt.ylabel("Total cases (in millions)", fontsize= 14)
plt.tick_params(axis='both', which='minor', labelsize= 5)
plt.fill_between(dates[::30], us_cases[::30], c_cases[::30], alpha=0.2)
plt.legend()
plt.grid(True)

plt.show()