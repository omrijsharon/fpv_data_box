from yamspy import MSPy


def do_nothing():
    pass


def erase_flash(serial_port):
    with MSPy(device=serial_port, loglevel='WARNING') as board:
        board.send_RAW_msg(MSPy.MSPCodes['MSP_DATAFLASH_ERASE'], data=[])
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)