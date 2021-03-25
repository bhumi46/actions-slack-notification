from slack import SlackNotify
import os


def main():
    slack = SlackNotify()
    slack.send_message()


if __name__ == '__main__':
    main()
