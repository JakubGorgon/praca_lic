import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import importlib
import plot_settings

importlib.reload(plot_settings)

df = pd.read_csv("../../data/interim/data-wearables.csv", delimiter=";", encoding="latin1")
df.columns = ['Company name', 'Device name', 'Crowd funded', 'County of origin',
       'Release year', 'Form factor', 'Akcelerometr', 'Żyroskop',
       'Magnetometr', 'Barometr', 'GPS', 'Fotopletyzmograf']

df_sensors = pd.DataFrame(df[["Akcelerometr", "Żyroskop", 
         "Magnetometr", "Barometr", 
         "GPS", "Fotopletyzmograf"]].sum().sort_values()).reset_index()

df_sensors.columns = ["Sensor", "Ilość"]


sns.barplot(df_sensors, x = "Sensor", y="Ilość")
df.duplicated()

df_sensors.columns

sensors = df.columns[6:].to_list()  # List of sensor columns
percentages = []
years = []
devices_per_year = []

for year in df["Release year"].unique():
    filt = df["Release year"] == year
    df_year = df[filt]
    total_devices_for_year = df_year.shape[0]
    devices_per_year.append(total_devices_for_year)
    years.append(year)
    for sensor in sensors:
        # Calculate percentage for the current year and sensor
        percentage_with_sensor = (df_year[sensor].sum() / total_devices_for_year) * 100
        percentages.append({
            "Year": year,
            "Sensor": sensor,
            "Percentage": percentage_with_sensor,
            "Devices per year": total_devices_for_year
        })

df_sensors_popularity_per_year = pd.DataFrame(percentages).dropna().sort_values(by=["Year", "Sensor"]).reset_index(drop=True)

plt.figure()
sns.lineplot(data=df_sensors_popularity_per_year, 
             x="Year", y="Percentage", hue="Sensor", linewidth=5)
plt.legend(loc='upper left', bbox_to_anchor=(0.05, 0.8), title="Sensor")
plt.xlabel("Rok")
plt.ylabel("Procent urządzeń wykorzystujących dany sensor")
plt.savefig('../../reports/figures/1-sensors-per-year.png', bbox_inches='tight')

count_of_devices_per_year = df.groupby(by="Release year")["Device name"].count().sort_index()
count_of_devices_per_year.index = [2011, 2012, 2013, 2014, 2015, 2016, 2017]

plt.figure()
sns.barplot(data=count_of_devices_per_year, edgecolor="black")
plt.xlabel("Rok")
plt.ylabel("Liczba urządzeń")
plt.savefig("../../reports/figures/2-devices-per-year.png", bbox_inches='tight')