from yamspy import MSPy
from utils.helper_functions import get_btfl_port, convert_to_mode_input


def do_nothing():
    pass


def get_aux(board):
    data = board.send_RAW_msg(MSPy.MSPCodes["MSP_MODE_RANGES"], [])
    dataHandler = board.receive_msg()
    board.process_recv_data(dataHandler)
    return board.MODE_RANGES


def get_active_aux_ch(aux):
    return [ch for ch in aux if ch['range']['end'] > 900]


def search_id_aux_ch(id, aux):
    id_aux_ch = [[i, ch] for i, ch in enumerate(aux) if ch['id'] == id]
    if len(id_aux_ch) == 0:
        return False
    else:
        id_aux_ch[0][1]["index"] = id_aux_ch[0][0]
        return id_aux_ch[0][1]


def bb_w_arm():
    AUX_ID = {"arm": 0, "beeper": 13, "blackbox": 26}
    serial_port = get_btfl_port()
    with MSPy(device=serial_port, loglevel='WARNING') as board:
        aux = get_aux(board)
        active_ch = get_active_aux_ch(aux)
        active_ch_len = len(active_ch)

        # New FC, no AUX was not set:
        if active_ch_len == 0:
            return "Error: Switches were not set.\nPlease set Arm switch in Betaflight Modes tab and try again."
        arm_ch = search_id_aux_ch(AUX_ID["arm"], active_ch)

        # New FC, Arm AUX was not set:
        if arm_ch is False:
            return "Error: Arm switch was not set.\nPlease set it in Betaflight Modes tab and try again."

        # Arm was set without AUX channel:
        if arm_ch['auxChannelIndex'] == 255:
            return "Error: Arm switch AUX is set to AUTO.\nPlease set it to a specific AUX switch in Betaflight Modes tab and try again."

        bb_ch = search_id_aux_ch(AUX_ID["blackbox"], active_ch)
        # Blackbox AUX was NOT set yet:
        if bb_ch is False:
            msg = [
                active_ch_len,
                AUX_ID["blackbox"],
                arm_ch['auxChannelIndex'],
                convert_to_mode_input(arm_ch['range']['start']),
                convert_to_mode_input(arm_ch['range']['end']),
                0,
                0
            ]
        # Blackbox AUX was set:
        else:
            if bb_ch['auxChannelIndex'] == arm_ch['auxChannelIndex'] and arm_ch['range']['start'] == bb_ch['range']['start'] and arm_ch['range']['end'] == bb_ch['range']['end']:
                return True
            else:
                msg = [
                    bb_ch['index'],
                    AUX_ID["blackbox"],
                    arm_ch['auxChannelIndex'],
                    convert_to_mode_input(arm_ch['range']['start']),
                    convert_to_mode_input(arm_ch['range']['end']),
                    0, 0
                ]
        data = board.send_RAW_msg(MSPy.MSPCodes["MSP_SET_MODE_RANGE"], bytearray(msg))
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)
    # TODO: BB rate and config
    return bb_w_arm()


def get_data_flash():
    serial_port = get_btfl_port()
    with MSPy(device=serial_port, loglevel='WARNING') as board:
        data = board.send_RAW_msg(MSPy.MSPCodes["MSP_DATAFLASH_SUMMARY"], [])
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)
        return board.DATAFLASH


def erase_flash():
    serial_port = get_btfl_port()
    with MSPy(device=serial_port, loglevel='WARNING') as board:
        board.send_RAW_msg(MSPy.MSPCodes['MSP_DATAFLASH_ERASE'], data=[])
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)


if __name__ == '__main__':
    print(get_data_flash())