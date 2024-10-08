import tkinter as tk
import random
import time
import pyttsx3
import threading
import winsound
from PIL import Image, ImageTk

# Настройка синтезатора речи
engine = pyttsx3.init()

# Установка голоса на женский
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)  # Скорость речи

# Параметры игры
k = 5  # Размер поля
window_size = 800
cell_size = window_size // k
padding = (window_size - cell_size * k) // 2

# Координаты мухи (центр поля)
fly_x, fly_y = k // 2, k // 2

# Функция для синтеза речи
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для проигрывания звуков
def play_sound():
    winsound.Beep(600, 300)  # 600 Hz, 300 ms
    time.sleep(1)
    winsound.Beep(600, 300)

# Функция для перемещения мухи
def move_fly(canvas, fly):
    global fly_x, fly_y
    directions = ['вправо', 'влево', 'вперед', 'назад']

    while True:
        time.sleep(0.7)  # Уменьшено до 0.7 секунд
        
        direction = random.choice(directions)
        speak(f"Муха {direction}")

        if direction == 'вправо' and fly_x < k - 1:
            fly_x += 1
        elif direction == 'влево' and fly_x > 0:
            fly_x -= 1
        elif direction == 'вперед' and fly_y > 0:
            fly_y -= 1
        elif direction == 'назад' and fly_y < k - 1:
            fly_y += 1
        else:
            break  # Муха вышла за границы, останавливаем игру
        
        # Перемещение мухи на новом месте
        x1 = padding + fly_x * cell_size
        y1 = padding + fly_y * cell_size
        canvas.coords(fly, x1, y1)
    
    speak("Игра окончена")

# Функция, запускающая игру после нажатия пробела
def start_game(event, canvas, fly):
    global fly_x, fly_y
    # Центрируем муху
    fly_x, fly_y = k // 2, k // 2
    
    # Перемещаем изображение мухи в центр
    x1 = padding + fly_x * cell_size
    y1 = padding + fly_y * cell_size
    canvas.coords(fly, x1, y1)

    play_sound()

    # Запуск перемещения мухи в отдельном потоке
    fly_thread = threading.Thread(target=move_fly, args=(canvas, fly))
    fly_thread.start()

# Основное окно
window = tk.Tk()
window.title("Муха игра")
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

# Загрузка и отрисовка мухи
fly_img = Image.open("myxa.png")
fly_img = fly_img.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
fly_img_tk = ImageTk.PhotoImage(fly_img)  # Сохраняем картинку как глобальную переменную

x1 = padding + fly_x * cell_size
y1 = padding + fly_y * cell_size
fly = canvas.create_image(x1, y1, anchor=tk.NW, image=fly_img_tk)

# Привязка события нажатия пробела
window.bind('<space>', lambda event: start_game(event, canvas, fly))

window.mainloop()
