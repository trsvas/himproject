import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()




    def init_main(self):
        toolbar = tk.Frame(self, bg='#d7d8e0', bd=2)  # Передавайте self вместо root
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Создание кнопок с использованием grid
        tk.Button(toolbar, text="Добавить позицию", command=self.open_dialog).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(toolbar, text="Редактировать", command=self.open_update_dialog).grid(row=0, column=1, padx=5, pady=5)




        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'temp', 'energy', 'time', 'V'), height=15,
                                 show='headings')




        self.tree.column('ID', width=70, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('temp', width=100, anchor=tk.CENTER)
        self.tree.column('energy', width=100, anchor=tk.CENTER)
        self.tree.column('time', width=100, anchor=tk.CENTER)
        self.tree.column('V', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Материал')
        self.tree.heading('temp', text='Температура')
        self.tree.heading('energy', text='Энергия')
        self.tree.heading('time', text='Время')
        self.tree.heading('V', text='Объем')

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.pack()

    def records(self, name, temp, energy, time, V):
        self.db.insert_data(name, temp, energy, time, V)
        self.view_records()

    def update_record(self, name, temp, energy, time, V):
        self.db.c.execute('''UPDATE coefficients SET name=?, temp=?, energy=?, time=?, V=? WHERE ID=?''',
                          (name, temp, energy, time, V, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM coefficients''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child(self)

    def open_update_dialog(self):
        Update(self)



class Child(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.view = parent
        self.init_child()

    def init_child(self):
        self.title('Добавить информацию')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text='Наименование мат-ла:')
        label_name.place(x=0, y=0)
        label_temp = tk.Label(self, text='Температура (Td), °C:')
        label_temp.place(x=20, y=30)
        label_energy = tk.Label(self, text='Энергия (Ed), Дж/моль:')
        label_energy.place(x=10, y=60)
        label_time = tk.Label(self, text='Время (td), мин:')
        label_time.place(x=40, y=90)
        label_V = tk.Label(self, text='Объем (Ve), л:')
        label_V.place(x=40, y=120)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=150, y=1)

        self.entry_temp = ttk.Entry(self)
        self.entry_temp.place(x=150, y=30)

        self.entry_energy = ttk.Entry(self)
        self.entry_energy.place(x=150, y=60)

        self.entry_time = ttk.Entry(self)
        self.entry_time.place(x=150, y=90)

        self.entry_V = ttk.Entry(self)
        self.entry_V.place(x=150, y=120)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_temp.get(),
                                                                       self.entry_energy.get(),
                                                                       self.entry_time.get(),
                                                                       self.entry_V.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self, parent):
        super().__init__(parent)
        self.view = parent
        self.init_edit()



    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_temp.get(),
                                                                          self.entry_energy.get(),
                                                                          self.entry_time.get(),
                                                                          self.entry_V.get()))

        self.btn_ok.destroy()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('info.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS coefficients (id INTEGER PRIMARY KEY, name TEXT, temp FLOAT, energy FLOAT, time FLOAT, V FLOAT)''')
        self.conn.commit()


    def insert_data(self, name, temp, energy, time, V):
        self.c.execute('''INSERT INTO coefficients (name, temp, energy, time, V) VALUES (?, ?, ?, ?, ?)''',
                       (name, temp, energy, time, V))
        self.conn.commit()




    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root, db)
    app.pack()
    root.title("База данных материалов")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()

