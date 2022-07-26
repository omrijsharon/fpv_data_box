import os
from tkinter import *
from tkinter import messagebox
from utils.helper_functions import yaml_writer, yaml_reader
from tkinter import filedialog
from utils.helper_functions import is_config


def config_menu(window, fc_dir, goggles_dir, state=False):
    # state False: configure mode
    # state True: copy mode

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
            if not os.path.exists(dir_data.get()):
                os.mkdir(dir_data.get())
            data = {
                "data_dir": dir_data.get(),
                "pilots": get_pilot_name_list(),
                "drones": get_drone_name_list()
            }
            filename = os.path.join(os.getcwd(), "config", "pilots_and_drones.yaml")
            yaml_writer(filename, data)
            popup_config.destroy()
        else:
            messagebox.showerror('Data Error', 'Error: Pilot list and drone list must contain at least one item.')

    def copy_data():
        messagebox.showinfo(title="copy data",
                            message=f"Drone: {lb_drone_name.get(ANCHOR)}, Pilot: {lb_pilot_name.get(ANCHOR)}")

    def get_data_dir():
        dir_data.set(os.path.join(filedialog.askdirectory(), "fpv_data"))

    def configure_mode():
        ent_dir_data.configure(state='normal')
        btn_dir_data.configure(state='normal')
        lbl_drone_name.configure(text="Add drone:")
        lbl_pilot_name.configure(text="Add pilot:")
        btn_drone_add.configure(state='normal')
        btn_pilot_add.configure(state='normal')
        ent_drone_name.configure(state='normal')
        ent_pilot_name.configure(state='normal')
        btn_drone_delete.configure(state='normal')
        btn_pilot_delete.configure(state='normal')
        btn_save.configure(text="Save config", command=save_config)
        btn_mode.configure(text="Copy mode", command=copy_mode)
        popup_config.title("FPV Data Box - Configure mode")

    def copy_mode():
        ent_dir_data.configure(state='disabled')
        btn_dir_data.configure(state='disabled')
        lbl_drone_name.configure(text="Select drone:")
        lbl_pilot_name.configure(text="Select pilot:")
        btn_drone_add.configure(state='disabled')
        btn_pilot_add.configure(state='disabled')
        ent_drone_name.configure(state='disabled')
        ent_pilot_name.configure(state='disabled')
        btn_drone_delete.configure(state='disabled')
        btn_pilot_delete.configure(state='disabled')
        btn_save.configure(text="Copy", command=copy_data)
        btn_mode.configure(text="Config mode", command=configure_mode)
        popup_config.title("FPV Data Box - Copy mode")

    popup_config = Toplevel()
    popup_config.wm_transient(window)
    # popup_config.attributes('-topmost', 'true')
    popup_config.title("FPV Data Box - Configure mode")
    popup_config.geometry('480x280')
    popup_config.resizable(False, False)


    # Choose Data Directory
    Label(popup_config, text="Data folder:").place(x=10, y=5)
    btn_dir_data = Button(popup_config, text="Browse", width=14, command=get_data_dir)
    btn_dir_data.place(x=359, y=23)
    dir_data = StringVar()
    dir_data.set(os.path.join(os.path.expanduser('~'), "fpv_data"))
    ent_dir_data = Entry(popup_config, textvariable=dir_data, width=57)
    ent_dir_data.place(x=13, y=25)

    # Add and delete drones
    x0, y0 = 10, 50
    lbl_drone_name = Label(popup_config, text="Drone Name:")
    lbl_drone_name.place(x=x0+2, y=y0+3)
    ent_drone_name = Entry(popup_config, width=29)
    ent_drone_name.place(x=x0+5, y=y0+23)
    btn_drone_add = Button(popup_config, text="Add", command=add_drone_name)
    btn_drone_add.place(x=x0+184, y=y0+20)
    btn_drone_delete = Button(popup_config, text="Delete", command=delete_drone_name, width=29)
    btn_drone_delete.place(x=x0+4, y=y0+166)
    lb_drone_name = Listbox(popup_config, width=35, height=7, exportselection=False)
    lb_drone_name.place(x=x0+4, y=y0+48)

    # Add and delete pilots
    x0, y0 = 250, 50
    lbl_pilot_name = Label(popup_config, text="Pilot Name:")
    lbl_pilot_name.place(x=x0+2, y=y0+3)
    ent_pilot_name = Entry(popup_config, width=29)
    ent_pilot_name.place(x=x0+5, y=y0+23)
    btn_pilot_add = Button(popup_config, text="Add", command=add_pilot_name)
    btn_pilot_add.place(x=x0 + 184, y=y0 + 20)
    btn_pilot_delete = Button(popup_config, text="Delete", command=delete_pilot_name, width=29)
    btn_pilot_delete.place(x=x0+4, y=y0+166)
    lb_pilot_name = Listbox(popup_config, width=35, height=7, exportselection=False)
    lb_pilot_name.place(x=x0+4, y=y0+48)

    # Save button that also saves the config
    btn_save = Button(popup_config, text="Save config", width=14, bg="blue", fg="white", command=save_config)
    btn_save.place(x=359, y=247)
    btn_mode = Button(popup_config, text="Config mode", width=14, command=configure_mode)
    btn_mode.place(x=14, y=247)

    # Updates the config if already exists
    config_filename = os.path.join(os.getcwd(), "config", "pilots_and_drones.yaml")
    if os.path.exists(config_filename):
        config = yaml_reader(config_filename)
        dir_data.set(config["data_dir"])
        lb_drone_name.insert(END, *config["drones"])
        lb_pilot_name.insert(END, *config["pilots"])

    # state False: configure mode
    # state True: copy mode
    if not is_config():
        configure_mode()
        state = is_config()
        btn_mode.configure(state='disabled')
    if state:
        copy_mode()
    else:
        configure_mode()


    popup_config.mainloop()