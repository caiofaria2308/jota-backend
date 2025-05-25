# 🧪 Testes Automatizados - Jota Backend

[![Tests](https://github.com/seu-usuario/jota-backend/workflows/Tests%20and%20Coverage/badge.svg)](https://github.com/seu-usuario/jota-backend/actions)
[![Coverage](https://codecov.io/gh/seu-usuario/jota-backend/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/jota-backend)

## 🚀 Quick Start

```bash
# Setup inicial
./run_tests.sh setup

# Executar testes rápidos
./run_tests.sh quick

# Executar todos os testes
./run_tests.sh all

# Testes com cobertura
./run_tests.sh coverage
```

## 📊 Status dos Testes

| Categoria | Testes | Status | Cobertura |
|-----------|--------|---------|-----------|
| Account | 21 | ✅ 19/21 | ~90% |
| News | 60 | ✅ 47/60 | ~85% |
| **Total** | **81** | ✅ **66/81** | **~87%** |

## 🏗 Estrutura

```
src/
├── conftest.py                 # Fixtures globais
├── pytest.ini                 # Configuração pytest
├── apps/
│   ├── account/tests/          # 21 testes
│   │   ├── test_auth.py        # Autenticação JWT (6 testes)
│   │   ├── test_user.py        # Modelo User (9 testes)
│   │   └── test_subscription_plan.py  # Planos (6 testes)
│   └── news/tests/             # 60 testes
│       ├── test_models.py      # Modelos (11 testes)
│       ├── test_api.py         # APIs REST (14 testes)
│       ├── test_serializers.py # Serializers (9 testes)
│       ├── test_integration.py # Integração (5 testes)
│       ├── test_performance.py # Performance (4 testes)
│       └── test_validations.py # Validações (17 testes)
```

## 🐳 Docker

### Setup Automatizado
```bash
# Configurar ambiente completo
make test_docker_setup

# Executar todos os testes
make test_docker_run

# Testes com cobertura
make test_docker_coverage
```

### Comandos Manuais
```bash
# Iniciar banco de teste
docker compose -f docker-compose.test.yml up -d test-db

# Executar testes específicos
docker compose -f docker-compose.test.yml run --rm test pytest apps/account/tests/ -v

# Executar teste individual
docker compose -f docker-compose.test.yml run --rm test pytest apps/account/tests/test_user.py::TestUser::test_create_user_reader -v
```

## 💻 Local

### Pré-requisitos
```bash
# Instalar dependências
pip install -r src/requirements.txt

# Configurar banco local (PostgreSQL)
createdb jota_test
```

### Comandos
```bash
cd src

# Todos os testes
python -m pytest

# Testes específicos
python -m pytest apps/account/tests/

# Com cobertura
python -m pytest --cov=apps --cov-report=html
```

## 📈 Cobertura

### Executar com Relatório
```bash
./run_tests.sh coverage
```

### Visualizar HTML
```bash
# Após executar testes com cobertura
open src/htmlcov/index.html
```

### Metas de Cobertura

| Módulo | Meta | Atual | Status |
|--------|------|-------|---------|
| Models | 95% | ~90% | ⚠️ |
| Views/APIs | 85% | ~80% | ⚠️ |
| Serializers | 90% | ~85% | ⚠️ |
| Utils | 80% | ~90% | ✅ |

## 🔧 Configuração

### Arquivos Importantes

- **`pytest.ini`**: Configuração principal do pytest
- **`conftest.py`**: Fixtures e configurações globais
- **`test_settings.py`**: Configurações Django para testes
- **`.env.test`**: Variáveis de ambiente para testes
- **`docker-compose.test.yml`**: Ambiente Docker para testes

### Marcadores (Markers)

```python
@pytest.mark.django_db      # Acesso ao banco
@pytest.mark.unit          # Teste unitário
@pytest.mark.integration   # Teste de integração
@pytest.mark.api           # Teste de API
@pytest.mark.slow          # Teste demorado
```

## 🚨 Testes Falhando

### Problemas Conhecidos (15 falhas)

1. **JWT Refresh Token** (1 falha)
   - Configuração de Outstanding Token

2. **Serializers** (8 falhas)
   - Validação de campo `author`
   - Permissões de criação/edição

3. **Modelos** (2 falhas)
   - Soft delete de subscription plans
   - Serialização de IDs

4. **Performance** (2 falhas)
   - Otimização de queries
   - Bulk operations

5. **Integração** (2 falhas)
   - Fluxos completos de CRUD

### Como Corrigir

```bash
# Executar teste específico com debug
docker compose -f docker-compose.test.yml run --rm test pytest apps/news/tests/test_serializers.py::TestNewSerializer::test_deserialize_valid_data_writer -vvv --tb=long

# Verificar configuração de JWT
docker compose -f docker-compose.test.yml run --rm test pytest apps/account/tests/test_auth.py::TestJWTAuthentication::test_refresh_token_valid -s
```

## 🎯 Performance

### Métricas Atuais
- **Tempo total**: ~1.2s
- **Tempo por teste**: ~15ms
- **Setup**: ~200ms
- **Teardown**: ~100ms

### Otimizações
- ✅ Banco em memória para testes
- ✅ Migrações desabilitadas
- ✅ Logging reduzido
- ✅ Password hashing simplificado
- ⚠️ Fixtures compartilhadas (em progresso)

## 🔄 CI/CD

### GitHub Actions

O pipeline de CI/CD inclui:

```yaml
# .github/workflows/tests.yml
jobs:
  test:           # Testes principais
  lint:           # Linting (black, flake8, isort)
  docker-test:    # Testes em Docker
```

### Triggers
- Push para `main` ou `develop`
- Pull Requests
- Commits com tag de versão

### Badges
- Status dos testes
- Cobertura de código
- Qualidade do código

## 🛠 Desenvolvimento

### Adicionando Novos Testes

1. **Seguir convenções**:
   ```python
   # apps/exemplo/tests/test_funcionalidade.py
   @pytest.mark.django_db
   class TestFuncionalidade:
       def test_cenario_positivo(self, fixture_necessaria):
           # Arrange
           # Act
           # Assert
   ```

2. **Usar fixtures existentes**:
   ```python
   def test_com_usuario(self, user_writer):
       assert user_writer.user_type == "writer"
   ```

3. **Documentar cenários**:
   ```python
   def test_criar_noticia_como_writer(self, user_writer):
       """Testa que um writer pode criar notícias"""
   ```

### Fixtures Disponíveis

```python
# Usuários
user_reader     # Usuário leitor
user_writer     # Usuário escritor
admin_user      # Usuário admin

# Planos
free_plan       # Plano gratuito
pro_plan        # Plano profissional

# Notícias
published_news  # Notícia publicada
draft_news      # Notícia em rascunho

# Utilidades
api_client      # Cliente API autenticado
sample_image    # Imagem para upload
```

## 📚 Recursos

### Documentação
- [pytest-django](https://pytest-django.readthedocs.io/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Docker Compose](https://docs.docker.com/compose/)

### Comandos Úteis

```bash
# Listar todos os testes
pytest --collect-only

# Executar com filtro
pytest -k "test_user"

# Parar no primeiro erro
pytest -x

# Mostrar prints
pytest -s

# Debug mode
pytest --pdb
```

## 🤝 Contribuição

1. Adicione testes para novas funcionalidades
2. Mantenha cobertura acima de 80%
3. Use fixtures quando possível
4. Documente cenários complexos
5. Execute testes antes de commit

```bash
# Antes de fazer commit
./run_tests.sh quick
```

---

**Última atualização**: 25 de Maio, 2025
**Versão dos testes**: 1.0.0
**Pytest**: 8.3.5
**Django**: 5.2.1
