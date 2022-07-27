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
from utils.msp_functions import do_nothing, bb_w_arm
from utils.helper_functions import is_config
from functools import partial
from config_menu import config_menu


def bb_w_arm_ui():
    msg = bb_w_arm()
    if msg == True:
        messagebox.showinfo("Record Blackbox when Armed", "Success!\nBlackbox will be recorded when armed")
    else:
        messagebox.showerror("Record Blackbox when Armed", msg)


def Refresher():
    update_fc_state(fc_state, fc_port, fc_dir)
    update_goggles_state(goggles_state, goggles_dir)
    lbl_fc.config(text=f"FC: {map_fc_state_to_string(fc_state.get())}")
    lbl_goggles.config(text=f"Goggles: {map_goggles_state_to_string(goggles_state.get())}")
    update_bottuns_by_state(fc_state, goggles_state, btn_erase_flash, btn_copy)
    window.after(1000, Refresher)


if __name__ == '__main__':
    window = Tk()
    window.title("FPV Data Box")
    window.geometry('480x280')
    window.resizable(False, False)
    window.attributes('-topmost', 'false')
    # Variables
    ## FC
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
    last_action = StringVar()
    last_action.set("")
    flash_used_space = DoubleVar()
    flash_used_space.set(3.0)
    flash_total_space = DoubleVar()
    flash_total_space.set(8.0)
    progbar_value = DoubleVar()

    # State Labels
    lbl_last_action = Label(window, text=f"Last Action: {last_action.get()}", font=("Arial", 12))
    lbl_last_action.place(x=20, y=10)
    lbl_fc = Label(window, text="FC: {}".format(fc_state.get()), font=("Arial Bold", 12))
    lbl_fc.place(x=20, y=250)
    lbl_goggles = Label(window, text="Goggles: {}".format(goggles_state.get()), font=("Arial Bold", 12))
    lbl_goggles.place(x=285, y=250)

    # Buttons
    btn_erase_flash = Button(window, text="Erase\nFlash", width=7, height=3, font=("Arial", 14), command=do_nothing)
    btn_erase_flash.place(x=372, y=100)
    btn_copy = Button(window, text="Copy Log files and Videos", width=31, height=3, font=("Arial", 14), command=do_nothing)
    btn_copy.place(x=20, y=100)
    config_state = fc_state.get() and goggles_state.get()
    partial_config_menu = partial(config_menu, window,fc_dir, goggles_dir, config_state)
    btn_config = Button(window, text="Configuration", width=24, height=2, font=("Arial", 14), command=partial_config_menu)
    btn_config.place(x=20, y=38)
    btn_arm_bb = Button(window, text="Record Blackbox\nwhen Armed", width=14, height=2, font=("Arial", 14), command=bb_w_arm_ui)
    btn_arm_bb.place(x=295, y=38)

    # Progress Bar
    progbar_value.set(100*flash_used_space.get() / flash_total_space.get())
    progbar = ttk.Progressbar(window ,orient='horizontal',mode='determinate',length=440, value=progbar_value.get())
    progbar.place(x=20, y=190)
    lbl_progbar = Label(window, text=f"Free Space: {flash_total_space.get() - flash_used_space.get()} MB", font=("Arial", 12))
    lbl_progbar.place(x=165, y=215)

    Refresher()
    if not is_config():
        config_menu(window, fc_dir=fc_dir, goggles_dir=goggles_dir, state=0)
    window.mainloop()