import os
import requests
from websocket import WebSocketApp

SUPPORTED_METHODS = [
  'get',
  'post',
  'put',
  'delete',
]

class SlackApi(object):
  bearer = None

  def __init__(self):
    self.bearer = os.environ['SLACK_TOKEN']

  """
    Make an HTTP Request to the Slack API
    params:
      method (str): HTTP Method to call
      endpoint (str): Endpoint on the Slack API to call
      data (dict): A dictionary of any information to submit with the request

    return:
      requests.Response object
  """
  def _request(self, method, endpoint, headers={}, data={}):
    data['token'] = self.bearer
    if method not in SUPPORTED_METHODS:
      raise Exception('Called with unsupported method: {}'.format(method))

    request = getattr(requests, method)

    response = request('https://slack.com/api/{}'.format(endpoint),
                       headers=headers, data=data)

    self._verify_response(response)

    return response

  """
    Verify response from the Slack API was successful
    params:
      response (request.Response): The response object from a call to the slack
                                   API

    return:
      bool: True if response was successful
  """
  def _verify_response(self, response):
    if response.status_code >= 400:
      raise Exception('Slack API call failed with status code: {}'.format(
                      response.status_code))

    response_data = response.json()
    if not response_data['ok']:
      raise Exception('Response failed: {}'.format(response_data))

    return True

  """
    Ensure the connection to the Slack API is working
  """
  def test(self):
    headers = {
      'Authentication': 'bearer {}'.format(self.bearer),
    }
    response = self._request('get', 'api.test', headers=headers)
    return response.json()

  """
    Return user information from slack

    params:
      user (str): Slack user ID to get information on

    return:
      dict: User information from slack
  """
  def get_user(self, user):
    data = {
      'user': user
    }
    response = self._request('post', 'users.info', data=data)
    response_data = response.json()
    return response_data['user']

  """
    Post a message to a slack channel

    params:
      channel (str): Channel ID to post message to
      text (str): Message to post to channel
  """
  def post_message(self, channel, message):
    data = {
      'channel': channel,
      'text': message,
      'as_user': True,
    }
    response = self._request('post', 'chat.postMessage', data=data)
    print response.text
    return True

  """
    Start a RTM connection to slack

    params:
      listener (obj): An object to receive messages from the websocket
  """
  def start_connection(self, listener):
    response = self._request('post', 'rtm.start')

    response_data = response.json()

    ws = WebSocketApp(response_data['url'],
      on_message=listener.on_message,
      on_error=listener.on_error,
      on_close=listener.on_close
    )

    return ws
