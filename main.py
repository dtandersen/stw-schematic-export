import json
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


@dataclass
class Schematic:
    name: str
    rarity: str
    stars: str
    perks: List[str]
    schematic_type: str
    material: str


def load_schematics(file) -> List[Schematic]:
    schematics = []

    soup = parse_schematics(file)
    schematic_elements = soup.findAll("div", {"class": "item-wrapper"})

    for schematic in schematic_elements:
        name = schematic.get('data-name')
        rarity = schematic.get('data-rarity')
        stars = schematic.get('data-stars')
        perks = schematic.get('data-perks')
        perks_descriptions = deserialize_perks(perks)
        schematic_type = schematic.get('data-type')
        material = schematic.get('data-material')

        weapon = Schematic(name=name.strip(),
                           rarity=rarity,
                           stars=stars,
                           perks=perks_descriptions,
                           schematic_type=schematic_type,
                           material=material)

        schematics.append(weapon)

    return schematics


def parse_schematics(file):
    html = read_schematics(file)
    soup = BeautifulSoup(html, 'html.parser')

    return soup


def read_schematics(file: str):
    file = open(file, mode='r', encoding="utf-8")
    html = file.read()
    file.close()

    return html


def deserialize_perks(perks) -> List[str]:
    data = json.loads(perks)
    perks = [d['d'] for d in data]
    return perks


def print_schematics(schematics: List[Schematic]):
    for schematic in schematics:
        perks = "|".join(schematic.perks)
        print(f"{schematic.name}|{schematic.schematic_type}|{schematic.rarity}|{perks}")


def main():
    schematics = load_schematics('schematics.html')
    print_schematics(schematics)


if __name__ == '__main__':
    main()
