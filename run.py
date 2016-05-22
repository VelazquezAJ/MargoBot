from library.slackapi import SlackApi
from margobot.margo import Margo

def main():
  api = SlackApi()

  margo = Margo(api)

  ws = api.start_connection(margo)
  ws.run_forever()

if __name__ == '__main__':
  main()
