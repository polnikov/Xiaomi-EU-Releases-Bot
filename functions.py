import requests

from typing import List
from bs4 import BeautifulSoup


def transform_version(firmware: str) -> str:
    version = firmware.split('_')[-2].lower().replace('v', '').split('.')[:-1]
    version = list(map(int, version))
    return version


def get_rom_name(firmware: str) -> str:
    firmware_list = firmware.split('_')
    if len(firmware_list) == 5:
        rom = firmware.split('_')[2].lower()
        return rom
    elif len(firmware_list) == 6:
        rom = '_'.join(firmware.split('_')[2:4]).lower()
        return rom


def get_list_of_firmwares() -> List[dict]:
    '''[{rom: rom, data: ([version], link)}]'''
    URL = 'https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv14/'
    response = requests.get(URL)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'id': 'files_list'}).find('tbody')
    rows = table.find_all('tr')

    raw_data_list = [(row.find('th').a['href'], row.find('th').a['title'].replace('Click to download ', '').replace('.zip', '')) for row in rows]
    data_list = list(map(lambda x: {'rom': get_rom_name(x[1]), 'version': transform_version(x[1]), 'link': x[0]}, raw_data_list))

    data = []
    roms = set(map(lambda x: x['rom'], data_list))
    for rom in roms:
        rom_data = list(filter(lambda x: x['rom'] == rom, data_list))
        max_v = max(rom_data, key=lambda x: x['version'])
        new = {'rom': rom, 'data': (max_v['version'], max_v['link'])}
        data.append(new)
    return data


def get_firmware_amount() -> int:  # 121
    URL = 'https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv14/'
    response = requests.get(URL)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    value = soup.find('table', {'id': 'files_list'}).find('tfoot').find('td', {'id': 'totals'}).text.split()[1]
    return value
