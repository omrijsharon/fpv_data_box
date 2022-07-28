from utils.helper_functions import get_btfl_port, get_dir, identifier_btfl, identifier_goggles


def update_fc_state(fc_state, fc_port, fc_dir, toggle_fc):
    #is FC connected in MSP mode?
    toggle_fc.set(False)
    result = get_btfl_port()
    if result is not None:
        if fc_state.get() == 0 or fc_state.get() == 2:
            toggle_fc.set(True)
        fc_state.set(1)
        fc_port.set(result)
        return

    #is  FC connected in FLASH mode?
    result = get_dir(identifier_btfl)
    if result is not None:
        fc_state.set(2)
        fc_dir.set(result)
        return

    #is FC is disconnected?
    fc_state.set(0)
    fc_port.set("")
    fc_dir.set("")
    return


def update_bottuns_by_state(fc_state, goggles_state, btn_erase_flash, btn_copy, btn_arm_bb):
    if fc_state.get() == 0:
        btn_erase_flash.config(state="disabled")
        btn_copy.config(state="disabled")
        btn_arm_bb.config(state="disabled")
    elif fc_state.get() == 1:
        btn_erase_flash.config(state="normal")
        btn_arm_bb.config(state="normal")
        btn_copy.config(state="disabled")
    elif fc_state.get() == 2:
        btn_erase_flash.config(state="disabled")
        btn_arm_bb.config(state="disabled")
        if goggles_state.get() == 0:
            btn_copy.config(state="disabled")
        elif goggles_state.get() == 1:
            btn_copy.config(state="normal")


def update_goggles_state(goggles_state, goggles_dir):
    #are Goggles connected?
    result = get_dir(identifier_goggles)
    if result is not None:
        goggles_state.set(1)
        goggles_dir.set(result)
        return None

    #are Goggles disconnected?
    goggles_state.set(0)
    goggles_dir.set("")
    return None


def map_fc_state_to_string(state):
    if state == 0:
        return "Disconnected"
    elif state == 1:
        return "MSP mode"
    elif state == 2:
        return "FLASH mode"
    else:
        return "Unknown"


def map_goggles_state_to_string(state):
    if state == 0:
        return "Disconnected"
    elif state == 1:
        return "Connected"
    else:
        return "Unknown"