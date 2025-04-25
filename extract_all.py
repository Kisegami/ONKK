import xarray as xr
import numpy as np
import pandas as pd

# Mở file NetCDF
file = "S5P_NRTI_L2__CO_____20250423T060136_20250423T060636_38999_03_020800_20250423T063503.nc"
ds = xr.open_dataset(file, group='PRODUCT')

# Lấy thông tin từ file
lat = ds['latitude'].values[0]         # shape (373, 215)
lon = ds['longitude'].values[0]        # shape (373, 215)
co = ds['carbonmonoxide_total_column'].values[0]
qa = ds['qa_value'].values[0]

# Lọc theo điều kiện Việt Nam và QA ≥ 0.5
mask = (lat >= 8) & (lat <= 24) & (lon >= 102) & (lon <= 110) & (qa >= 0.5)

# Lấy giá trị tại các pixel thỏa mãn
filtered_lat = lat[mask]
filtered_lon = lon[mask]
filtered_co = co[mask]
filtered_qa = qa[mask]

# Tạo DataFrame
date_str = file.split("_")[7][:8]
df = pd.DataFrame({
    "date": pd.to_datetime(date_str, format="%Y%m%d"),
    "lat": filtered_lat,
    "lon": filtered_lon,
    "CO_mol_per_m2": filtered_co,
    "qa_value": filtered_qa
})

# Xuất ra CSV
df.to_csv("co_pixel_data_vietnam.csv", index=False)
print("✅ Xuất dữ liệu thành công:", df.shape)
