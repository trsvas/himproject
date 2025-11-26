import tkinter as tk
from tkinter import messagebox
from my_app import MyApp
from data import Main, Child, Update, DB
import sqlite3
from us import *
import sys

conn = sqlite3.connect('info.db')
cur = conn.cursor()


def center_window(window, width, height):
    """Центрирование окна на экране"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def exit_program():
    """Выход из программы"""
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        conn.close()
        sys.exit()


def login():
    global app
    username = username_entry.get()
    password = sha256(password_entry.get().encode()).hexdigest()

    cur.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cur.fetchone()

    if result and result[0] == password:
        messagebox.showinfo("Успех", "Добро пожаловать!")
        role = result[1]

        if role == 'researcher':

            # Закрываем окно авторизации
            app.destroy()  # Добавь эту строку

            root = tk.Tk()  # Создаем корневое окно для расчетов
            app = MyApp(root)  # Создаем экземпляр класса MyApp
            app.run()  # Запускаем главный цикл приложения
        elif role == 'administrator':

            show_admin_interface()


    else:
        messagebox.showerror("Ошибка", "Неправильный логин или пароль")


def show_admin_interface():
    app.withdraw()
    admin_window = tk.Toplevel(app)
    admin_window.title("Меню администратора")

    window_width, window_height = 300, 200
    center_window(admin_window, window_width, window_height)

    tk.Button(admin_window, text="Добавить коэффициенты", command=add_mat).pack(pady=10)
    tk.Button(admin_window, text="Добавить пользователя", command=run_add).pack(pady=10)

    # Кнопка выхода в окне администратора
    tk.Button(admin_window, text="Выйти из программы", command=exit_program, bg="lightcoral").pack(pady=10)


def add_mat():
    db = DB()  # Создаем объект базы данных
    mat_window = tk.Toplevel()  # Создаем новое Toplevel окно для добавления материалов
    main_app = Main(mat_window, db)  # Передаем новое окно и объект базы данных в Main
    main_app.pack(fill=tk.BOTH, expand=True)  # Упаковываем виджет
    mat_window.title("База данных материалов")  # Заголовок окна
    mat_window.geometry("650x450+300+200")  # Задаем размеры окна
    mat_window.resizable(False, False)
    back_button = tk.Button(mat_window, text="Назад в главное меню",
                            command=lambda: [mat_window.destroy(), show_admin_interface()],
                            bg="lightblue")
    back_button.pack(side=tk.BOTTOM, pady=10)


def edit_mat():
    """Функция для редактирования существующих материалов через существующий интерфейс"""
    # Создаем окно с таблицей материалов для редактирования
    db = DB()
    edit_window = tk.Toplevel()
    main_app = Main(edit_window, db)
    main_app.pack(fill=tk.BOTH, expand=True)
    edit_window.title("Редактирование материалов")
    edit_window.geometry("650x450")
    center_window(edit_window, 650, 450)

    # Добавляем пояснение
    info_label = tk.Label(edit_window,
                          text="Для редактирования: выберите материал в таблице и нажмите 'Редактировать'",
                          bg="lightyellow")
    info_label.pack(side=tk.TOP, fill=tk.X)


# Создание главного окна для авторизации
app = tk.Tk()
app.title("Авторизация")
app.geometry("400x250")  # Увеличил высоту для кнопки выхода

# Центрируем главное окно
center_window(app, 400, 250)

# Метка и поле ввода для логина
tk.Label(app, text="Логин:").pack(pady=5)
username_entry = tk.Entry(app)
username_entry.pack(pady=5)

# Метка и поле ввода для пароля
tk.Label(app, text="Пароль:").pack(pady=5)
password_entry = tk.Entry(app, show='*')  # Показываем символы для пароля
password_entry.pack(pady=5)

# Кнопка для входа
login_button = tk.Button(app, text="Войти", command=login)
login_button.pack(pady=10)

# Кнопка для выхода из программы
exit_button = tk.Button(app, text="Выйти из программы", command=exit_program, bg="lightcoral")
exit_button.pack(pady=10)

# Обработка закрытия окна через крестик
app.protocol("WM_DELETE_WINDOW", exit_program)

conn.commit()
# Запуск главного цикла Tkinter
app.mainloop()