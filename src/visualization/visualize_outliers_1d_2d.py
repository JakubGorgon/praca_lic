import pandas as pd; import numpy as np
import seaborn as sns; import matplotlib.pyplot as plt;
import preliz as pz

x = pz.Normal(mu=10, sigma=1).rvs(200)
y = 10 + 0.3*x+pz.Normal(mu=0, sigma=0.1).rvs(200)
df = pd.DataFrame(data=[x,y]).T
df.columns=["x", 'y']
df['outlier'] = np.repeat("nie", repeats=200)

df.loc[len(df)] = [8, 13.5, "tak"] 

plt.rcParams["font.size"] = 18

bins_x = [7,7.5,8,8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5]
bins_y = np.linspace(12.19, 13.81,12).round(2)

fig, ax = plt.subplots(1, 2, figsize=(19, 10), sharey=True)
sns.histplot(x=x, bins=bins_x, ax=ax[0])
sns.histplot(x=y, bins=bins_y, ax=ax[1])
ax[0].set_xlabel("X")
ax[1].set_xlabel("Y")
ax[0].set_ylabel("Liczba")
ax[0].set_xticks(bins_x[::2])
ax[1].set_xticks(bins_y[::2])
plt.tight_layout()
plt.savefig("../../reports/figures/8-histograms-x-and-y.png")

plt.figure(figsize=(19, 10))
sns.scatterplot(data=df, x="x", y="y", 
                hue="outlier",
                legend=False,
                style="outlier",
                palette={"tak": "red",
                         "nie":"blue"},
                 markers={"tak": "X", 
                          "nie": "o"},
                size="outlier",
                sizes={"tak": 700, 
                       "nie": 200})
plt.tight_layout()
plt.savefig("../../reports/figures/9-scatterplot-x-and-y.png")
