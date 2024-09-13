import numpy as np
from PIL import Image
from tree import Tree
import colorsys
import threading
from constants import (NUMBER_OF_GENERATIONS, WIDTH, HEIGHT, RGB_IMAGE,
                       R_IMAGE, B_IMAGE, G_IMAGE, NUMBER_OF_TREADS, HSV_IMAGE)


def generate(thread_num):
    for generation in range(NUMBER_OF_GENERATIONS):
        print(f'Image {generation + 1} / {NUMBER_OF_GENERATIONS} in thread {thread_num + 1}')

        # Заводим каналы цветов и функции для их заполнения
        r_tree, g_tree, b_tree = Tree().random(), Tree().random(), Tree().random()
        r_f, g_f, b_f = r_tree.operate, g_tree.operate, b_tree.operate
        r_array, g_array, b_array = np.zeros((WIDTH, HEIGHT)), np.zeros((WIDTH, HEIGHT)), np.zeros((WIDTH, HEIGHT))

        # Заполняем массивы цветовых каналов
        for x in range(WIDTH):
            for y in range(HEIGHT):
                try:
                    r_array[x, y] = r_f(x, y)
                    g_array[x, y] = g_f(x, y)
                    b_array[x, y] = b_f(x, y)
                except:
                    r_array[x, y] = 0.0
                    g_array[x, y] = 0.0
                    b_array[x, y] = 0.0

        # Нормализация значений
        if np.max(r_array) != np.min(r_array):
            r_array = 255 * (r_array - np.min(r_array)) / (np.max(r_array) - np.min(r_array))
        r_array = np.clip(r_array, 0, 255)

        if np.max(g_array) != np.min(g_array):
            g_array = 255 * (g_array - np.min(g_array)) / (np.max(g_array) - np.min(g_array))
        g_array = np.clip(g_array, 0, 255)

        if np.max(b_array) != np.min(b_array):
            b_array = 255 * (b_array - np.min(b_array)) / (np.max(b_array) - np.min(b_array))
        b_array = np.clip(b_array, 0, 255)

        if RGB_IMAGE:
            # Создание полного изображения
            data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            data[..., 0] = r_array  # Красный канал
            data[..., 1] = g_array  # Зеленый канал
            data[..., 2] = b_array  # Синий канал

            # Создание и сохранение изображения
            image = Image.fromarray(data)
            image.save(f'output/image_{thread_num + 1}_{generation + 1}_rgb.png')

        if HSV_IMAGE:
            # Создание полного изображения
            data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            data[..., 0] = r_array  # Красный канал
            data[..., 1] = g_array  # Зеленый канал
            data[..., 2] = b_array  # Синий канал

            for x in range(WIDTH):
                for y in range(HEIGHT):
                    hsv = data[x, y, 0], data[x, y, 1], data[x, y, 2]
                    data[x, y, :] = colorsys.hsv_to_rgb(*hsv)
            data *= 255

            # Создание и сохранение изображения
            image = Image.fromarray(data)
            image.save(f'output/image_{thread_num + 1}_{generation + 1}_hsv.png')

        if R_IMAGE:
            # Создание изображения красного канала
            data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            data[..., 0] = r_array  # Красный канал
            data[..., 1] = np.zeros((HEIGHT, WIDTH))  # Зеленый канал
            data[..., 2] = np.zeros((HEIGHT, WIDTH))  # Синий канал

            # Создание и сохранение изображения
            image = Image.fromarray(data)
            image.save(f'output/image_{thread_num + 1}_{generation + 1}_red.png')

        if G_IMAGE:
            # Создание изображения зеленого канала
            data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            data[..., 0] = np.zeros((HEIGHT, WIDTH))  # Красный канал
            data[..., 1] = g_array  # Зеленый канал
            data[..., 2] = np.zeros((HEIGHT, WIDTH))  # Синий канал

            # Создание и сохранение изображения
            image = Image.fromarray(data)
            image.save(f'output/image_{thread_num + 1}_{generation + 1}_green.png')

        if B_IMAGE:
            # Создание изображения синего канала
            data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            data[..., 0] = np.zeros((HEIGHT, WIDTH))  # Красный канал
            data[..., 1] = np.zeros((HEIGHT, WIDTH))  # Зеленый канал
            data[..., 2] = b_array  # Синий канал

            # Создание и сохранение изображения
            image = Image.fromarray(data)
            image.save(f'output/image_{thread_num + 1}_{generation + 1}_blue.png')


# Создание и запуск потоков
threads = []

for i in range(NUMBER_OF_TREADS):
    thread = threading.Thread(target=generate, args=(i,))
    threads.append(thread)
    thread.start()

# Ожидание завершения всех потоков
for thread in threads:
    thread.join()

print("All threads have finished execution")
