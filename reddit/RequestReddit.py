import os
import asyncpraw
from dotenv import load_dotenv

from praw.models import Submission, Comment
from praw.models.reddit.comment import CommentModeration
from praw.models.reddit.submission import SubmissionModeration


async def approve(item: Submission | Comment | SubmissionModeration | CommentModeration):
  try:
    if isinstance(item, Submission):
      print(f"Aprovando submission: {item.title}")
    elif isinstance(item, Comment):
      print(f"Aprovando comment: {item.body}")
    await item.mod.approve()
  except Exception as e:
    print(f"Ocorreu um erro ao tentar aprovar o item {item}. Erro: {e}")


async def repprove(item: Submission | Comment | SubmissionModeration | CommentModeration):
  try:
    if isinstance(item, Submission):
      print(f"Reprovando submission: {item.title}")
    elif isinstance(item, Comment):
      print(f"Reprovando comment: {item.body}")
    await item.mod.remove()
  except Exception as e:
    print(f"Ocorreu um erro ao tentar reprovar o item {item}. Erro: {e}")


class RedditRequest:
  def __init__(self):
    self.subreddit_async = None
    self.reddit_async = None
    self.REDDIT_USER_AGENT = None
    self.REDDIT_PASSWORD = None
    self.REDDIT_USERNAME = None
    self.REDDIT_CLIENT_SECRET = None
    self.REDDIT_CLIENT_ID = None
    self.SUBREDDIT_NAME = None
    self.reddit = None
    self.subreddit = None
    load_dotenv()

  def start(self):
    self.REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    self.REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    self.REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
    self.REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
    self.REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    self.SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")

    self.reddit_async = asyncpraw.Reddit(
      client_id=self.REDDIT_CLIENT_ID,
      client_secret=self.REDDIT_CLIENT_SECRET,
      username=self.REDDIT_USERNAME,
      password=self.REDDIT_PASSWORD,
      user_agent=self.REDDIT_USER_AGENT,
    )

  def get_unmoderated_posts(self):
    pass

  async def search(self, ids):
    return await self.reddit_async.submission(id=ids)

  async def close(self):
    await self.reddit_async.close()
    self.reddit_async = None

  def __del__(self):
    if self.reddit_async is not None:
      print("Você precisa fechar a conexão com o Async Praw")
      exit(1)
