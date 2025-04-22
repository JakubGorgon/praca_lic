import pandas as pd; import numpy as np
import seaborn as sns; import matplotlib.pyplot as plt
import gdown
import tempfile
import os

file_id = "1DOEJCUgoj-jRmP1_g8IpGRWoSNg6byJn"
url = f"https://drive.google.com/uc?id={file_id}"

# Step 1: Get a temporary file path (no open file handle)
with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
    tmp_path = tmp.name

# Step 2: Download the file to that path
gdown.download(url, tmp_path, quiet=False)

# Step 3: Read the CSV
df_raw = pd.read_csv(tmp_path)


df_raw.dtypes
df_raw['datetime'] = pd.to_datetime(df_raw['datetime'])

df_raw['datetime'].dt.date.unique()
df_raw['id'] = df_raw["id"].astype(str)

# df = df_raw.drop(columns=["X","Y", "Z"])
df = df_raw

df.isna().sum()

df.set_index("datetime", inplace=True)
df.sort_index(inplace=True)


df_agg = df.sort_values(by=["id", "datetime"]).reset_index()

# Calculate time difference within each ID group
df_agg["time_diff"] = df_agg.groupby("id")["datetime"].diff().dt.total_seconds().fillna(0)
df_agg["new_episode"] = df_agg["time_diff"] > 20
df_agg["episode_id"] = df_agg.groupby("id")["new_episode"].cumsum()

agg_funcs = {
    "EDA": ["mean", "std", "min", "max"],
    "HR": ["mean", "std", "min", "max"],
    "TEMP": ["mean", "std", "min", "max"],
}

df_grouped = df_agg.groupby(["id", "episode_id"]).agg(agg_funcs)

df_grouped.columns = ["_".join(col).strip("_") for col in df_grouped.columns]
df_grouped = df_grouped.reset_index()

# Include stress level (assuming it remains constant within an episode)
df_grouped["Deklarowany poziom stresu"] = df_agg.groupby(["id", "episode_id"])["label"].first().values
df_grouped['start'] = df_agg.groupby(["id", "episode_id"])["datetime"].first().values
df_grouped['end'] = df_agg.groupby(["id", "episode_id"])["datetime"].last().values
df_grouped.sort_values("start")



df_grouped.to_pickle("../data/interim/data_grouped_on_stress_episode.csv")

df_resampled = df.groupby('id').resample('1S').mean()
df_resampled.dropna(inplace=True)
df_resampled.reset_index(inplace=True)

df_resampled['label'] = np.where(df_resampled['label']==0.06060606060606061,
                                 0, df_resampled['label'])

df_resampled['label'].unique()
df_resampled['label'].dtype
df = df_resampled.set_index("datetime").sort_index()

df['label'] = np.where(df['label']==0.0, "Brak stresu", 
                       np.where(df['label'] == 1.0, "Niski/Średni", 
                                "Wysoki"))

# df.to_pickle("../data/interim/data_resampled.csv")


df_resampled_10_s = df.groupby('id').resample('10S').mean()
df_resampled_10_s.dropna(inplace=True)
df_resampled_10_s.reset_index(inplace=True)
df_resampled_10_s = df_resampled_10_s.set_index("datetime").sort_index()
df_resampled_10_s['label'] = np.where(df_resampled_10_s['label']==0.006231,
                                 0, df_resampled_10_s['label'])
df_resampled_10_s['label'] = df_resampled_10_s['label'].round()
df_resampled_10_s['label'].unique()

df_resampled_10_s['label'] = np.where(df_resampled_10_s['label']==0.0, "Brak stresu", 
                       np.where(df_resampled_10_s['label'] == 1.0, "Niski/Średni", 
                                "Wysoki"))

# df_resampled_10_s.to_pickle("../data/interim/data_resampled_10_s.csv")
