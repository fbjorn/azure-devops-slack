# Installation

```shell
poetry install
```

Debug locally:

```bash
poetry run functions_framework --target devops_webhook --debug

poetry run functions_framework --target save_sample --debug
```

# Deploy

```bash
poetry export > requirements.txt

gcloud functions deploy devops-slack-webhook --allow-unauthenticated --entry-point devops_webhook --runtime python310 --trigger-http --region europe-west3 --project <>
```

# Local development

## Recording Azure DevOps events for unit tests

```shell

NAME=foo poetry run functions_framework --target save_sample --debug
```

This will create a `foo.json` under [tests/samples](./tests/samples) and you can use
this file for testing

## Obfuscation of IDs in tests samples

Most likely, you don't want to expose IDs of your projects or users recording event
samples for tests. Neither do I. For that purpose, there's a script that simplifies
this. Create an `obfuscate.yaml` in the repo root with the following content:

```yaml
- from: Foo
  into: Bar
```

And then run `poetry run python obfuscate.py`.

It will replace all `Foo` occurrences in samples with `Bar`.

1. https://www.workast.com/help/article/how-to-find-a-slack-user-id/
2. `az devops user list | jq ".items[].user | [.displayName, .mailAddress]"`
