import xarray as xr
import numpy as np

# Cấu hình chung
file_path = "S5P_NRTI_L2__CO_____20250423T060136_20250423T060636_38999_03_020800_20250423T063503.nc"
variable_name = "carbonmonoxide_total_column"  # Hoặc thay bằng biến khác nếu là NO2, SO2, O3
qa_threshold = 0.5

# Mở file từ group PRODUCT
ds = xr.open_dataset(file_path, group="PRODUCT")
data = ds[variable_name]
qa = ds['qa_value']
lat = ds['latitude']
lon = ds['longitude']

# Lọc theo QA
valid_mask = qa >= qa_threshold
data_valid = data.where(valid_mask)

# Tính giá trị quan trọng
mean_val = float(data_valid.mean().values)
max_val = float(data_valid.max().values)
min_val = float(data_valid.min().values)

# Tìm vị trí của giá trị lớn nhất
idx_max = np.unravel_index(np.nanargmax(data_valid[0].values), data_valid[0].shape)
lat_max = float(lat[0].values[idx_max])
lon_max = float(lon[0].values[idx_max])

# Đếm số pixel hợp lệ và ước tính diện tích (rất sơ bộ)
valid_pixel_count = np.count_nonzero(~np.isnan(data_valid[0].values))
pixel_area_km2 = 7 * 7  # Giả định 7x7km/pixel ~ 49 km²
total_area = valid_pixel_count * pixel_area_km2

# Kết quả
print("📦 File:", file_path.split("/")[-1])
print("🔬 Biến:", variable_name)
print("📅 Ngày đo:", str(ds['time'].values[0])[:10])
print("✅ QA threshold:", qa_threshold)
print("\n📊 Thống kê:")
print("→ Trung bình:", round(mean_val, 6), "mol/m²")
print("→ Lớn nhất :", round(max_val, 6), "mol/m²")
print("→ Nhỏ nhất :", round(min_val, 6), "mol/m²")
print("→ Vị trí cực đại: lat =", lat_max, ", lon =", lon_max)
print("→ Diện tích có QA tốt:", round(total_area, 2), "km²")
