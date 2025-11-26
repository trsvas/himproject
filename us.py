import tkinter as tk
from tkinter import messagebox
import sqlite3
from hashlib import sha256

# Подключение к базе данных SQLite
conn = sqlite3.connect('info.db')
cur = conn.cursor()

# Создаем таблицы, если их еще нет
cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('researcher', 'administrator'))
                )''')

conn.commit()

login_window = None
entry_username = None
entry_password = None


def add_user():
    user_window = tk.Tk()
    user_window.title("Добавить пользователя")

    window_width, window_height = 400, 250  # Увеличил высоту для дополнительной кнопки
    position_x = (user_window.winfo_screenwidth() // 2) - (window_width // 2)
    position_y = (user_window.winfo_screenheight() // 2) - (window_height // 2)
    user_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    tk.Label(user_window, text="Логин").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_username = tk.Entry(user_window)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Пароль").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_password = tk.Entry(user_window, show='*')
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Роль исследователь/администратор:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_role = tk.Entry(user_window)
    entry_role.grid(row=2, column=1, padx=10, pady=5)

    def save_user():
        username = entry_username.get()
        password = sha256(entry_password.get().encode()).hexdigest()
        role = entry_role.get().strip().lower()
        if role not in ['researcher', 'administrator']:
            messagebox.showerror("Ошибка", "Роль должна быть 'researcher' или 'administrator'")
            return
        try:
            cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Успех", "Пользователь добавлен")
            user_window.destroy()  # Закрываем окно после успешного добавления
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить пользователя: {e}")

    def exit_window():
        """Закрытие окна добавления пользователя"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти? Несохраненные данные будут потеряны."):
            user_window.destroy()

    # Фрейм для кнопок
    button_frame = tk.Frame(user_window)
    button_frame.grid(row=4, column=0, columnspan=2, pady=15)

    # Кнопка сохранения
    tk.Button(button_frame, text="Сохранить", command=save_user, bg="lightgreen", width=10).pack(side=tk.LEFT, padx=10)

    # Кнопка выхода
    tk.Button(button_frame, text="Выйти", command=exit_window, bg="lightcoral", width=10).pack(side=tk.LEFT, padx=10)

    # Обработка закрытия окна через крестик
    user_window.protocol("WM_DELETE_WINDOW", exit_window)


# Открытие окна добавления пользователя при запуске
def run_add():
    add_user()

    # Запуск основного цикла
    tk.mainloop()

    # Закрытие соединения
    conn.close()