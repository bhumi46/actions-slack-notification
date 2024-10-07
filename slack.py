import requests
import os
import json
import sys


class SlackNotify:

    def __init__(self) -> None:
        self._variables_from_env_variables()

    def _get_actions_input(self, name: str) -> str:
        return os.getenv(f'INPUT_{name.upper()}')

    def _variables_from_env_variables(self):
        event_json = os.getenv('GITHUB_EVENT_PATH')
        with open(event_json, "rb") as rb:
            self._event_path = json.load(rb)
        self._TOKEN = self._get_actions_input('key')
        self._GITHUB_ACTOR = os.getenv('GITHUB_ACTOR', '')
        self._COLOR = self._get_actions_input('color')
        self._SLACK_TITLE = self._get_actions_input('title')
        self._SLACK_MESSAGE = self._get_actions_input('message')
        self._USER_ID = self._get_slack_user_id()  # Get the Slack user ID based on the GitHub actor

    def _get_slack_user_mapping(self):
        mapping_string = os.getenv('SLACK_USER_MAPPING', '{}')
        return json.loads(mapping_string)  # Parse the JSON string into a dictionary

    def _get_slack_user_id(self):
        user_mapping = self._get_slack_user_mapping()
        return user_mapping.get(self._GITHUB_ACTOR, '')  # Return the corresponding Slack user ID

    def _get_field_of_input_message(self):
        return {
            'title': 'Message',
            'value': self._SLACK_MESSAGE
        }

    def _get_field_of_commit_url(self):
        long_sha = os.getenv("GITHUB_SHA", '')
        commit_sha = long_sha[0:6]
        return {
            'title': 'Commit URL',
            'value': "<https://github.com/" + os.getenv("GITHUB_REPOSITORY", '') + "/commit/" + os.getenv("GITHUB_SHA", '') + "|" + commit_sha + ">",
        }

    def _get_field_of_commit_message(self):
        return {
            'title': 'Commit message',
            'value': self._event_path['commits'][-1]['message']
        }

    def _get_field_of_input_fields(self) -> list:
        str_field = self._get_actions_input('fields')
        if str_field == "":
            return []
        fields: list = json.loads(str_field)
        if type(fields) is list:
            return fields
        else:
            return [fields]

    def send_message(self):
        exit_flg = False
        if self._TOKEN == '':
            sys.stderr.writelines('No setting api key')
            exit_flg = True
        if self._USER_ID == '':
            sys.stderr.writelines('No corresponding Slack user ID for the GitHub actor')
            exit_flg = True
        if exit_flg:
            sys.exit(1)

        if self._TOKEN != '' and self._USER_ID:
            author_icon = self._get_actions_input('author_icon')
            fields = [
                self._get_field_of_input_message(),
                self._get_field_of_commit_message(),
                self._get_field_of_commit_url()
            ]
            fields.extend(self._get_field_of_input_fields())
            attachments = [{
                "title": self._SLACK_TITLE,
                'color': self._COLOR,
                'author_name': self._GITHUB_ACTOR,
                'author_link': f'https://github.com/{self._GITHUB_ACTOR}',
                'author_icon': author_icon,
                'footer': '<https://github.com/mosip/actions-slack-notification|Powered By mosip Github Actions Library>',
                'fields': fields
            }]
            payload = {
                'channel': self._USER_ID,  # Send notification to the user ID
                'attachments': attachments,
            }
            body = json.dumps(payload)
            if self._get_actions_input('debug').upper() != 'Y':
                print(body)
            r = requests.post('https://slack.com/api/chat.postMessage', body, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {self._TOKEN}'})
            res = r.json()
            if res['ok'] == True:
                print('Slack notification ok')
                sys.exit(0)
            else:
                sys.stderr.writelines('Slack notification ng')
                print(res)
                sys.exit(1)
