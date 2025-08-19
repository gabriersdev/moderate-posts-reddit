import asyncio
import os
import pendulum

from dotenv import load_dotenv
from database.MySQL import MySQL
from reddit.RequestReddit import RedditRequest, approve, repprove
from verifier.RedditVerifier import verify

load_dotenv()

ATM = os.getenv("ATM")
TIMEZONE = "America/Sao_Paulo"
NOW = pendulum.now(tz=TIMEZONE)
SLUG_SCRIPT = "MPR"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
STATUS_REQUEST_PENDING = 2
STATUS_POSTS_NOT_MODERATED = 0
STATUS_POSTS_MODERATED = 3
STATUS_IGNORE_ACTION = 4


def register(message):
    print(f"[{SLUG_SCRIPT}] {NOW.format("YYYY-MM-DD HH:mm:ss")} - {message}")


async def verify_requests():
    register("Verificando solicitações de moderação")

    mysql = MySQL()
    await mysql.start()
    reddit = RedditRequest()

    request_with_status_2 = await mysql.execute("SELECT `id`, `code`, `datetime_create`, `action_type` FROM `actions_moderations` WHERE `status` = %s ORDER BY `datetime_create` ASC", [STATUS_REQUEST_PENDING])

    # Percorre as solicitações do banco de dados com status
    if not request_with_status_2:
        register("Nenhuma solicitação com status 2 retornada pelo banco de dados")

    for r in request_with_status_2:
        print(f"Iniciando execução da solicitação com ID {r[0]}")
        datetime_init_request = pendulum.instance(r[2], tz="America/Sao_Paulo")

        request_id = r[0]
        action_type = r[3]

        # Busca os posts pendentes de moderação que entraram na fila até o horário de início da solicitação
        posts_pending_moderation = await mysql.execute("SELECT `reddit_id`, `post_title`, `post_author_name` FROM `posts_unmoderated_reddit` WHERE `datetime_register` <= TIMESTAMP(%s) AND `status` = %s ORDER BY `datetime_register`", [datetime_init_request.format("YYYY-MM-DD HH:mm:ss"), STATUS_POSTS_NOT_MODERATED])

        if not posts_pending_moderation:
            register("A query SELECT ao banco de dados não retornou nada.")
            set_request_status = await mysql.execute("UPDATE `actions_moderations` SET `status` = %s WHERE `status` = %s AND `id` = %s", [STATUS_IGNORE_ACTION, STATUS_REQUEST_PENDING, request_id])
            register(f"Status da solicitação com ID {request_id} alterado para {STATUS_IGNORE_ACTION} pois nenhum post retornou do banco de dados para que algo fosse feito. Retorno da ação de alteração de status: {set_request_status}")

            continue

        for ppm in posts_pending_moderation:
            post_id = ppm[0]

            reddit.start()
            # Obtém instância do post
            post = await reddit.search(post_id)

            if not post.fullname.startswith('t3_'):
                return

            # Verifica se ainda não foi moderado
            # Se ação for 1 - aprova se 2 - remove
            if not verify(post):
                if int(action_type) == 1:
                    await approve(post)
                    register(f"O post {post} foi aprovado")
                elif int(action_type) == 2:
                    await repprove(post)
                    register(f"[MPR] O post {post} foi removido")
                else:
                    register(f"Action {action_type} não mapeado")
                    exit(1)

                await reddit.close()

        if not posts_pending_moderation:
            register("Nenhum post pendente de moderação existente. Portanto a solicitação foi concluída sem nada ter sido feito.")

        await mysql.execute("UPDATE `actions_moderations` SET `status` = %s WHERE `id` = %s", [STATUS_POSTS_MODERATED, request_id])
        await mysql.close()


if __name__ == "__main__":
    register(f"Iniciando verificações de requisições para moderar posts.")
    asyncio.run(verify_requests())
