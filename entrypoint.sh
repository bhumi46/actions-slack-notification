#!/usr/bin/env bash

export GITHUB_BRANCH=${GITHUB_REF##*heads/}
export SLACK_TITLE=${SLACK_TITLE:-"Message"}

if [ -f "${GITHUB_EVENT_PATH}" ]; then
	export COMMIT_MESSAGE=$(cat "$GITHUB_EVENT_PATH" | jq -r '.commits[-1].message')
fi

export GITHUB_ACTOR=${SLACK_MSG_AUTHOR:-"$GITHUB_ACTOR"}

if [[ -z "$SLACK_MESSAGE" ]]; then
	export SLACK_MESSAGE="$COMMIT_MESSAGE"
fi

exec "$@"