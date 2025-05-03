import csv
import json
import sys
import jmespath
from rich.console import Console
from rich.table import Table

from .options import OutputOption

console = Console()


def print_beauty(list_of_dict: list[dict], output: OutputOption) -> None:
    table_headers = list_of_dict[0].keys()
    if output == OutputOption.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=table_headers)
        writer.writeheader()
        writer.writerows(list_of_dict)
    elif output == OutputOption.json:
        console.print_json(json.dumps(list_of_dict))
    elif output == OutputOption.table:
        table = Table(show_lines=True, expand=True)
        # Define a list of colors to cycle through for the columns
        colors = ["red", "green", "blue", "magenta", "cyan", "yellow", "purple"]

        # Add index column
        table.add_column("#", style="bold", width=5)

        # Add columns with different colors and proper width handling
        for i, header in enumerate(table_headers):
            color = colors[
                i % len(colors)
            ]  # Cycle through colors if more columns than colors
            # Set appropriate width for different column types
            if header.lower() in ["description", "url"]:
                table.add_column(
                    header, style=color, width=30, overflow="fold", no_wrap=False
                )
            elif header.lower() in ["name", "language"]:
                table.add_column(header, style=color, width=15, overflow="fold")
            else:
                table.add_column(header, style=color, width=10)

        for row in list_of_dict:
            table.add_row(
                *[str(list_of_dict.index(row) + 1)] + [str(row) for row in row.values()]
            )
        console.print(table)
    else:
        raise ValueError(f"Unsupported output option: {output}")


def sort_by_key(list_of_dict: list[dict], key: str, reverse: bool = False):
    """
    Sort a list of dictionaries by a specified key.

    Args:
        list_of_dict (list[dict]): The list of dictionaries to sort.
        key (str): The key to sort by.
        reverse (bool): Whether to sort in reverse order. Defaults to False.

    Returns:
        list[dict]: The sorted list of dictionaries.
    """
    expr = f"sort_by(@,&{key})"
    if reverse:
        expr += ".reverse(@)"
    return jmespath.search(expr, list_of_dict)
