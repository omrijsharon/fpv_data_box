import serial.tools.list_ports
import platform
import os
import yaml


def yaml_writer(file_name, data):
    with open(file_name, "w") as f:
        yaml.dump(data, f)


def yaml_reader(file_name):
    with open(file_name, "r") as f:
        return yaml.safe_load(f)


def is_config():
    # print(os.listdir(os.path.join(os.getcwd(), "config")))
    return len(os.listdir(os.path.join(os.getcwd(), "config"))) > 1


def get_btfl_port(): #MSP mode
    for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
        if "betaflight" in desc.lower() or "stmicroelectronics" in desc.lower():
            # print("{}: {} [{}]".format(port, desc, hwid))
            return port
    return None


def convert_to_mode_input(pwm):
    """
    value for this element in 'blocks' of 25 where 0 == 900 and 48 == 2100
    :param pwm: value between 900 and 2100
    :return: value between 0 and 48
    """
    return int((pwm - 900) / 25)


def get_os():
    return platform.system()


def get_path_in_media_linux(sub_path_list):
    """
    :param path_list: a list of dir and subdirs. i.e.: ["DCIM", "100MEDIA"]
    :return: path to desired dir
    """
    for user in os.listdir("/media"):
        user_path = os.path.join("/media", user, *sub_path_list)
        if os.path.exists(user_path):
            return user_path
    return None


def identifier_goggles(disk=None):
    if get_os() == "Windows":
        goggles_dir = os.path.join(disk.Name, "DCIM", "100MEDIA")
        if os.path.exists(goggles_dir):
            return goggles_dir
    elif get_os() == "Linux":
        return get_path_in_media_linux(["DCIM", "100MEDIA"])
    else:
        raise NotImplementedError("OS not supported")
    return None


def identifier_btfl(disk=None): #FLASH mode
    if get_os() == "Windows":
        if disk.VolumeName=="BETAFLT":
            return disk.Name
    elif get_os() == "Linux":
        return get_path_in_media_linux(["BETAFLT"])
    else:
        raise NotImplementedError("OS not supported")
    return None


def get_dir(identifier_func):
    if get_os() == "Windows":
        import wmi
        c = wmi.WMI()
        for disk in c.Win32_LogicalDisk():
            if disk.Description == "Removable Disk":
                result = identifier_func(disk)
                if result:
                    return result
    elif get_os() == "Linux":
        return identifier_func()
    else:
        raise NotImplementedError("OS not supported")
    return None


if __name__ == '__main__':
    print(convert_to_mode_input(900), convert_to_mode_input(2100))
