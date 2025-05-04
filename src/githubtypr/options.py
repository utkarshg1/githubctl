from enum import Enum


class OutputOption(str, Enum):
    table = "table"
    json = "json"
    csv = "csv"
