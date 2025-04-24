import xarray as xr
import matplotlib.pyplot as plt

# Đường dẫn đến file NetCDF tải từ Sentinel-5P
file_path = 'S5P_NRTI_L2__SO2____20250423T060136_20250423T060636_38999_03_020701_20250423T063945.nc'

# Mở file NetCDF bằng xarray
ds = xr.open_dataset(file_path)

# In danh sách các biến để kiểm tra
print("Danh sách biến có trong file:")
print(ds.data_vars)

# Trích xuất các khí cụ thể (nếu có)
# Tên biến có thể là: 'CO_column_number_density', 'SO2_column_number_density', 'NO2_column_number_density', 'O3_column_number_density'
try:
    co = ds['CO_column_number_density']
    print("\n✅ CO data loaded.")
except KeyError:
    print("\n❌ CO data not found.")

try:
    so2 = ds['SO2_column_number_density']
    print("✅ SO2 data loaded.")
except KeyError:
    print("❌ SO2 data not found.")

try:
    no2 = ds['NO2_column_number_density']
    print("✅ NO2 data loaded.")
except KeyError:
    print("❌ NO2 data not found.")

try:
    o3 = ds['O3_column_number_density']
    print("✅ O3 data loaded.")
except KeyError:
    print("❌ O3 data not found.")

# (Tuỳ chọn) Vẽ bản đồ NO2 nếu có
if 'NO2_column_number_density' in ds:
    no2 = ds['NO2_column_number_density']
    plt.figure(figsize=(10, 6))
    no2.plot(cmap='viridis')
    plt.title("NO₂ Column Density")
    plt.show()
