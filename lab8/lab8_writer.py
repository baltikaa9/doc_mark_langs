import h5py
import numpy as np

# Имя файла
filename = "experiment_data.h5"

print(f"Создание файла {filename}...")

with h5py.File(filename, 'w') as f:
    f.attrs['author'] = 'User'
    f.attrs['version'] = 1.0
    f.attrs['date'] = '2023-10-27'

    f.create_dataset('simple_int', data=42)
    f.create_dataset('simple_float', data=3.14159)

    dt = h5py.special_dtype(vlen=str)
    dset_str = f.create_dataset('message', (1,), dtype=dt)
    dset_str[0] = "Привет из HDF5!"

    matrix_data = np.random.random((5, 5))
    f.create_dataset('random_matrix', data=matrix_data)

    sensor_group = f.create_group('sensor_settings')
    sensor_group.attrs['location'] = 'Lab 1'
    sensor_group.create_dataset('threshold', data=0.05)
    sensor_group.create_dataset('is_active', data=True)

    x = np.linspace(0, 10, 1000)
    y = np.sin(x) * np.exp(-0.1 * x)

    vis_group = f.create_group('visualization_data')
    vis_group.create_dataset('x_axis', data=x)
    vis_group.create_dataset('y_axis', data=y)
