import h5py
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def write():
    matrix = np.random.random((10, 10))

    # Создаем матрицу с big-endian порядком байтов
    matrix_big_endian = matrix.astype('>f8')  # >f8 = big-endian float64

    with h5py.File('lab8/test.h5', 'w') as f:
        matrix_group = f.create_group('matrix_group')

        matrix_group.create_dataset('matrix', data=matrix)
        matrix_big_endian_dataset = matrix_group.create_dataset('matrix_big_endian', data=matrix_big_endian)

        matrix_big_endian_dataset.attrs['description'] = 'Данные с big-endian порядком байтов'

        scalar = f.create_group('scalar')
        scalar.create_dataset('scalar_int', data=42)
        scalar.create_dataset('scalar_float', data=42.22)
        scalar.create_dataset('scalar_string', data='zxc123')

        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        for i in range(100):
            for j in range(100):
                img_array[i, j] = [i * 2, j * 2, (i + j) % 256]

        # Сохраняем как PIL Image и затем в файл
        img = Image.fromarray(img_array)
        img.save('test_image.png')

        # Сохраняем массив картинки в HDF5
        image = f.create_dataset('image', data=img_array, compression='gzip')
        # Добавляем стандартные атрибуты HDF5 Image для правильного отображения
        image.attrs['CLASS'] = 'IMAGE'
        image.attrs['IMAGE_VERSION'] = '1.2'
        image.attrs['IMAGE_SUBCLASS'] = 'IMAGE_TRUECOLOR'
        image.attrs['INTERLACE_MODE'] = 'INTERLACE_PIXEL'
        image.attrs['format'] = 'RGB'
        image.attrs['description'] = 'Тестовая картинка с градиентом'

def read():
    with h5py.File('lab8/test.h5', 'r') as f:
        print(f'Ключи в корне: {list(f.keys())}')
        print()

        # Читаем матрицы из группы
        matrix_group = f['matrix_group']
        print(f'Ключи в matrix_group: {list(matrix_group.keys())}')
        print()

        # Проверяем порядок байтов в датасетах
        print('Порядок байтов в датасетах:')
        print(f'matrix dtype: {matrix_group["matrix"].dtype} (byte order: {matrix_group["matrix"].dtype.byteorder})')
        print(f'matrix_big_endian dtype: {matrix_group["matrix_big_endian"].dtype} (byte order: {matrix_group["matrix_big_endian"].dtype.byteorder})')
        print('Обозначения: "<" = little-endian, ">" = big-endian, "=" = native, "|" = not applicable')
        print()

        matrix_1 = matrix_group['matrix'][:1]  # 1 строка
        print(f'Первая строка matrix: {matrix_1}')

        matrix_2 = matrix_group['matrix'][1:2]  # 2 строка
        print(f'Вторая строка matrix: {matrix_2}')
        print()

        matrix_big_1 = matrix_group['matrix_big_endian'][:1]  # 1 строка
        print(f'Первая строка matrix_big_endian: {matrix_big_1}')
        print()

        # Читаем атрибуты big-endian датасета
        print('Метаданные matrix_big_endian:')
        for key, value in matrix_group['matrix_big_endian'].attrs.items():
            print(f'{key}: {value}')
        print()

        # Читаем скалярные значения
        scalar_group = f['scalar']
        print(f'Ключи в scalar: {list(scalar_group.keys())}')
        print()

        print('Скалярные значения:')
        scalar_int = scalar_group['scalar_int'][()]  # [()] для чтения скаляра
        scalar_float = scalar_group['scalar_float'][()]
        scalar_string = scalar_group['scalar_string'][()]
        if isinstance(scalar_string, bytes):
            scalar_string = scalar_string.decode()

        print(f'Целое число: {scalar_int}')
        print(f'Дробное число: {scalar_float}')
        print(f'Строка: {scalar_string}')
        print()

        # Читаем и восстанавливаем картинку
        print('Картинка:')
        img_array = f['image'][:]
        print(f'Размер картинки: {img_array.shape}')
        print(f'Формат: {f["image"].attrs["format"]}')
        print(f'Описание: {f["image"].attrs["description"]}')
        print(f'CLASS: {f["image"].attrs["CLASS"]}')
        print(f'IMAGE_VERSION: {f["image"].attrs["IMAGE_VERSION"]}')


        # Отображаем картинку через matplotlib
        print('Отображение картинки через matplotlib...')
        plt.figure(figsize=(8, 8))
        plt.imshow(img_array)
        plt.title('Картинка из HDF5 файла')
        plt.axis('off')  # Убираем оси координат
        plt.show()

if __name__ == '__main__':
    write()
    read()
