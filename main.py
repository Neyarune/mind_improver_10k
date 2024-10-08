import tkinter as tk
import random
from PIL import Image, ImageTk

def draw_grid(k=5):
    window_size = 800
    cell_size = window_size // k
    padding = (window_size - cell_size * k) // 2

    # Создание окна
    window = tk.Tk()
    window.title("Grid Drawing")
    canvas = tk.Canvas(window, width=window_size, height=window_size)
    canvas.pack()

    # Рисование сетки
    for row in range(k):
        for col in range(k):
            x1 = padding + col * cell_size
            y1 = padding + row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    # Загрузка изображения
    img = Image.open("myxa.png")
    img = img.resize((cell_size, cell_size), Image.Resampling.LANCZOS)  # Используем LANCZOS вместо ANTIALIAS
    img_tk = ImageTk.PhotoImage(img)

    # Выбор случайной клетки
    random_row = random.randint(0, k - 1)
    random_col = random.randint(0, k - 1)

    # Расчет координат для картинки
    x1 = padding + random_col * cell_size
    y1 = padding + random_row * cell_size

    # Отрисовка изображения
    canvas.create_image(x1, y1, anchor=tk.NW, image=img_tk)

    window.mainloop()

# Поле фиксировано размером 5x5
draw_grid()
