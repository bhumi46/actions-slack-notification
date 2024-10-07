# Actions Slack Notification

This GitHub Action sends notifications to individual Slack users based on GitHub events. It can be customized with various input parameters to suit your notification needs.

## Features

- Sends notifications directly to specified Slack users.
- Customizable message, title, and appearance.
- Supports mentions and additional fields.

## Inputs

The following inputs are required and optional for the action:

| Input          | Description                                                  | Required | Default                              |
|----------------|--------------------------------------------------------------|----------|--------------------------------------|
| `key`          | Slack app OAuth token                                        | Yes      |                                      |
| `color`        | Attachments Slack color (default: `good`)                   | No       | `good`                               |
| `title`        | Slack title field                                           | No       | `Actions event notification`         |
| `message`      | Slack text field                                           | No       | `Actions event`                      |
| `author_icon`  | Author icon URL (default: `github.event.sender.avatar_url`) | No       | `${{ github.event.sender.avatar_url }}` |
| `fields`       | Attachments fields as an array object string (e.g. `"[{"title": "test", "value": "test value"}]"`) | No       |                                      |
| `debug`        | Print payload if set to `Y`                                 | No       |                                      |

## User Mapping

To enable notifications to individual Slack users based on their GitHub usernames, you must pass a mapping of usernames to Slack user IDs as a secret. 

### Example User Mapping JSON
```json
{
  "github_username1": "U123456",
  "github_username2": "U234567",
  "github_username3": "U345678"
}
