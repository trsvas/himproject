import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import sqlite3


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        root.title("Редактирование данных")

        # Создание подключения к базе данных
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

        # Создание таблицы, если она не существует
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                value1 FLOAT,
                value2 FLOAT,
                value3 FLOAT,
                value4 FLOAT,
                value5 FLOAT,
                value6 FLOAT,
                value7 FLOAT
            )
        """)
        self.conn.commit()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        for i in range(1, 8):
            entry = tk.Entry(self.root)
            entry.pack(pady=5)
            setattr(self, f'value_entry_{i}', entry)

        # Кнопка добавления
        self.add_button = tk.Button(self.root, text="Добавить данные", command=self.add_data)
        self.add_button.pack(pady=5)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=(
        "ID", "Материал", "Value1", "Value2", "Value3", "Value4", "Value5", "Value6", "Value7"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)
        self.tree.bind('<Double-1>', self.on_item_select)

        # Кнопка обновления таблицы
        self.update_table_button = tk.Button(self.root, text="Обновить таблицу", command=self.update_table)
        self.update_table_button.pack(pady=5)

        self.update_table()

    def add_data(self):
        name = self.name_entry.get()
        values = [getattr(self, f'value_entry_{i}').get() for i in range(1, 8)]
        try:
            # Преобразование значений в числа (формат REAL)
            values = [float(v) for v in values]
            self.c.execute(
                "INSERT INTO data (name, value1, value2, value3, value4, value5, value6, value7) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (name, *values))
            self.conn.commit()
            messagebox.showinfo("Успех", "Данные добавлены!")
            self.update_table()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        for i in range(1, 8):
            getattr(self, f'value_entry_{i}').delete(0, tk.END)

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.c.execute("SELECT * FROM data")
        for row in self.c.fetchall():
            self.tree.insert('', tk.END, values=row)

    def on_item_select(self, event):
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, 'values')

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item_values[1])

        for i in range(1, 8):
            getattr(self, f'value_entry_{i}').delete(0, tk.END)
            getattr(self, f'value_entry_{i}').insert(0, item_values[i + 1])

        # Удаление выбранного элемента
        self.c.execute("DELETE FROM data WHERE id=?", (item_values[0],))
        self.conn.commit()
        self.update_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()