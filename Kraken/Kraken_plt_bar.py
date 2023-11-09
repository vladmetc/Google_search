"""
Visualize Google Search results for the entity alone against results associated with 'scam'.
"""
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 40)
pd.set_option('display.width', 400)


pf = pd.read_csv(
    're_csv/articles_data.csv',
    parse_dates=['timestamp', ],
)
df = pd.DataFrame(pf)
print("\ndf.index", df.index)

print("df.describe():\n", df.describe(include='all'))

df_sorted = df[['timestamp']].value_counts().sort_index()
# print("\ndf_sorted_", df_sorted)

df_sorted_scam = df[['timestamp', 'scam']].value_counts().sort_index()
# print("df_sorted_scam", df_sorted_scam)

df_merged = pd.merge(df_sorted, df_sorted_scam, how='outer', on='timestamp', suffixes=("_total", "_scam"))

num_cols = len(df_merged.columns)

df1 = df_merged.resample('7D').sum()

# No h:m:s in dates
df1.index = [df1.index[i].date() for i in range(len(df1.index))]

df1['period'] = [f"{df1.index[i]} - {df1.index[i] + pd.Timedelta('6D')}" for i in range(len(df1.index))]
print("df1.shape[0]", df1)

# fig, ax = plt.subplots(layout='constrained')

rects = df1.plot.bar(
    x='period', title="Kraken Crypto Exchange - Google Search news",
    alpha=0.9, figsize=(9, 6), width=0.7, ylabel='News count', ylim=(0, 50),
    # ax=ax
)
plt.legend(loc='upper right', ncols=3)

for i in range(num_cols):
    plt.bar_label(rects.containers[i], padding=3)

plt.gcf().autofmt_xdate(bottom=0.35, rotation=60)

# plt.savefig("re_plots/bar.png")
plt.show()
