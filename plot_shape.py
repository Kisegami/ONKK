import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Load dữ liệu CO từ CSV
df = pd.read_csv("co_pixel_data_vietnam.csv")
df = df.dropna(subset=["lat", "lon", "CO_mol_per_m2"])

# Chuyển CSV thành GeoDataFrame
gdf_points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["lon"], df["lat"]),
    crs="EPSG:4326"
)

# Load GeoJSON Việt Nam
gdf_vn = gpd.read_file("vn.json")

# Đảm bảo cả 2 cùng CRS
gdf_vn = gdf_vn.to_crs("EPSG:4326")
gdf_points = gdf_points.to_crs("EPSG:4326")

# Vẽ bản đồ
fig, ax = plt.subplots(figsize=(10, 12))
gdf_vn.plot(ax=ax, edgecolor="black", facecolor="white", linewidth=0.8)

# Vẽ các điểm đo CO
gdf_points.plot(
    ax=ax,
    column="CO_mol_per_m2",
    cmap="Reds",
    markersize=10,
    alpha=0.8,
    legend=True,
    legend_kwds={"label": "CO (mol/m²)"}
)

plt.title("Phân bố điểm đo CO từ Sentinel-5P trên nền bản đồ Việt Nam (GeoJSON)")
plt.xlabel("Kinh độ")
plt.ylabel("Vĩ độ")
plt.grid(True)
plt.tight_layout()
plt.show()
