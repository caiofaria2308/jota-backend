# Jota - Backend
API backend para o projeto Jota desenvolvida em Django.

## 📋 Pré-requisitos

- Python 3.13
- Docker e Docker Compose (opcional)
- Make

## 🚀 Configuração do Ambiente

### 1. Configuração do Ambiente Virtual

```bash
# Instalar virtualenv
python3.13 -m pip install virtualenv

# Criar ambiente virtual
python3.13 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate
```

### 2. Instalação das Dependências

```bash
# Instalar dependências do projeto
pip install -r src/requirements.txt
```

### 3. Configuração do Banco de Dados

```bash
# Copiar arquivo de configuração
cp src/.env.sample src/.env

# Editar o arquivo .env com suas configurações de banco de dados
# Gerar SECRET_KEY
make generate_secretkey
```

## 🛠️ Comandos Disponíveis

### Inicialização do Projeto

```bash
# Primeira execução (configura banco de dados e dependências)
make init

# Execuções subsequentes
make up
```

### Gerenciamento do Projeto

```bash
# Pausar o projeto
make stop

# Visualizar logs da API
make log_api

# Visualizar logs da fila
make log_queue

# Criar superusuário
make createsuperuser
```

## 📁 Estrutura do Projeto

```
src/
├── apps/
│   ├── account/     # Gerenciamento de usuários e autenticação
│   └── news/        # Sistema de notícias
├── setting/         # Configurações do Django
├── manage.py        # Gerenciador do Django
└── requirements.txt # Dependências do projeto
```

## 🐳 Docker

O projeto inclui configurações para Docker:

- `docker-compose.yml` - Ambiente de produção
- `docker-compose.dev.yml` - Ambiente de desenvolvimento

## 📝 Notas Importantes

- Certifique-se de preencher corretamente as variáveis de ambiente no arquivo `.env`
- Para desenvolvimento, use sempre o ambiente virtual ativado
- Os comandos Make facilitam o gerenciamento do projeto

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
