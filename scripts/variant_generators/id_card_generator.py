from datetime import datetime
from enum import Enum
from random import Random
from typing import Optional

from faker import Faker

from src.tabular_sense.core.utils import calculate_id_card_checksum
from src.tabular_sense.path import get_data_dir


class IdCardFormat(Enum):
    """身份证格式"""

    STANDARD = "{area}{date}{seq}{verify}"
    SPACE = "{area} {date} {seq}{verify}"
    DASH = "{area}-{date}-{seq}{verify}"

    def format(self, area: str, date: str, seq: str, verify: str) -> str:
        return self.value.format(area=area, date=date, seq=seq, verify=verify)


class IdCardGenerator:
    """身份证生成"""

    rng: Optional[Random] = None
    areas: Optional[list[str]] = None

    def __init__(self):
        if self.rng is None:
            self.rng = Random()

        if self.areas is None:
            seed_dir = get_data_dir() / "seed"

            with open(seed_dir / "area.txt", "r", encoding="utf-8") as area_file:
                self.areas = area_file.read().splitlines()

    def __call__(self, fmt: IdCardFormat):
        faker = Faker("zh_CN")

        if self.rng.random() < 0.5:
            area = self.rng.choice(self.areas)
            date = faker.date_between(start_date=datetime(1920, 1, 1), end_date=datetime(2010, 12, 31)) \
                .strftime('%Y%m%d')
            seq = f"{self.rng.randint(0, 999):03d}"
            checksum = calculate_id_card_checksum(area + date + seq)
        else:
            area = self.rng.choice(self.areas)
            date = faker.date_between(start_date=datetime(1920, 1, 1), end_date=datetime(1999, 12, 31)) \
                .strftime('%y%m%d')
            seq = f"{self.rng.randint(0, 999):03d}"
            checksum = ""

        return fmt.format(area, date, seq, checksum)


def id_cards(num: int) -> list[str]:
    generator = IdCardGenerator()
    fmt = generator.rng.choice(list(IdCardFormat))
    samples = []

    for _ in range(num):
        samples.append(generator(fmt))

    return samples
