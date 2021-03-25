import requests
import os
import json
import sys


class SlackNotify:

    def __init__(self) -> None:
        self._variables_from_env_variables()

    def _variables_from_env_variables(self):
        self._TOKEN = os.getenv('SLACK_KEY', '')
        self._CHANNEL = os.getenv('SLACK_CHANNEL_ID', '')
        self._GITHUB_ACTOR = os.getenv('GITHUB_ACTOR', '')
        color = ''
        slack_color = os.getenv('SLACK_COLOR')
        if slack_color == 'success':
            color = 'good'
        elif slack_color == 'cancelled':
            color = '#808080'
        elif slack_color == 'failure':
            color = 'danger'
        else:
            color = os.getenv('SLACK_COLOR', 'good')
        self._COLOR = color
        self._SLACK_TITLE = os.getenv('SLACK_TITLE')
        self._SLACK_MESSAGE = os.getenv('SLACK_MESSAGE')

    def _get_field_of_title(self):
        return {
            'title': self._SLACK_TITLE,
            'value': self._SLACK_MESSAGE,
            'short': False
        }

    def _get_field_of_ref(self):
        return {
            'title': 'Ref',
            'value': os.getenv('GITHUB_REF'),
            'short': True
        }

    def _get_field_of_event(self):
        return {
            'title': 'event',
            'value': os.getenv('GITHUB_EVENT_NAME'),
            'short': True

        }

    def _get_field_of_action_url(self):
        return {
            'title': 'Actions URL',
            'value': '<https://github.com/'+os.getenv('GITHUB_REPOSITORY', '')+'/commit/'+os.getenv("GITHUB_SHA", '')+'/checks|'+os.getenv("GITHUB_WORKFLOW", '')+'>',
            'short': True
        }

    def _get_field_of_commit(self):
        long_sha = os.getenv("GITHUB_SHA", '')
        commit_sha = long_sha[0:6]
        return {
            'title': 'Commit',
            'value': "<https://github.com/" + os.getenv("GITHUB_REPOSITORY", '') + "/commit/" + os.getenv("GITHUB_SHA", '') + "|" + commit_sha + ">",
            'short': True
        }

    def _get_minimal_fields(self, minimal):
        required_fields = minimal.split(',')
        main_fields = []
        for required_field in required_fields:
            required_field_lower = required_field.lower()
            if required_field_lower == 'ref':
                main_fields.append(self._get_field_of_ref())
            elif required_field_lower == 'envet':
                main_fields.append(self._get_field_of_event())
            elif required_field_lower == 'actions url':
                main_fields.append(self._get_field_of_action_url())
            elif required_field_lower == 'commit':
                main_fields.append(self._get_field_of_commit())
        main_fields.append(self._get_field_of_title())
        return main_fields

    def _get_fields(self):
        fields = []
        minimal = os.getenv('MSG_MINIMAL')
        if minimal == None:
            minimal = ''

        if minimal == 'true':
            fields.append(self._get_field_of_title())
        elif minimal != '':
            fields.extend(self._get_minimal_fields(minimal))
        else:
            fields.append(self._get_minimal_fields(
                'ref,event,actions url,commit'))
        return fields

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
            attachments = [{
                "title": "Slack通知",
                "text": '',
                'color': self._COLOR,
                'author_name': self._GITHUB_ACTOR,
                'author_link': f'https://github.com/{self._GITHUB_ACTOR}',
                'author_icon': f'https://github.com/{self._GITHUB_ACTOR}',
                'footer': '<https://github.com/nozomi-nishinohara/actions-slack-notification|Powered By nozomi-nishinohara Github Actions Library>',
                'fields': self._get_fields()
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
                sys.exit(0)

