import os
from tkinter import *
from tkinter import messagebox
from utils.helper_functions import yaml_writer
from tkinter import filedialog


def add_drone_name():
    if len(ent_drone_name.get()) > 0:
        lb_drone_name.insert(lb_drone_name.size(), ent_drone_name.get())
        ent_drone_name.delete(0, END)


def delete_drone_name():
    lb_drone_name.delete(ANCHOR)


def get_drone_name_list():
    return list(lb_drone_name.get(0, END))


def add_pilot_name():
    lb_pilot_name.insert(lb_pilot_name.size(), ent_pilot_name.get())
    ent_pilot_name.delete(0, END)


def delete_pilot_name():
    lb_pilot_name.delete(ANCHOR)


def get_pilot_name_list():
    return list(lb_pilot_name.get(0, END))


def save_config():
    if len(get_pilot_name_list()) > 0 and len(get_drone_name_list()) > 0:
        os.mkdir(dir_data.get())
        data = {
            "data_dir": dir_data.get(),
            "pilots": get_pilot_name_list(),
            "drones": get_drone_name_list()
        }
        filename = os.path.join(os.getcwd(), "config", "pilots_and_drones.yaml")
        yaml_writer(filename, data)
        window.destroy()
    else:
        messagebox.showerror('Data Error', 'Error: Pilot list and drone list must contain at least one item.')


def get_data_dir():
    dir_data.set(os.path.join(filedialog.askdirectory(), "fpv_data"))


window = Tk()
window.title("FPV Data Box - Configure")
window.geometry('480x280')
window.resizable(False, False)

Label(window, text="Data folder:").place(x=10, y=5)
btn_dir_data = Button(window, text="Browse", width=14, command=get_data_dir)
btn_dir_data.place(x=359, y=23)
dir_data = StringVar()
dir_data.set(os.path.join(os.path.expanduser('~'), "fpv_data"))
ent_dir_data = Entry(window, textvariable=dir_data,width=57)
ent_dir_data.place(x=13, y=25)

x0, y0 = 10, 53
Label(window, text="Drone Name:").place(x=x0, y=y0)
ent_drone_name = Entry(window, width=16, font=("Arial", 14))
ent_drone_name.place(x=x0+5, y=y0+20)
btn_drone_add = Button(window, text="Add", command=add_drone_name)
btn_drone_add.place(x=x0+184, y=y0+20)
btn_drone_delete = Button(window, text="Delete", command=delete_drone_name, width=29)
btn_drone_delete.place(x=x0+4, y=y0+166)
lb_drone_name = Listbox(window, width=35, height=7)
lb_drone_name.place(x=x0+4, y=y0+48)


x0, y0 = 250, 53
Label(window, text="Pilot Name:").place(x=x0, y=y0)
ent_pilot_name = Entry(window, width=16, font=("Arial", 14))
ent_pilot_name.place(x=x0+5, y=y0+20)
btn_pilot_name = Button(window, text="Add", command=add_pilot_name)
btn_pilot_name.place(x=x0+184, y=y0+20)
btn_pilot_delete = Button(window, text="Delete", command=delete_pilot_name, width=29)
btn_pilot_delete.place(x=x0+4, y=y0+166)
lb_pilot_name = Listbox(window, width=35, height=7)
lb_pilot_name.place(x=x0+4, y=y0+48)

btn_next = Button(window, text="Next", width=14, bg="blue", fg="white", command=save_config)
btn_next.place(x=359, y=247)

window.mainloop()