import json
import random

BARKS = [
  'woof!',
  'arf!',
  'grr!',
  '*head tilt*',
]

class Margo(object):
  slack_api = None

  def __init__(self, slack_api):
    self.slack_api = slack_api

  def on_message(self, ws, message_str):
    message = json.loads(message_str)
    if message['type'] == 'message':
      text = message['text']
      if 'Margo, Bark!' in text:
        self.bark_at_user(message['channel'], message['user'])

  def on_error(self, ws, message):
    print message

  def on_close(self, ws):
    message = "Closed"

  """
    Posts a random 'bark' message to a given user

    param:
      channel (str): Channel to bark in
      user_id (str): User to bark at
  """
  def bark_at_user(self, channel, user_id):
    user = self.slack_api.get_user(user_id)
    user_name = user['name']

    message = '@{} {}'.format(user_name, random.choice(BARKS))

    self.slack_api.post_message(channel, message)
