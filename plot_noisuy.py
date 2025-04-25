import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging

# Load dữ liệu gốc
df = pd.read_csv("co_pixel_data_vietnam.csv").dropna(subset=["lat", "lon", "CO_mol_per_m2"])

# Định nghĩa raster đều: mỗi pixel là 1 điểm
res = 0.05  # độ phân giải lưới (có thể chọn 0.02 cho dày hơn)
lon_min, lon_max = df['lon'].min(), df['lon'].max()
lat_min, lat_max = df['lat'].min(), df['lat'].max()
grid_lon = np.arange(lon_min, lon_max + res, res)
grid_lat = np.arange(lat_min, lat_max + res, res)
grid_x, grid_y = np.meshgrid(grid_lon, grid_lat)

# Ánh xạ dữ liệu gốc vào pixel gần nhất
data_map = np.full(grid_x.shape, np.nan)
for _, row in df.iterrows():
    i = int((row['lat'] - lat_min) / res)
    j = int((row['lon'] - lon_min) / res)
    if 0 <= i < data_map.shape[0] and 0 <= j < data_map.shape[1]:
        data_map[i, j] = row['CO_mol_per_m2']

# Kriging toàn bộ lưới
OK = OrdinaryKriging(
    df['lon'], df['lat'], df['CO_mol_per_m2'],
    variogram_model='linear',  # hoặc 'spherical', 'gaussian'
    verbose=False, enable_plotting=False
)
z, _ = OK.execute('grid', grid_lon, grid_lat)

# Gộp dữ liệu gốc + nội suy (giữ nguyên điểm gốc)
result_map = np.where(np.isnan(data_map), z, data_map)

# Vẽ heatmap kết quả
plt.figure(figsize=(10, 8))
plt.imshow(result_map, extent=(lon_min, lon_max, lat_min, lat_max),
           origin='lower', cmap='Reds', aspect='auto')
plt.colorbar(label='CO (mol/m²)')
plt.title("Kriging giữ nguyên điểm gốc - phủ trùm pixel")
plt.xlabel("Kinh độ")
plt.ylabel("Vĩ độ")
plt.grid(True)
plt.tight_layout()
plt.show()
