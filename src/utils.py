import re


def convert_links_to_slack_md(text: str) -> str:
    res = re.sub(r"\[(.*?)\]\((.*?)\)", r"<\2|\1>", text)
    return res
