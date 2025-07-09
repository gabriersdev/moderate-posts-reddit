# Moderate Posts Reddit

É um bot que aprova posts no reddit de um servidor, de acordo com as solicitações de moderação registradas no banco de dados.  
Todas as solicitações que têm o status 2 são tratadas. E os posts que entraram na fila de moderação até a data e hora do início da solicitação são moderados.

Explicando:
- O post 123 entrou na fila de moderação às 10:00
- O post 456 entrou na fila de moderação às 10:10
- As 10:15 foi feita uma solicitação de moderação
- O post 789 entrou na fila de moderação às 10:16
- Quando o bot rodar o script, apenas os posts 123 e 456 serão moderados.

As ações de moderação que o bot pode fazer são duas:
- Aprovar o post (apenas POSTS) no Reddit
- Reprovar (remover) o post do Reddit

Após a execução das ações, é registrado no banco de dados.

## Technologies Used

- Python
- Async Praw, Pendulum, Mysql2, Requests
- Desenvolvido no PyCharm
