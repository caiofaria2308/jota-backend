# Documentação de Testes - Jota Backend

## Visão Geral

Este projeto utiliza **pytest-django** para testes automatizados, fornecendo uma suite completa de testes para todos os componentes do backend Jota.

## Estrutura dos Testes

```
src/
├── conftest.py                    # Fixtures globais
├── pytest.ini                    # Configuração do pytest
├── apps/
│   ├── account/tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py          # Testes de autenticação JWT
│   │   ├── test_subscription_plan.py  # Testes do modelo SubscriptionPlan
│   │   └── test_user.py          # Testes do modelo User
│   └── news/tests/
│       ├── __init__.py
│       ├── test_models.py        # Testes do modelo New
│       ├── test_api.py           # Testes das APIs REST
│       ├── test_serializers.py   # Testes dos serializers
│       ├── test_integration.py   # Testes de integração
│       ├── test_performance.py   # Testes de performance
│       └── test_validations.py   # Testes de validação
```

## Configuração

### Banco de Dados de Teste
Os testes utilizam **SQLite em memória** para máxima velocidade e não dependem do PostgreSQL em produção.

### Configurações Específicas
- **Arquivo**: `src/setting/test_settings.py`
- **Migrations**: Desabilitadas para velocidade
- **Password Hashers**: MD5 (apenas para testes)
- **Logging**: Desabilitado durante testes

## Fixtures Disponíveis

### Fixtures de Usuários
- `user`: Usuário padrão
- `admin_user`: Usuário administrador
- `pro_user`: Usuário com plano Pro
- `free_user`: Usuário com plano Free

### Fixtures de Planos
- `free_plan`: Plano gratuito
- `pro_plan`: Plano profissional

### Fixtures de Notícias
- `news_item`: Notícia individual
- `multiple_news`: Lista de múltiplas notícias
- `news_with_image`: Notícia com imagem

### Fixtures de Utilidades
- `api_client`: Cliente DRF autenticado
- `authenticated_client`: Cliente Django autenticado

## Comandos de Teste

### Executar Todos os Testes
```bash
make test
```

### Testes por Categoria
```bash
# Testes unitários
make test_unit

# Testes de integração
make test_integration

# Testes de API
make test_api

# Testes de autenticação
make test_auth

# Testes de modelos
make test_models

# Testes de performance
make test_performance
```

### Testes por Aplicação
```bash
# Testes da aplicação account
make test_account

# Testes da aplicação news
make test_news
```

### Comandos Específicos
```bash
# Testes com cobertura
make test_coverage

# Testes em modo verboso
make test_verbose

# Testes rápidos (sem migrations)
make test_fast

# Testes com relatório JUnit
make test_junit

# Limpeza do cache de testes
make test_clean
```

## Marcadores (Markers)

Os testes são organizados com marcadores para execução seletiva:

- `@pytest.mark.unit`: Testes unitários
- `@pytest.mark.integration`: Testes de integração
- `@pytest.mark.api`: Testes de API
- `@pytest.mark.auth`: Testes de autenticação
- `@pytest.mark.models`: Testes de modelos
- `@pytest.mark.serializers`: Testes de serializers
- `@pytest.mark.views`: Testes de views
- `@pytest.mark.performance`: Testes de performance
- `@pytest.mark.validation`: Testes de validação
- `@pytest.mark.slow`: Testes demorados

## Cobertura de Testes

### Account App (25 testes)
- **Autenticação**: 6 testes (login, logout, refresh token)
- **Modelo User**: 10 testes (criação, validação, permissões)
- **Modelo SubscriptionPlan**: 7 testes (planos, validações)
- **Serializadores**: 2 testes

### News App (42 testes)
- **Modelo New**: 12 testes (CRUD, validações, queries)
- **API Endpoints**: 16 testes (GET, POST, PUT, DELETE)
- **Serializadores**: 10 testes (validação de dados)
- **Integração**: 5 testes (fluxos completos)
- **Performance**: 4 testes (otimização de queries)
- **Validações**: 20 testes (edge cases)

### Total: 67+ testes individuais

## Exemplos de Uso

### Executar um Teste Específico
```bash
cd src
pytest apps/account/tests/test_user.py::TestUserModel::test_create_user -v
```

### Executar Testes com Filtro
```bash
cd src
pytest -m "unit and not slow" -v
```

### Executar Testes com Cobertura
```bash
cd src
pytest --cov=apps --cov-report=html --cov-report=term
```

## Integração Contínua

Os testes são projetados para CI/CD com:
- Execução rápida (< 30 segundos)
- Sem dependências externas
- Relatórios em formato JUnit XML
- Cobertura de código automática

## Boas Práticas

1. **Isolation**: Cada teste é isolado e não depende de outros
2. **Fixtures**: Use fixtures para dados de teste consistentes
3. **Markers**: Marque testes apropriadamente para organização
4. **Performance**: Testes devem ser rápidos e eficientes
5. **Coverage**: Mantenha cobertura > 90% em código crítico

## Troubleshooting

### Problemas Comuns
1. **Erro de BD**: Use SQLite para testes (configurado automaticamente)
2. **Migrations**: Desabilitadas por padrão para velocidade
3. **Fixtures**: Certifique-se de que fixtures estão sendo carregadas

### Debug de Testes
```bash
# Modo debug com breakpoints
pytest --pdb apps/account/tests/test_user.py

# Output detalhado
pytest -v -s apps/news/tests/test_models.py
```

## Próximos Passos

1. ✅ Configuração de testes completa
2. ✅ Fixtures e utilitários
3. ✅ Testes para todos os modelos
4. ✅ Testes de API completos
5. ✅ Testes de integração
6. 🔄 Configuração de CI/CD
7. 🔄 Relatórios automáticos de cobertura
8. 🔄 Testes de regressão automáticos