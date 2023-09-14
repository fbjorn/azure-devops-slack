import json
from pathlib import Path

from ruamel.yaml import YAML

conf_file = Path(__file__).parent / "obfuscate.yaml"
conf = YAML().load(conf_file.read_text("utf8"))
samples_dir = Path(__file__).parent / "tests" / "samples"


for path in samples_dir.glob("*.json"):
    content = path.read_text()
    for rule in conf:
        if not rule.get("from") and not rule.get("into"):
            continue
        content = content.replace(rule["from"], rule["into"])
    j = json.loads(content)
    if (
        j.get("resource", {})
        .get("pullRequest", {})
        .get("repository", {})
        .get("project", {})
    ):
        j["resource"]["pullRequest"]["repository"]["project"]["description"] = "--"
    if j.get("resource", {}).get("repository", {}).get("project", {}):
        j["resource"]["repository"]["project"]["description"] = "--"

    path.write_text(json.dumps(j, indent=2))
    print(f"{path} fixed")
