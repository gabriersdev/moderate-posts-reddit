import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Webhook:
  def __init__(self):
    self.webhook_url = os.getenv("WEBHOOK_URL")

  def send(self, payload):
    if not self.webhook_url:
      print("URL do webhook não definida")
      exit(1)

    # Adiciona props ao dict
    # Flag 4096 = Supress notifications
    # See: https://discohook.org
    payload["flags"] = 4096
    payload["avatar_url"] = "https://eskimozin.github.io/reddit-mod-queue/reddit.jpg"

    print(payload)

    return requests.post(self.webhook_url, json=payload)
