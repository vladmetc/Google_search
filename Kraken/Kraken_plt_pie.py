"""
Visualize Google Search results for the entity alone against results associated with 'scam'.
"""
import matplotlib.pyplot as plt
import pandas as pd

pf = pd.read_csv(
    're_csv/articles_data.csv',
    parse_dates=['timestamp', ],
)
df = pd.DataFrame(pf)

df_sorted = df[['timestamp']].value_counts().sort_index()
df_sorted_scam = df[['timestamp', 'scam']].value_counts().sort_index()

df_merged = pd.merge(df_sorted, df_sorted_scam, how='outer', on='timestamp', suffixes=("_total", "_scam"))

vals = [df_merged['count_total'].sum(), df_merged['count_scam'].sum()]

df3 = pd.Series(
    [(vals[0] - vals[1]), vals[1]],
    index=[f"Non-scam: {int(vals[0] - vals[1])}", f"Scam related: {int(vals[1])}"],
    name=f"Total count: {int(vals[0])}"
)

explode = (0, 0.07)

df3.plot.pie(
    subplots=True, explode=explode, shadow=True, startangle=82, textprops={'size': 'larger'},
    figsize=(6, 6), autopct="%.1f%%", radius=0.9, title="Kraken Crypto Exchange news"
)

# plt.savefig("re_plots/pie.png")
plt.axis('off')
plt.show()
