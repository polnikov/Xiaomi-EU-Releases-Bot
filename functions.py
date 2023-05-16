import json
import requests

from typing import List
from bs4 import BeautifulSoup


URL = 'https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv14/'


def transform_version(firmware: str) -> str:
    version = firmware.split('_')[-2].lower().replace('v', '').split('.')[:-1]
    version = list(map(int, version))
    return version


def get_rom_name(firmware: str) -> str:
    firmware_list = firmware.split('_')
    if len(firmware_list) == 5:
        rom = firmware_list[2].lower()
        return rom
    elif len(firmware_list) == 6:
        rom = [firmware_list[2].lower(), firmware_list[3].lower()]
        return rom


def get_list_of_firmwares() -> List[dict]:
    '''
        [{rom: rom, data: ([version], link)}]
        [{rom: [], data: ([version], link)}]
    '''
    response = requests.get(URL)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'id': 'files_list'}).find('tbody')
    rows = table.find_all('tr')

    raw_data = [(row.find('th').a['href'], row.find('th').a['title'].replace('Click to download ', '').replace('.zip', '')) for row in rows]
    raw_data_list = list(map(lambda x: {'rom': get_rom_name(x[1]), 'version': transform_version(x[1]), 'link': x[0]}, raw_data))

    data_list = []
    for data in raw_data_list:
        rom = data.get('rom')
        if isinstance(rom, str):
            data_list.append(data)
        else:
            one = {'rom': rom[0], 'version': data.get('version'), 'link': data.get('link')}
            data_list.append(one)
            two = {'rom': rom[1], 'version': data.get('version'), 'link': data.get('link')}
            data_list.append(two)

    roms = []
    for data in data_list:
        data_rom = data.get('rom')
        if isinstance(data_rom, str):
            roms.append(data_rom)
        else:
            roms.append(data_rom[0])
            roms.append(data_rom[1])
    roms = set(roms)

    data = []
    for rom in roms:
        rom_data = list(filter(lambda x: x['rom'] == rom, data_list))
        max_v = max(rom_data, key=lambda x: x['version'])
        new = {'rom': rom, 'data': (max_v['version'], max_v['link'])}
        data.append(new)
    return data


def get_firmware_amount() -> dict:
    response = requests.get(URL)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    value = soup.find('table', {'id': 'files_list'}).find('tfoot').find('td', {'id': 'totals'}).text.split()[1]
    if value:
        data = {"value": int(value)}
    else:
        data = {"value": 0}
    return data


def save_firmware_amount(data) -> None:
    with open('firmware_amount.json', 'w') as file:
        json.dump(data, file)


def read_firmware_amount() -> int:
    with open('firmware_amount.json', 'r') as file:
        data = json.load(file)
    value = data['value']
    return value
