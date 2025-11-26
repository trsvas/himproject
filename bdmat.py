import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаём соединение с базой данных
conn = sqlite3.connect('info.db')
cursor = conn.cursor()


# Создаём интерфейс
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Данные материалов")

        # Создаём комбобокс
        self.combobox = ttk.Combobox(root, values=["Поливинилхлорид", "Полиэтилен", "Полипропилен"])
        self.combobox.pack(anchor="nw", padx=10)

        # Кнопка для получения данных
        self.button = tk.Button(root, text="Показать данные", command=self.show_data)
        self.button.pack(anchor="nw", padx=10)

        # Метки для отображения данных
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(anchor="nw", padx=10)

    def show_data(self):
        # Получение выбранного значения из комбобокса
        selected_material = self.combobox.get()

        # Запрос к базе данных
        cursor.execute("SELECT temp, energy, time, V FROM info WHERE name = ?", (selected_material,))
        result = cursor.fetchone()

        if result:
            temp, energy, time, V = result
            self.result_label.config(text=f"Температура: {temp}, Энергия: {energy}, Время: {time}, Объем: {V}")
        else:
            self.result_label.config(text="Данные не найдены")


# Настройка окна
root = tk.Tk()
app = App(root)
root.mainloop()

# Закрытие соединения с базой данных
conn.close()