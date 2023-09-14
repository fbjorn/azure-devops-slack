import json
from pathlib import Path

from ruamel.yaml import YAML

conf_file = Path(__file__).parent / "users.yaml"
conf = YAML().load(conf_file.read_text("utf8"))

print(json.dumps(conf["users"]))
