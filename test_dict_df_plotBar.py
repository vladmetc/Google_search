import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 40)
pd.set_option('display.width', 400)


species = ("Adelie", "Chinstrap", "Gentoo")
penguin_means = {
    'Bill Depth': (18.35, 18.43, 14.98),
    'Bill Length': (38.79, 48.83, 47.50),
    'Flipper Length': (189.95, 195.82, 217.19),
}

# x = np.arange(len(species))  # the label locations

df = pd.DataFrame(
    penguin_means,
    index=pd.Series(species)
)
# print('df\n', df)

# x = np.arange(len(species))
# width = 0.6  # the width of the bars
# multiplier = 0

fig, ax = plt.subplots(layout='constrained')

rects = df.plot.bar(
    title='Penguin attributes by species',
    rot=0,
    width=0.6,
    figsize=(7, 4),
    ax=ax,
    ylim=(0, 250),
    ylabel='Length (mm)'
)
plt.legend(loc='upper left', ncols=3)

for i in range(df.shape[1]):
    # for artist in rects.containers[i]:
    #     print(artist)
    plt.bar_label(rects.containers[i], padding=3)

# for i in ax.containers:
#     for j in i:
#         print(j)

plt.show()
