from yamspy import MSPy

from utils.helper_functions import get_btfl_port, convert_to_mode_input


serial_port = get_btfl_port()
with MSPy(device=serial_port, loglevel='WARNING') as board:
    # msg: [sequence id, permanentId, auxChannelIndex, rangeStartStep, rangeEndStep, ?, ?]
    msg = [1, 26, 0, convert_to_mode_input(1700), convert_to_mode_input(2100), 0, 0]
    data = board.send_RAW_msg(MSPy.MSPCodes["MSP_SET_MODE_RANGE"], bytearray(msg))
    # data = board.send_RAW_msg(MSPy.MSPCodes["MSP_MODE_RANGES"], [])
    dataHandler = board.receive_msg()
    board.process_recv_data(dataHandler)
    # data = board.send_RAW_msg(MSPy.MSPCodes["MSP_MODE_RANGES"], [])
    # dataHandler = board.receive_msg()
    # board.process_recv_data(dataHandler)
    # aux = board.MODE_RANGES
    # only_active = [ch for ch in aux if ch['range']['end'] > 900]
    # arm_switch = [ch for ch in only_active if ch["id"] == 0][0]
    # print(only_active)
    # # print(board.AUX_CONFIG_IDS)