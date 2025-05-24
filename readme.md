# Jota - Bakend
Documentação de como rodar o projeto.

## Requirementos:
- Ter python3.13 instalado

## Passo a Passo
- `$ python3.13 install -m pip install virtualenv`
- `$ python3.13 install -m venv venv`
- `$ source venv/bin/activate`
- `$ python install -r src/requirements.txt`
- `$ cp src/.env.sample src/.env`
- Preencha os dados do banco de dados
- Use o seguinte comando para gerar a variavel "SECRET_KEY":
  - `$ make generate_secretkey`
- Para inciar o projeto:
  - Pela primeira vez: `$ make build` 
  - Nas demais `$ make up`
- Para pausar o projeto:  `$ make stop`
- Para ver os logs da api: `$ make log_api`
- Para ver os logs da fila: `$ make log_queue`
- Para criar superusuário: `$ make createsuperuser`
  
## 