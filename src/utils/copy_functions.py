import os
import shutil
import argparse
import time
from datetime import datetime
from yamspy import MSPy
import functools
from copy import deepcopy


def file_list_size(path, file_list):
    files_path = [os.path.join(path, filename) for filename in file_list]
    files_size = [os.path.getsize(file) for file in files_path]
    total_size = sum(files_size)
    return total_size


def create_current_dst_dir(dst_dir):
    dst_dir = os.path.join(dst_dir, datetime.now().strftime('%Y_%m_%d'))
    os.path.exists(dst_dir) or os.makedirs(dst_dir)
    n_batch = str(len(os.listdir(dst_dir))).zfill(4)  # max of 10000 batches a day
    current_dst_dir = os.path.join(dst_dir, n_batch)
    os.makedirs(current_dst_dir)
    return current_dst_dir


def log_files_list(fc_src, extension="bbl"):
    file_list = [filename for filename in os.listdir(fc_src) if
                 (filename.lower().split(".")[-1] == extension.lower() and (not "all" in filename.lower()))]
    return file_list


def create_dst_filename_list(file_list, drone, pilot):
    drone = drone.replace(" ", "_").replace(".", "")
    pilot = pilot.replace(" ", "_").replace(".", "")
    dst_filename_list = []
    for i, file in enumerate(file_list):
        idx = str(i).zfill(2)  # max of 100 logs in a batch
        names = f"drone_{drone}_pilot_{pilot}"  # names_dir.split("_")[1::2] to get drone and pilot
        dst_filename = f"log{idx}__" + datetime.now().strftime('%Y_%d_%m-%H_%M_%S') + "__" + names
        dst_filename_list.append(dst_filename)
    return dst_filename_list


def check_same_n_files(dst_filename_list, video_files_list):
    n_log_files = len(dst_filename_list)
    n_video_files = len(video_files_list)
    if not n_video_files == n_log_files:
        exception = f"Number of videos ({n_video_files}) and number log-files ({n_log_files}) do not match."
        return False, exception
    return True, None


def copy_log_files(copy_window, progress_var_fc, lbl_fc_file_copy,
                   fc_src, batch_dst_dir, logfile_list, dst_filename_list):
    logfile_list_left = deepcopy(logfile_list)
    total_size = file_list_size(fc_src, logfile_list)
    for src_filename, dst_filename in zip(logfile_list, dst_filename_list):
        lbl_fc_file_copy.config(text=f"FC: copying file: {src_filename}")
        src_file = os.path.join(fc_src, src_filename)
        dst_file = os.path.join(batch_dst_dir, dst_filename + ".bbl")
        shutil.copy(src_file, dst_file)
        del logfile_list_left[0]
        progress_var_fc.set((1 - file_list_size(fc_src, logfile_list_left) / total_size) * 100)
        copy_window.update()
    lbl_fc_file_copy.config(text=f"Finished copying files from FC.")
    return True


def copy_video_files(copy_window, progress_goggles_var, lbl_goggles_file_copy,
                     video_src, batch_dst_dir, video_files_list, dst_filename_list):
    video_files_list_left = deepcopy(video_files_list)
    total_size = file_list_size(video_src, video_files_list)
    for n, dst_file in enumerate(dst_filename_list):
        src_filename = video_files_list[n]
        lbl_goggles_file_copy.config(text=f"Video: copying file: {src_filename}")
        src_extension = src_filename.split(".")[-1]
        dst_filename = dst_file + "." + src_extension
        src_file = os.path.join(video_src, src_filename)
        dst_file_w_extension = os.path.join(batch_dst_dir, dst_filename)
        shutil.copy(src_file, dst_file_w_extension)
        del video_files_list_left[0]
        progress_goggles_var.set((1 - file_list_size(video_src, video_files_list_left) / total_size) * 100)
        copy_window.update()
        # Legacy code: copy both video and srt files
        """
        even = 2 * n
        odd = 2 * n + 1
        for k in [even, odd]:
            src_filename = video_files_list[k]
            lbl_goggles_file_copy.config(text=f"Goggles: copying file: {src_filename}")
            src_extension = src_filename.split(".")[-1]
            dst_filename = dst_file + "." + src_extension
            src_file = os.path.join(video_src, src_filename)
            dst_file_w_extension = os.path.join(batch_dst_dir, dst_filename)
            shutil.copy(src_file, dst_file_w_extension)
            del video_files_list_left[0]
            progress_goggles_var.set((1 - file_list_size(video_src, video_files_list_left) / total_size) * 100)
            copy_window.update()
        """
    lbl_goggles_file_copy.config(text=f"Finished copying video files.")
    return True
