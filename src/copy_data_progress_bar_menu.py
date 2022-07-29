import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from time import sleep
from copy import deepcopy
from utils.copy_functions import *
from utils.helper_functions import get_btfl_port, get_dir, identifier_btfl, identifier_goggles


def copy_all_data(fc_src, googles_src, dst_dir, drone, pilot):
    def cancel_command():
        answer = messagebox.askyesno("Cancel copy", "Are you sure you want to cancel copying files?")
        if answer:
            copy_window.destroy()


    #start progress bar
    copy_window = tk.Toplevel()
    copy_window.geometry('250x150')
    copy_window.resizable(False, False)
    copy_window.title("Copying files...")
    copy_window.attributes('-topmost', True)
    btn_cancel = tk.Button(copy_window, text="Cancel", command=cancel_command)
    btn_cancel.place(x=98, y=110)

    lbl_fc_file_copy = tk.Label(copy_window, text="FC: copying file: ")
    lbl_fc_file_copy.place(x=18, y=10)
    progress_var_fc = tk.DoubleVar()
    progress_var_fc.set(0)
    progress_bar_fc = ttk.Progressbar(copy_window, variable=progress_var_fc, maximum=100)
    progress_bar_fc.place(x=20, y=30, width=210, height=20)

    lbl_goggles_file_copy = tk.Label(copy_window, text="Goggles: copying file: ")
    lbl_goggles_file_copy.place(x=18, y=58)
    progress_goggles_var = tk.DoubleVar()
    progress_goggles_var.set(0)
    progress_bar_goggles = ttk.Progressbar(copy_window, variable=progress_goggles_var, maximum=100)
    progress_bar_goggles.place(x=20, y=80, width=210, height=20)

    copy_window.update()

    ## copy all data - here starts the original function
    batch_dst_dir = create_current_dst_dir(dst_dir)

    logfile_list = log_files_list(fc_src)
    logfile_list_len = len(logfile_list)
    video_srt_files_list = os.listdir(googles_src)[-2 * logfile_list_len:]

    dst_filename_list = create_dst_filename_list(logfile_list, drone, pilot)
    #dst_filename_list[0].split("__")[-1].split("_")[1::2] # get drone and pilot of the first file

    is_equal, exception = check_same_n_files(dst_filename_list, video_srt_files_list)
    if not is_equal:
        return False, exception

    # Copies BBL files
    if not copy_log_files(copy_window, progress_var_fc, lbl_fc_file_copy,
                          fc_src, batch_dst_dir, logfile_list, dst_filename_list):
        return False, "Error copying BBL files"

    # Copies MP4 and SRT files
    if not copy_video_files(copy_window, progress_goggles_var, lbl_goggles_file_copy,
                            googles_src, batch_dst_dir, video_srt_files_list, dst_filename_list):
        return False, "Error copying MP4 and SRT files"

    copy_window.destroy()
    copy_window.update()
    return True, None

if __name__ == '__main__':
    fc_src = get_dir(identifier_btfl)
    logfile_list = log_files_list(fc_src)
    print(file_list_size(fc_src, logfile_list))