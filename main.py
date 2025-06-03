import requests
import pandas as pd
import matplotlib.pyplot as plt
import folium
from pathlib import Path

# === SETUP ===
# Create folders if not exist
Path("CrimeData").mkdir(exist_ok=True)
Path("images").mkdir(exist_ok=True)

# === 1. PULL DATA FROM CHICAGO CRIME API ===
url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?$limit=1000"
response = requests.get(url)
data = response.json()

# === 2. CONVERT TO DATAFRAME ===
df = pd.DataFrame(data)
df.to_csv("CrimeData/chicago_crime_sample.csv", index=False)
print("✅ Data saved to CrimeData/chicago_crime_sample.csv")

# === 3. CLEAN DATE/TIME COLUMNS ===
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.date
df['hour'] = df['date'].dt.hour

# === 4. QUICK ANALYSIS ===
print("\n🔹 Top 10 Crime Types:")
print(df['primary_type'].value_counts().head(10))

print("\n🔹 Most Common Locations:")
print(df['location_description'].value_counts().head(10))

print("\n🔹 Crimes by Hour of Day:")
print(df['hour'].value_counts().sort_index())

# === 5. BAR CHART: Top 10 Crime Types ===
top_crimes = df['primary_type'].value_counts().head(10)
plt.figure(figsize=(8, 5))
top_crimes.plot(kind='barh', title='Top 10 Crime Types')
plt.xlabel("Number of Reports")
plt.tight_layout()
plt.savefig("images/top_crime_types.png")
plt.show()
print("📊 Bar chart saved to images/top_crime_types.png")

# === 6. LINE CHART: Daily Crime Count ===
daily_counts = df.groupby('day').size()
plt.figure(figsize=(10, 5))
daily_counts.plot(kind='line', title='Daily Crime Reports')
plt.xlabel("Date")
plt.ylabel("Reports")
plt.tight_layout()
plt.savefig("images/daily_crime_trend.png")
plt.show()
print("📈 Line chart saved to images/daily_crime_trend.png")

# === 7. FOLIUM MAP: Plot Crimes (First 100 w/ coordinates) ===
map_df = df.dropna(subset=['latitude', 'longitude']).head(100)
crime_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[float(row['latitude']), float(row['longitude'])],
        radius=3,
        popup=row['primary_type'],
        color='crimson',
        fill=True,
        fill_opacity=0.7
    ).add_to(crime_map)

crime_map.save("CrimeData/chicago_map.html")
print("🗺️ Map saved to CrimeData/chicago_map.html")

# === 8. FILTERED VIOLENT CRIMES ===
violent = df[df['primary_type'].isin(['ASSAULT', 'BATTERY', 'HOMICIDE', 'ROBBERY'])]
print(f"\n🔍 Violent Crimes Found: {len(violent)}")
