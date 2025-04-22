import pandas as pd; import numpy as np
import seaborn as sns; import matplotlib.pyplot as plt; import plotly.express as px
import gdown; import tempfile

file_id = "1P2-DrRmHUoO7d8lmZ480xrmbrGuxpCoI"
url = f"https://drive.google.com/uc?id={file_id}"


with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
    tmp_path = tmp.name

gdown.download(url, tmp_path, quiet=False)

df = pd.read_pickle(tmp_path)


df.columns = ["ID", "X", "Y", "Z", "EDA", "Tętno", "Temperatura", "Deklarowany poziom stresu"]
df['Intensywność ruchu'] = np.sqrt(df["X"]**2 + df["Y"]**2 + df["Z"]**2)

cols_to_keep = ["ID", "EDA", "Tętno", "Temperatura", "Deklarowany poziom stresu"]

df = df.loc[:, cols_to_keep]


# df.index=df.index - pd.Timedelta(hours=5)

desc_stats = df.describe().round(2).T.iloc[:, 1:]
desc_stats.columns = ["Średnia arytmetyczna", 
                      "Odchylenie standardowe",
                      "Wartość minimalna",
                      "Kwartyl pierwszy",
                      "Mediana", 
                      "Kwartyl trzeci",
                      "Wartość maksymalna"]
desc_stats.to_excel("../data/processed/statystyki_opisowe.xlsx")

continuous_vars = ["EDA", "Tętno", "Temperatura"]
fig, axes = plt.subplots(len(continuous_vars), 1, figsize=(20, 16))
for i, var in enumerate(continuous_vars):
    sorted_ids = df.groupby("ID")[var].median().sort_values().index
    sns.boxplot(data=df, x=var, y="ID", palette="coolwarm", order=sorted_ids, ax=axes[i], linewidth=2.5)
    axes[i].set_xlabel(var, fontsize=16)
    axes[i].set_ylabel("Identyfikator obiektu", fontsize=16)
    axes[i].tick_params(axis='both', labelsize=16)
plt.tight_layout()
plt.savefig("../reports/figures/4-boxplots-per-participant.png")

df.groupby(by="ID")[continuous_vars].mean().round(2)


plt.figure()
sns.heatmap(data=df.corr(numeric_only=True), 
            annot=True,
            cmap='viridis')
plt.tight_layout()
plt.savefig("../reports/figures/5-correlation-matrix.png")

df.groupby(by="ID").corr(numeric_only=True)

plt.figure()
sns.heatmap(df.groupby(by="Deklarowany poziom stresu").corr(numeric_only=True),
            annot=True,
            cmap="viridis")
plt.ylabel("Deklarowany poziom stresu-Zmienna")
plt.tight_layout()
plt.savefig("../reports/figures/6-correlation-matrix-stratified-by-stress.png")

label_colors={"Wysoki": "red",
              "Brak stresu": "blue",
              "Niski/Średni": "green"}
plt.figure()
sns.pairplot(data=df.sample(50000), 
             corner=True, 
             kind='scatter',
             hue='Deklarowany poziom stresu', 
             plot_kws={'s': 10},
             aspect=1.25,
             palette=label_colors,
             )
plt.tight_layout()
plt.savefig("../reports/figures/7-pair-scatterplots.png")

df["Deklarowany poziom stresu"].value_counts(normalize=True).round(2)


df.describe()

df.groupby("Deklarowany poziom stresu")[continuous_vars].mean().round(2)


sns.kdeplot(df, x='Temperatura', hue="ID")

filt = (df['ID']=="E4") & (df.index.day==19) 
sns.lineplot(df[filt], y="Tętno", x=df[filt].index, hue="Deklarowany poziom stresu")


# Aggregated observations to stress episode level
df_agg = pd.read_pickle("../data/interim/data_grouped_on_stress_episode.csv")

df_agg["id_num"] = pd.factorize(df_agg["id"])[0]


df_agg['id_num'].unique()

color_scale = [(0, "blue"), (0.5, "green"), (1, "red")]
fig = px.parallel_coordinates(df_agg.sample(100), color="Deklarowany poziom stresu", 
                              color_continuous_scale=color_scale,
                              dimensions=["HR_mean", "HR_std", "HR_max","TEMP_mean",
                                          "EDA_mean", "Deklarowany poziom stresu"])
fig.show()
# Looks like this is the approach to take:
# Have a mixed-effects model
# See how different stress levels affect phisiological variables
# for each individual
# say for 5C how is heart rate different, given the period was highly stressful? 
# Stratifying by just stress level doesnt take 
# into account natural variabilty between individuals - 
# everyone has a different baseline and 
# the differences between no/moderat/high stress 
# in Heart rate on an individual level is important

filt = df["ID"] == "5C"
df[filt].groupby(by="Deklarowany poziom stresu")['Tętno'].mean()



plt.figure(figsize=(24,24))
sns.heatmap(df.groupby(by="ID").corr(numeric_only=True),
            annot=True,
            cmap="viridis")




