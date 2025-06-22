import asyncio
import os
import aiomysql
from dotenv import load_dotenv


class MySQL:
  def __init__(self):
    self.host = None
    self.db = None
    self.user = None
    self.password = None
    self.port = None
    self.pool = None
    load_dotenv()

  async def start(self):
    """Cria e retorna uma nova conexão."""
    self.host = (os.getenv("DB_HOST"))
    self.port = int(os.getenv("DB_PORT"))
    self.db = (os.getenv("DB"))
    self.user = (os.getenv("DB_USER"))
    self.password = (os.getenv("DB_PASS"))

    self.pool = await aiomysql.create_pool(
      host=self.host,
      port=self.port,
      user=self.user,
      password=self.password,
      db=self.db
    )

    success_conn = False
    iterate_conn = 0

    while not success_conn and iterate_conn < 3:
      try:
        print("Connection established!")
        success_conn = True
        return self.pool
      except aiomysql.Error as error:
        print(f"An Error! {error}")
        print(f"Iterate {iterate_conn + 1}")
        iterate_conn += 1

      if iterate_conn == 2:
        print("An error occurred in all iterations")
        await self.close()
        return None

  async def execute(self, query="", value=""):
    """Executa uma query e retorna o resultado."""
    if self.pool:
      success_conn = False
      iterate_conn = 0

      while not success_conn and iterate_conn < 3:
        try:
          async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
              await cur.execute(query, value)
              if query.upper().find("INSERT") != -1 or query.upper().find("UPDATE") != -1:
                await conn.commit()
                await cur.fetchall()
                return cur.rowcount
              success_conn = True
              return await cur.fetchall()
        except aiomysql.Error as error:
          print(f"An Error! {error}")
          print(f"Iterate {iterate_conn + 1}")
          iterate_conn += 1

          print("Attemp starting connection with server!")
          await self.start()

        if iterate_conn == 2:
          print("An error occurred in all iterations")
          await self.close()
          return None
    return None

  async def close(self):
    """Encerra todos os pools de conexão."""
    if self.pool:
      try:
        self.pool.close()
        await self.pool.wait_closed()
        self.pool = None
        print("Connection closed!")
        return True
      except aiomysql.Error as error:
        print(f"An Error! {error}")
        return None
      finally:
        self.pool = None
    return None

  def __del__(self):
    if self.pool:
      self.pool = None
      print("A pool estava aberta e seu encerramento foi forçado.")

