# actions-slack-notification

actionsで使用するslack通知

## Contents

- [actions-slack-notification](#actions-slack-notification)
  - [Contents](#contents)
  - [Inputs](#inputs)


## Inputs

| Key         | Overview                                                                                                            |
| :---------- | :------------------------------------------------------------------------------------------------------------------ |
| key         | slack app oauth token                                                                                               |
| channel     | slack channel id                                                                                                    |
| color       | attachments slack color (default: good)                                                                             |
| title       | slack title field                                                                                                   |
| message     | slack text field                                                                                                    |
| mention     | Mentions a slack message. If there is more than one, please specify them separated by commas. (default: <!channel>) |
| author_icon | author icon url (default: github.event.sender.avatar_url)                                                           |
| fields      | attachments fields on array object string (e.g. '[{"title": "test", "value": "test value"}]')                       |
| debug       | print payload if is 'Y'                                                                                             |
