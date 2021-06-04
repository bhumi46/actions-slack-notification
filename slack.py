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
        print(os.getenv('GITHUB_EVENT_PATH'))
        self._event_path = {
            'commits': [{
                'message': 'test'
            }]
        }
        self._TOKEN = self._get_actions_input('key')
        self._CHANNEL = self._get_actions_input('channel')
        self._GITHUB_ACTOR = os.getenv('GITHUB_ACTOR', '')
        self._COLOR = self._get_actions_input('color')
        self._SLACK_TITLE = self._get_actions_input('title')
        self._SLACK_MESSAGE = self._get_actions_input('message')

    def _get_field_of_input_message(self):
        return {
            'title': 'Message',
            'value': self._SLACK_MESSAGE
        }

    def _get_field_of_action_url(self):
        return {
            'title': 'Actions URL',
            'value': '<https://github.com/'+os.getenv('GITHUB_REPOSITORY', '')+'/commit/'+os.getenv("GITHUB_SHA", '')+'/checks|'+os.getenv("GITHUB_WORKFLOW", '')+'>',
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
        if type(fields) in list:
            return fields
        else:
            return [fields]

    def send_message(self):
        exit_flg = False
        if self._TOKEN == '':
            sys.stderr.writelines('No setting api key')
            exit_flg = True
        if self._CHANNEL == '':
            sys.stderr.writelines('No setting slack channel')
            exit_flg = True
        if exit_flg:
            sys.exit(1)
        if self._TOKEN != '' and self._CHANNEL:
            author_icon = self._get_actions_input('author_icon')
            mention = self._get_actions_input('mention')
            mentions = mention.split(',')
            attachments = [{
                "title": self._SLACK_TITLE,
                "text": '\n'.join(mentions),
                'color': self._COLOR,
                'author_name': self._GITHUB_ACTOR,
                'author_link': f'https://github.com/{self._GITHUB_ACTOR}',
                'author_icon': author_icon,
                'footer': '<https://github.com/nozomi-nishinohara/actions-slack-notification|Powered By nozomi-nishinohara Github Actions Library>',
                'fields': [
                    self._get_field_of_input_message(),
                    self._get_field_of_commit_message(),
                    self._get_field_of_commit_url(),
                    self._get_field_of_action_url(),
                ].extend(self._get_field_of_input_fields())
            }]
            payload = {
                'channel': self._CHANNEL,
                'attachments': attachments,
            }
            r = requests.post('https://slack.com/api/chat.postMessage', json.dumps(
                payload), headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {self._TOKEN}'})
            res = r.json()
            if res['ok'] == True:
                print('Slack notification ok')
                sys.exit(0)
            else:
                sys.stderr.writelines('Slack notification ng')
                print(res)
                sys.exit(1)
