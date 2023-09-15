# Azure DevOps code review 🤝 Slack

Do you

- 🚀 collaboratively work on code in Azure DevOps,
- 🧑‍💻 use Slack for work related communication,
- 🥵 hate spammy notifications in your mailbox?

Well, then you might like an idea to receive notifications from pull requests into
Slack.

It requires a bit of setup, but then all (configured) team members will be able to get
informed in direct messages:

1. **When a pull request is created, and they are assigned as reviewers**
<img width="663" alt="image" src="https://github.com/fbjorn/azure-devops-slack/assets/9670990/70736266-76aa-40f9-a48e-47a7ef7afeaa">

2. **When their pull request is approved**
<img width="653" alt="image" src="https://github.com/fbjorn/azure-devops-slack/assets/9670990/4003405c-6ac7-455f-bda4-41e408affd73">

3. **When someone leaves a comment on their PRs**
<img width="654" alt="image" src="https://github.com/fbjorn/azure-devops-slack/assets/9670990/f4d7f288-bc5e-4460-b866-14e11820d71f">

4. When someone replies to their comment _[IN PROGRESS]_

# Setup

First of all, I think that all this information is sensitive since you're working in
private repositories. Thus, your data should not be transferred to 3rd parties. That's
why I didn't create a shared Slack application. It's up to you to host your own
notification webhook, because each DevOps event gets transferred through it.

## 1. Collect information about users

Slack doesn't know anything about your Azure users and vice versa. So you will have to
create a mapping for them manually. Moreover, not everyone in your team might want to
opt in for such notifications, so it's still a wise idea to compose this list by hands.

If you have an Azure CLI installed (and `jq` as a bonus), you can use this snippet:

```shell
az devops user list | jq ".items[].user | [.displayName, .mailAddress]"
```

Otherwise, go to `Organization settings` -> `Users` (or ask your admin to gather this
information) and save a list of emails and usernames.

Follow this article to
[find user IDs in Slack](https://www.workast.com/help/article/how-to-find-a-slack-user-id/).

After that, create a `users.yaml` in the repository root with the following structure:

```yaml
users:
  - name_filter: Jane Doe
    emails: ["jane.doe@example.com"]
    slack_id: ABCDFOOBAR
```

Name filter is used to match a user if it's not matched by the email (there are some
cases when users change their emails but not the display name). It can be just a surname
or a name as well if it's kinda unique.

## 2. Create a Slack application

1. Go to Slack application management and [create a new app](https://api.slack.com/apps)
2. Choose "From an app manifest", select your workspace and copy the content from
   [slack-app.manifest.json](./slack-app.manifest.json). Pick another name based on your
   preferences. The important there is the permission to `chat:write`, otherwise the app
   won't be able to post messages to DMs.
3. Go to "OAuth & Permissions" and save the value of `Bot User OAuth Token`

## 3. Deploy the webhook

There are few options for how you can deploy it. Feel free to suggest more. If you
decide to deploy it as a Google Cloud function, then you have to create a `.env` file
with the settings. If you want to deploy it as a Docker container, then it's up to you
how to pass the configuration inside. Anyway, the service is configured via the
environment variables.

```dotenv
# [REQUIRED]
# Slack application token from the previous step
SLACK_BOT_TOKEN=xoxb-123-foobar

# [REQUIRED for Docker, OPTIONAL for cloud functions]
# A list of users that will receive the messages from the bot.
# If you deploy as a Cloud Function, then no need to add it - the list will be
# taken automatically from `users.yaml`. If you deploy as a docker container,
# run `poetry run invoke convert-users`, this is the value you shoud set.
USERS='[ <array of users in a JSON format> ]'

# [OPTIONAL]
# An HTTP header that you might want to configure later when setting up
# an event subscription in Azure DevOps. The value is up to you
API_KEY=foo-bar

# [OPTIONAL]
# Set this if you want to log the DevOps events and additional debug information
DEBUG=1
```

### Google Cloud Functions

```bash
poetry run invoke deploy-cloud-function --help
```

### Anywhere as a Docker image

_[SOON]_

## 4. Set up triggers in Azure DevOps

Finally, go to Project Settings in Azure DevOps:
`https://dev.azure.com/<ORG>/<PROJ>/_settings/`.

Open "Service hooks" section and click a plus icon for adding:

- `Web hooks / Pull request commented on` (v2.0)
- `Web hooks / Pull request created` (v1.0)
- `Web hooks / Pull request updated` (v1.0)

For each of them, enter the URL of the service that you deployed on a previous step.

Optionally, add an HTTP header `X-API-KEY:<key>` if you configured it in the settings.

Save an enjoy being up-to-date 🎉

# Installation and local development

```shell
# install project dependencies
poetry install

# set up pre-commit hooks (required if you want to make PRs)
pre-commit install

# get information about useful commands
poetry run invoke --help

# run unit tests
poetry run pytest

# update unit test snapshots
poetry run pytest --snapshot-update

# export Poetry dependencies to Cloud Functions -acceptable format
poetry export > requirements.txt
```

## Recording Azure DevOps events for unit tests

```shell
# 1. Run ngrok or other tool that exposes a local port to the internet
ngrok http 8080

# 2. Edit corresponding service hook in Azure DevOps and set the new URL there

# 3. Run the following command and perform an action you'd like to record
#    (for example merging a pull request)
poetry run invoke record-test-sample foo
```

This will create a `foo.json` under [tests/samples](./tests/samples) and you can use
this file for testing the parser logic.

Most likely, you don't want to expose IDs of your projects or users recording event
samples for tests. Neither do I. For that purpose, there's a script that simplifies
this. Create an `obfuscate.yaml` in the repo root with the following content:

```yaml
- from: Foo
  into: Bar
```

And then run:

```shell
poetry run invoke obfuscate-tests
```

It will replace all `Foo` occurrences in samples with `Bar`.

# Contribution

Every PR and suggestion is welcomed. My team is using this project on daily basis, but
your Azure setup might be different resulting in potential bugs. Don't hesitate to
report issues, or record your event sample and add it to test cases.

I believe this project is a great example of a service to deploy as a stateless cloud
function, but I only tested it with Google. If you have successfully deployed it to
another cloud provider, please let me know, so we can update the instructions.
