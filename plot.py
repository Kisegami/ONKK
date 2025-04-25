import pandas as pd
import matplotlib.pyplot as plt

# Load dữ liệu
df = pd.read_csv("co_pixel_data_vietnam.csv")
df = df.dropna(subset=["lat", "lon", "CO_mol_per_m2"])

# Xác định khung giới hạn tự động
buffer = 0.2
lat_min, lat_max = df['lat'].min() - buffer, df['lat'].max() + buffer
lon_min, lon_max = df['lon'].min() - buffer, df['lon'].max() + buffer

# Vẽ scatter
plt.figure(figsize=(10, 8))
sc = plt.scatter(
    df['lon'], df['lat'],
    c=df['CO_mol_per_m2'],
    cmap='Reds',
    s=10,
    alpha=0.8
)

plt.colorbar(sc, label='CO (mol/m²)')
plt.title('Phân bố CO (Sentinel-5P)')
plt.xlabel('Kinh độ')
plt.ylabel('Vĩ độ')
plt.grid(True)
plt.xlim(lon_min, lon_max)
plt.ylim(lat_min, lat_max)
plt.tight_layout()
plt.show()
