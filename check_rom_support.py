from logger import logger

from roms import ROMS


def check_rom_support(rom):
    logger.info(f'Checking ROM [{rom}] in support ROMs')
    for r in ROMS:
        if rom in r:
            return True
    logger.error(f'ROM [{rom}] is not support')
