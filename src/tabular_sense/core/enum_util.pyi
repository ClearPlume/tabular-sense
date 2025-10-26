from enum import IntEnum


class ColumnType(IntEnum):
    AGE = 0
    AMOUNT = 1
    BANK_CARD = 2
    COORDINATE = 3
    DATE = 4
    DATETIME = 5
    EMAIL = 6
    FLOAT = 7
    ID_CARD = 8
    INT = 9
    IP = 10
    JOB = 11
    NAME = 12
    PERCENT = 13
    PHONE = 14
    PLATE = 15
    TIME = 16
    URL = 17
    USERAGENT = 18
    USERNAME = 19
    BOOLEAN = 20
    EDUCATION = 21
    ETHNICITY = 22
    GENDER = 23
    PRIORITY = 24
    STATE = 25
    ADDRESS = 26
    COMPANY = 27
    HOSPITAL = 28
    RECREATION = 29
    RESIDENTIAL = 30
    SHOPPING = 31

    @staticmethod
    def to_multiple_label(*types: ColumnType) -> list[int]: ...

    @staticmethod
    def from_multiple_label(vector: list[int]) -> list[ColumnType]: ...


def to_multiple_label(*types: ColumnType) -> list[int]: ...


def from_multiple_label(vector: list[int]) -> list[ColumnType]: ...
