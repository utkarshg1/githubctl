import jmespath
import json
from rich.console import Console

console = Console()

with open("tests/people.json", "r") as f:
    data = json.load(f)

console.print(data)

search = "people[?(age == `28`)]"
result = jmespath.search(search, data)
console.print(result)
