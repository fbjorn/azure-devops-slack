import json
import os
from pathlib import Path

from invoke import task
from pydantic import SecretStr
from ruamel.yaml import YAML

from src.settings import conf

REPO_ROOT = Path(__file__).parent


@task
def obfuscate_tests(ctx):
    """
    Replace personal information in tests/samples
    """
    conf_file = REPO_ROOT / "obfuscate.yaml"
    obfuscate_conf = YAML().load(conf_file.read_text("utf8"))
    samples_dir = REPO_ROOT / "tests" / "samples"

    for path in samples_dir.glob("*.json"):
        content = path.read_text()
        for rule in obfuscate_conf:
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


def _convert_users() -> str:
    conf_file = REPO_ROOT / "users.yaml"
    users_conf = YAML().load(conf_file.read_text("utf8"))

    return json.dumps(users_conf["users"])


@task
def convert_users(ctx):
    """
    Convert users.yaml into a USERS environment variable for the settings
    """
    print(_convert_users())


@task
def deploy_cloud_function(
    ctx, gcp_project, name="devops-slack-webhook", region="europe-west3"
):
    """
    Deploy webhook as a Google Cloud Function
    :param gcp_project: Project name in Google Cloud
    :param name: Name of the cloud function
    :param region: Google Cloud region
    """
    yaml = YAML()
    deploy_yaml = "deploy.yaml"
    yaml_content = {}
    for k, v in conf.dict().items():
        if isinstance(v, SecretStr):
            yaml_content[k] = v.get_secret_value()
        elif k == "USERS":
            yaml_content[k] = json.dumps(v)
        else:
            yaml_content[k] = str(v)
    with open(deploy_yaml, "w") as f:
        yaml.dump(yaml_content, f)

    cmd = [
        f"gcloud functions deploy {name}",
        "--allow-unauthenticated",
        "--entry-point devops_webhook",
        "--runtime python310",
        "--trigger-http",
        f"--region {region}",
        f"--project {gcp_project}",
        f"--env-vars-file={deploy_yaml}",
    ]
    try:
        ctx.run(" ".join(cmd))
    finally:
        os.remove(deploy_yaml)


@task
def record_test_sample(ctx, name):
    """
    Record sample JSON event and save it to tests/samples
    :param name: Name of the file with a sample to write
    """
    os.environ["NAME"] = name
    ctx.run("poetry run functions_framework --target save_sample --debug")


@task
def backend(ctx):
    """
    Record sample JSON event and save it to tests/samples
    :param name: Name of the file with a sample to write
    """
    os.environ["PYTHONUNBUFFERED"] = "1"
    ctx.run('poetry run gunicorn "src.flask_app" -b 0.0.0.0:8000')
