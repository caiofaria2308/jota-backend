#!/bin/bash

# Script para executar testes automatizados - Jota Backend
# Uso: ./run_tests.sh [opção]
# Opções: all, quick, coverage, docker, clean

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para print colorido
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se estamos no diretório correto
if [[ ! -f "docker-compose.test.yml" ]]; then
    print_error "Execute este script a partir do diretório raiz do projeto"
    exit 1
fi

# Função para executar testes rápidos
run_quick_tests() {
    print_status "Executando testes rápidos..."
    docker compose -f docker-compose.test.yml up -d test-db
    sleep 5
    docker compose -f docker-compose.test.yml run --rm test pytest --tb=short -x -q
    print_success "Testes rápidos concluídos!"
}

# Função para executar todos os testes
run_all_tests() {
    print_status "Executando todos os testes..."
    docker compose -f docker-compose.test.yml up -d test-db
    sleep 5
    docker compose -f docker-compose.test.yml run --rm test pytest -v
    print_success "Todos os testes concluídos!"
}

# Função para executar testes com cobertura
run_coverage_tests() {
    print_status "Executando testes com cobertura..."
    docker compose -f docker-compose.test.yml up -d test-db
    sleep 5
    
    # Verificar se pytest-cov está instalado
    docker compose -f docker-compose.test.yml run --rm test pip show pytest-cov > /dev/null 2>&1 || {
        print_warning "Instalando pytest-cov..."
        docker compose -f docker-compose.test.yml run --rm test pip install pytest-cov
    }
    
    docker compose -f docker-compose.test.yml run --rm test pytest --cov=apps --cov-report=term --cov-report=html -v
    print_success "Testes com cobertura concluídos!"
    print_status "Relatório HTML disponível em: src/htmlcov/index.html"
}

# Função para executar testes localmente
run_local_tests() {
    print_status "Executando testes localmente..."
    cd src
    python -m pytest -v
    cd ..
    print_success "Testes locais concluídos!"
}

# Função para limpar ambiente
clean_environment() {
    print_status "Limpando ambiente de teste..."
    docker compose -f docker-compose.test.yml down -v 2>/dev/null || true
    docker system prune -f 2>/dev/null || true
    
    # Limpar cache de teste
    if [[ -d "src/.pytest_cache" ]]; then
        rm -rf src/.pytest_cache
        print_status "Cache pytest removido"
    fi
    
    if [[ -d "src/htmlcov" ]]; then
        rm -rf src/htmlcov
        print_status "Relatórios de cobertura removidos"
    fi
    
    print_success "Ambiente limpo!"
}

# Função para setup inicial
setup_environment() {
    print_status "Configurando ambiente de teste..."
    docker compose -f docker-compose.test.yml up -d test-db
    sleep 10
    
    # Verificar se o banco está respondendo
    if docker compose -f docker-compose.test.yml exec test-db pg_isready -U juser > /dev/null 2>&1; then
        print_success "Banco de dados de teste configurado!"
    else
        print_error "Falha na configuração do banco de dados"
        exit 1
    fi
}

# Função para mostrar estatísticas dos testes
show_test_stats() {
    print_status "Coletando estatísticas dos testes..."
    docker compose -f docker-compose.test.yml up -d test-db > /dev/null 2>&1
    sleep 5
    
    stats=$(docker compose -f docker-compose.test.yml run --rm test pytest --collect-only -q 2>/dev/null | tail -n 1)
    print_success "Estatísticas: $stats"
}

# Função para verificar health dos serviços
check_health() {
    print_status "Verificando health dos serviços..."
    
    # Verificar se Docker está rodando
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker não está rodando"
        exit 1
    fi
    
    # Verificar se os containers estão rodando
    if docker compose -f docker-compose.test.yml ps | grep -q "running"; then
        print_success "Containers de teste estão rodando"
    else
        print_warning "Containers de teste não estão rodando"
        setup_environment
    fi
}

# Função para mostrar ajuda
show_help() {
    echo "Script de Testes - Jota Backend"
    echo ""
    echo "Uso: $0 [opção]"
    echo ""
    echo "Opções disponíveis:"
    echo "  all        - Executar todos os testes com verbose"
    echo "  quick      - Executar testes rápidos (para de no primeiro erro)"
    echo "  coverage   - Executar testes com relatório de cobertura"
    echo "  local      - Executar testes localmente (sem Docker)"
    echo "  docker     - Executar testes no Docker"
    echo "  setup      - Configurar ambiente de teste"
    echo "  clean      - Limpar ambiente e cache"
    echo "  stats      - Mostrar estatísticas dos testes"
    echo "  health     - Verificar health dos serviços"
    echo "  help       - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 quick     # Testes rápidos"
    echo "  $0 coverage  # Testes com cobertura"
    echo "  $0 clean     # Limpar ambiente"
}

# Main script
case "${1:-help}" in
    "all")
        check_health
        run_all_tests
        ;;
    "quick")
        check_health
        run_quick_tests
        ;;
    "coverage")
        check_health
        run_coverage_tests
        ;;
    "local")
        run_local_tests
        ;;
    "docker")
        check_health
        run_all_tests
        ;;
    "setup")
        setup_environment
        ;;
    "clean")
        clean_environment
        ;;
    "stats")
        show_test_stats
        ;;
    "health")
        check_health
        ;;
    "help"|*)
        show_help
        ;;
esac

# Cleanup automático no final (exceto para clean e help)
if [[ ! "$1" =~ ^(clean|help|setup)$ ]]; then
    echo ""
    print_status "Limpando containers temporários..."
    docker compose -f docker-compose.test.yml down > /dev/null 2>&1 || true
fi

echo ""
print_success "Script concluído!"
