from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt

class GUI:
    def __init__(self):
        self.root = Tk()
    
    def create_table(self, columns_id, columns_size, columns_headers, data, table_size):
        table = ttk.Treeview(self.root, height=table_size)
        table['columns'] = columns_id
        table.column('#0', anchor=CENTER, width=1)

        for i, col_id in enumerate(columns_id):
            table.column(col_id, anchor=CENTER, width=columns_size[i])
            table.heading(col_id, text=columns_headers[i],anchor=CENTER)
        
        self.fill_table(table, data)
        table.pack()
    
    def fill_table(self, table, data_array):
        for i, value in enumerate(data_array):
            table.insert(parent='',index='end',iid=i,text='',values=value)
    
    def show_graph(self, amplifiers_points, powers, length, min_power):
        fig, ax = plt.subplots()
        ax.plot(amplifiers_points, powers, **{'marker': 'o'})
        ax.plot([0, length], [min_power, min_power])
        ax.set_xlabel('Длина канала')
        ax.set_ylabel('Уровень мощности')
        plt.show()

    def create_btn(self, text, command):
        plt_button = ttk.Button(self.root, text=text, command=command)
        plt_button.pack()

    def show_gui(self):
        self.root.mainloop()