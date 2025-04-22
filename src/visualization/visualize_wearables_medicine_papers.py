import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import importlib
import plot_settings

importlib.reload(plot_settings)

df = pd.read_csv("../../data/interim/pubmed_wearables_popularity.csv")

df.columns = ["Ilość wyszukań"]

df = df.sort_index(ascending=True).iloc[0:20].astype('int64')

plt.figure()
sns.lineplot(df, legend=False, linewidth=5)
plt.ylabel("Liczba publikacji")
plt.xticks(rotation=45)
plt.xlabel("Rok")
plt.savefig("../../reports/figures/3-wearables-in-medicine-popularity.png",
            bbox_inches="tight")