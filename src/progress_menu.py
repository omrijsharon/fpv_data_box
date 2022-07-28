import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from time import sleep
from copy import deepcopy


def file_list_size(path, file_list):
    files_path = [os.path.join(path, filename) for filename in file_list]
    files_size = [os.path.getsize(file) for file in files_path]
    total_size = sum(files_size)
    return total_size


path = r"H:\DCIM\100MEDIA"
file_list = os.listdir(path)
files_left2copy_list = deepcopy(file_list)
total_size = file_list_size(path, file_list)
teams = range(100)


def button_command():
    def cancel_command():
        answer = messagebox.askyesno("Cancel copy", "Are you sure you want to cancel copying files?")
        if answer:
            popup.destroy()


    #start progress bar
    popup = tk.Toplevel()
    popup.geometry('250x150')
    popup.resizable(False, False)
    popup.title("Copying files...")
    btn_cancel = tk.Button(popup, text="Cancel", command=cancel_command)
    btn_cancel.place(x=98, y=110)

    lbl_fc_file_copy = tk.Label(popup, text="FC: copying file: ")
    lbl_fc_file_copy.place(x=18, y=10)
    progress_var_fc = tk.DoubleVar()
    progress_var_fc.set(0)
    progress_bar_fc = ttk.Progressbar(popup, variable=progress_var_fc, maximum=100)
    progress_bar_fc.place(x=20, y=30, width=210, height=20)

    lbl_goggles_file_copy = tk.Label(popup, text="Goggles: copying file: ")
    lbl_goggles_file_copy.place(x=18, y=58)
    progress_goggles_var = tk.DoubleVar()
    progress_goggles_var.set(0)
    progress_bar_goggles = ttk.Progressbar(popup, variable=progress_goggles_var, maximum=100)
    progress_bar_goggles.place(x=20, y=80, width=210, height=20)

    popup.update()
    # popup.pack_slaves()
    for file in file_list:
        lbl_fc_file_copy.config(text=f"FC: copying file: {file}")
        sleep(0.1)
        del files_left2copy_list[0]
        progress_var_fc.set((1 - file_list_size(path, files_left2copy_list) / total_size) * 100)
        popup.update()
    lbl_fc_file_copy.config(text=f"Finished copying files from FC.")
    goggles_files_left2copy_list = deepcopy(file_list)
    for file in file_list:
        lbl_goggles_file_copy.config(text=f"Goggles: copying file: {file}")
        sleep(0.1)
        del goggles_files_left2copy_list[0]
        progress_goggles_var.set((1 - file_list_size(path, goggles_files_left2copy_list) / total_size) * 100)
        popup.update()
    lbl_goggles_file_copy.config(text=f"Finished copying files from Goggles.")
    popup.destroy()

    return 0

root = tk.Tk()

tk.Button(root, text="Launch", command=button_command).pack()

root.mainloop()