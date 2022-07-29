import os
import shutil
import argparse
import time
from datetime import datetime
# from yamspy import MSPy
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from utils.state_change import update_fc_state, update_goggles_state, map_fc_state_to_string, map_goggles_state_to_string, update_bottuns_by_state
from utils.msp_functions import do_nothing, bb_w_arm, get_data_flash, erase_flash, reboot_flash_mode
from utils.helper_functions import is_config
from functools import partial
from config_menu import config_menu


def erase_flash_ui():
    answer = messagebox.askokcancel("Erase Flash", "Delete all logs from blackbox?")
    if answer:
        erase_flash()
        # messagebox.showinfo("Erase Flash", "Success!\nFlash erased")
    else:
        pass
        # messagebox.showinfo("Erase Flash", "Cancelled")


def reboot_flash_mode_ui():
    btn_reboot_flash_mode.config(state="disabled")
    lbl_fc.config(text=f"FC: Entering Flash Mode...")
    window.update()
    reboot_flash_mode()


def bb_w_arm_ui():
    msg = bb_w_arm()
    if msg == True:
        messagebox.showinfo("Record Blackbox when Armed", "Success!\nBlackbox will be recorded when armed")
    else:
        messagebox.showerror("Record Blackbox when Armed", msg)


def fc_general_on_enter(event):
    if fc_state.get() == 0:
        lbl_assistant.config(text="Button will be activated when Flight Controller is connected")
    elif fc_state.get() == 1:
        lbl_assistant.config(text="")
    elif fc_state.get() == 2:
        lbl_assistant.config(text="Flight Controller in flash mode. Disconnect, reconnect it.")


def copy_on_enter(event):
    if fc_state.get() == 0:
        lbl_assistant.config(text="Button will be activated when Flight Controller is connected")
    elif fc_state.get() == 1:
        lbl_assistant.config(text="")
        if goggles_state.get() == 0:
            lbl_assistant.config(text="Button will be activated when Goggles SD is connected")
    elif fc_state.get() == 2:
        lbl_assistant.config(text="")
        if goggles_state.get() == 0:
            lbl_assistant.config(text="Button will be activated when the Goggles SD card is connected")


def on_leave(event):
    lbl_assistant.config(text="")


def Refresher():
    update_fc_state(fc_state, fc_port, fc_dir, toggle_fc)
    update_goggles_state(goggles_state, goggles_dir)
    lbl_fc.config(text=f"FC: {map_fc_state_to_string(fc_state.get())}")
    lbl_goggles.config(text=f"Goggles: {map_goggles_state_to_string(goggles_state.get())}")
    update_bottuns_by_state(fc_state, goggles_state, btn_erase_flash, btn_copy, btn_arm_bb, btn_reboot_flash_mode)
    if fc_state.get() == 1 and toggle_fc.get():
        data_flash = get_data_flash()
        if data_flash["ready"] and data_flash["supported"]:
            flash_used_space.set(data_flash["usedSize"])
            flash_total_space.set(data_flash["totalSize"])
            progbar_value.set(100 * flash_used_space.get() / flash_total_space.get())
            progbar.config(value=progbar_value.get())
            lbl_progbar_value.config(text="{}%".format(round(progbar_value.get())))
            lbl_progbar_free.config(text=f"Free Space: {round((flash_total_space.get() - flash_used_space.get()) / 2 ** 20, 2)} MB")
            lbl_progbar_used.config(text=f"Used Space: {round(flash_used_space.get() / 2 ** 20, 2)} MB")
    elif fc_state.get() == 0 or fc_state.get() == 2:
        progbar_value.set(0)
        progbar.config(value=progbar_value.get())
        lbl_progbar_free.config(text="")
        lbl_progbar_used.config(text="")
        lbl_progbar_value.config(text="")
    window.after(1000, Refresher)



if __name__ == '__main__':
    window = Tk()
    window.title("FPV Data Box")
    window.geometry('480x280')
    window.resizable(False, False)
    window.attributes('-topmost', 'false')
    window.attributes("-fullscreen", True)

    # Variables
    ## FC
    toggle_fc = BooleanVar()
    toggle_fc.set(False)
    fc_state = IntVar()
    fc_state.set(0)
    fc_port = StringVar()
    fc_port.set("")
    fc_dir = StringVar()
    fc_dir.set("")

    ## Goggles
    goggles_state = IntVar()
    goggles_state.set(0)
    goggles_dir = StringVar()
    goggles_dir.set("")

    ## Misc.
    flash_used_space = DoubleVar()
    flash_used_space.set(0.0)
    flash_total_space = DoubleVar()
    flash_total_space.set(8.0)
    progbar_value = DoubleVar()

    # State Labels
    lbl_assistant = Label(window, text=f"", font=("Arial", 12))
    lbl_assistant.place(x=20, y=10)
    lbl_fc = Label(window, text="FC: {}".format(fc_state.get()), font=("Arial Bold", 12))
    lbl_fc.place(x=20, y=250)
    lbl_goggles = Label(window, text="Goggles: {}".format(goggles_state.get()), font=("Arial Bold", 12))
    lbl_goggles.place(x=285, y=250)

    # Buttons
    partial_config_menu = partial(config_menu, window, fc_dir, goggles_dir, fc_state, state=False)
    btn_config = Button(window, text="Edit\nConfig", width=6, height=2, font=("Arial", 14), command=partial_config_menu)
    btn_config.place(x=20, y=38)
    btn_arm_bb = Button(window, text="Record Blackbox\nwhen Armed", width=14, height=2, font=("Arial", 14), command=bb_w_arm_ui)
    btn_arm_bb.place(x=97, y=38)
    btn_arm_bb.bind("<Enter>", fc_general_on_enter)
    btn_arm_bb.bind("<Leave>", on_leave)
    btn_reboot_flash_mode = Button(window, text="Activate\nFlash mode", width=10, height=2, font=("Arial", 14), command=reboot_flash_mode_ui)
    btn_reboot_flash_mode.place(x=262, y=38)
    btn_reboot_flash_mode.bind("<Enter>", fc_general_on_enter)
    btn_reboot_flash_mode.bind("<Leave>", on_leave)
    btn_erase_flash = Button(window, text="Erase\nFlash", width=6, height=2, font=("Arial", 14), command=erase_flash_ui)
    btn_erase_flash.place(x=383, y=38)
    btn_erase_flash.bind("<Enter>", fc_general_on_enter)
    btn_erase_flash.bind("<Leave>", on_leave)
    partial_copy_menu = partial(config_menu, window, fc_dir, goggles_dir, fc_state, state=True)
    btn_copy = Button(window, text="Copy Log files and Videos", width=39, height=3, font=("Arial", 14), command=partial_copy_menu)
    btn_copy.place(x=20, y=100)
    btn_copy.bind("<Enter>", copy_on_enter)
    btn_copy.bind("<Leave>", on_leave)

    # Progress Bar
    progbar_value.set(100 * flash_used_space.get() / flash_total_space.get())
    progbar = ttk.Progressbar(window ,orient='horizontal',mode='determinate',length=440, value=progbar_value.get())
    progbar.place(x=20, y=190)
    lbl_progbar_free = Label(window, text=f"Free Space: {(flash_total_space.get() - flash_used_space.get()) / 2 ** 20} MB", font=("Arial", 12))
    lbl_progbar_free.place(x=295, y=215)
    lbl_progbar_used = Label(window,text=f"Used Space: {(flash_used_space.get()) / 2 ** 20} MB", font=("Arial", 12))
    lbl_progbar_used.place(x=20, y=215)
    lbl_progbar_value = Label(window, text="{}%".format(round(progbar_value.get())), font=("Arial", 12))
    lbl_progbar_value.place(x=230, y=215)

    Refresher()
    if not is_config():
        config_menu(window, fc_dir=fc_dir, goggles_dir=goggles_dir, fc_state=fc_state, state=0)
    window.mainloop()