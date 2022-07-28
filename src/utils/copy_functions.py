import os
import shutil
import argparse
import time
from datetime import datetime
from yamspy import MSPy
import functools


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
    dst_filename_list = []
    for i, file in enumerate(file_list):
        idx = str(i).zfill(2)  # max of 100 logs in a batch
        names = f"drone_{drone}_pilot_{pilot}"  # names_dir.split("_")[1::2] to get drone and pilot
        dst_filename = f"log{idx}__" + datetime.now().strftime('%Y_%d_%m-%H_%M_%S') + "__" + names
        dst_filename_list.append(dst_filename)
    return dst_filename_list


def check_same_n_files(dst_filename_list, video_srt_files_list):
    n_log_files = len(dst_filename_list)
    n_video_files = int(len(video_srt_files_list) / 2)
    if not n_video_files == n_log_files:
        exception = f"Number of videos ({n_video_files}) and number log-files ({n_log_files}) do not match."
        return False, exception
    return True, None


def copy_log_files(fc_src, batch_dst_dir, logfile_list, dst_filename_list):
    for src_filename, dst_filename in zip(logfile_list, dst_filename_list):
        src_file = os.path.join(fc_src, src_filename)
        dst_file = os.path.join(batch_dst_dir, dst_filename + ".bbl")
        shutil.copy(src_file, batch_dst_dir)
    return True


def copy_video_files(googles_src, batch_dst_dir, video_srt_files_list, dst_filename_list):
    for n, dst_file in enumerate(dst_filename_list):
        even = 2 * n
        odd = 2 * n + 1
        for k in [even, odd]:
            src_filename = video_srt_files_list[k]
            src_extension = src_filename.split(".")[-1]
            dst_filename = dst_file + "." + src_extension
            src_file = os.path.join(googles_src, src_filename)
            dst_file_w_extension = os.path.join(batch_dst_dir, dst_filename)
            shutil.copy(src_file, dst_file_w_extension)
    return True


def copy_all_data(fc_src, googles_src, dst_dir, drone, pilot):
    # TODO: move to progress bar menu
    batch_dst_dir = create_current_dst_dir(dst_dir)

    logfile_list = log_files_list(fc_src)
    logfile_list_len = len(logfile_list)
    video_srt_files_list = os.listdir(googles_src)[-2 * logfile_list_len:]

    dst_filename_list = create_dst_filename_list(logfile_list, drone, pilot)

    is_equal, exception = check_same_n_files(dst_filename_list, video_srt_files_list)
    if not is_equal:
        return False, exception

    # Copies BBL files
    if not copy_log_files(fc_src, batch_dst_dir, logfile_list, dst_filename_list):
        return False, "Error copying BBL files"

    # Copies MP4 and SRT files
    if not copy_video_files(googles_src, batch_dst_dir, video_srt_files_list, dst_filename_list):
        return False, "Error copying MP4 and SRT files"
    return True, None
