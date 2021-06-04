# actions-slack-notification

actionsで使用するslack通知

## Contents

- [actions-slack-notification](#actions-slack-notification)
  - [Contents](#contents)
  - [Environment](#environment)
  - [Inputs](#inputs)

## Environment

| Key                | Overview                      |
| :----------------- | :---------------------------- |
| SLACK_KEY          | slack app api key             |
| NOTIFICATION_DEBUG | print payload if is not empty |

## Inputs

| Key         | Overview                                                                                                            |
| :---------- | :------------------------------------------------------------------------------------------------------------------ |
| channel     | slack channel id                                                                                                    |
| color       | attachments slack color (default: good)                                                                             |
| title       | slack title field                                                                                                   |
| message     | slack text field                                                                                                    |
| mention     | Mentions a slack message. If there is more than one, please specify them separated by commas. (default: <!channel>) |
| author_icon | author icon url (default: github.event.sender.avatar_url)                                                           |
| fields      | attachments fields on array object string (e.g. '[{"title": "test", "value": "test value"}]')                       |
