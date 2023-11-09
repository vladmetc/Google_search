"""
Visualize Google Search results for the entity.
"""
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from PIL import Image
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import csv

with open('re_csv/articles_data.csv') as rf:
    reader = csv.DictReader(rf)
    txt = ""
    for i, row in enumerate(reader):
        # # txt = ''.join(row for row in reader) \
        txt += ''.join(row['title'] + row['text']) \
            .replace('\n', ' ') \
            .replace(',', '') \
            .replace('.', '') \
            .replace('/', ' ') \
            .replace('"', ' ') \
            .replace(':', ' ') \
            .replace('-', ' ') \
            .replace('   ', ' ') \
            .replace('  ', ' ') \
            .lower()

# StopWords
stopwords = set(STOPWORDS)
adw = ['crypto', 'https', 'htm', 'sell', 'buy', 'view', 'us', 'europe', 'world', 'say', 'says', 'said', 'may', 's',
       'one', 'year', 'will', 'user', 'users', 'cryptocurrencies', 'exchanges', 'binance', 'bitcoin',
       'june', 'february', 'cryptocom', 'days', 'another', 'ago']
for item in adw:
    if item not in stopwords:
        stopwords.add(item)
        # print("item %s in stopwords:" % item, item in stopwords, end="\t")
    else:
        print("%s already in stopwords" % item)

with open('stopwords.txt', 'w') as fl:
    for word in stopwords:
        writer = fl.write(word + ' ')

crimea_mask = np.array(Image.open('re_plots/Crimea_map.jpg'))

wc = WordCloud(
    scale=3,
    # colormap='cividis',
    # colormap='gist_earth',
    colormap='Wistia',
    # colormap='YlGnBu_r',
    mask=crimea_mask,
    contour_color='#1b2e46',
    contour_width=2,
    # width=420,
    # height=350,
    max_words=150,
    stopwords=stopwords,
    background_color='#101a28',
    collocations=False
).generate_from_text(txt)

plt.figure(figsize=(10, 8))
plt.imshow(wc)
plt.title('Kraken cryptocurrency exchange', fontsize=15)
plt.axis('off')
plt.show()
