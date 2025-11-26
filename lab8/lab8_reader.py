import h5py
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use('qtagg')
filename = "experiment_data.h5"

print(f"Чтение файла {filename}...\n")

with h5py.File(filename, 'r') as f:
    print("--- Глобальные атрибуты ---")
    for key, val in f.attrs.items():
        print(f"{key}: {val}")

    print("\n--- Скалярные значения ---")
    val_int = f['simple_int'][()]
    val_float = f['simple_float'][()]
    val_str = f['message'][0].decode('utf-8') if isinstance(f['message'][0], bytes) else f['message'][0]

    print(f"Int: {val_int}")
    print(f"Float: {val_float}")
    print(f"Message: {val_str}")

    print("\n--- Массив (Random Matrix) ---")
    matrix = f['random_matrix'][:]
    print(f"Shape: {matrix.shape}")
    print(f"Первая строка: {matrix[0]}")

    print("\n--- Объект (Sensor Settings) ---")
    grp = f['sensor_settings']
    loc = grp.attrs['location']
    thresh = grp['threshold'][()]
    active = grp['is_active'][()]
    print(f"Location: {loc}, Threshold: {thresh}, Active: {active}")

    print("\n--- Подготовка визуализации ---")
    x = f['visualization_data']['x_axis'][:]
    y = f['visualization_data']['y_axis'][:]

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Затухающая синусоида', color='b')
plt.title("Данные из HDF5")
plt.xlabel("Время (x)")
plt.ylabel("Амплитуда (y)")
plt.grid(True)
plt.legend()
plt.show()
