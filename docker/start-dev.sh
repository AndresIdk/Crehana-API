#!/bin/bash

# Script para iniciar el entorno de desarrollo
echo "Iniciando Crehana Task Manager"
echo "=============================="

# Cambiar al directorio del script
cd "$(dirname "$0")"
echo "Directorio: $(pwd)"

# Verificar que Docker esté corriendo
if ! docker info >/dev/null 2>&1; then
    echo "ERROR: Docker no esta corriendo"
    echo "Inicia Docker e intenta de nuevo"
    exit 1
fi

echo "Configuracion lista"

# Configurar pre-commit hooks si no están instalados
echo "Revisando pre-commit hooks..."
cd ..
if [ -f ".git/hooks/pre-commit" ]; then
    echo "Pre-commit ya configurado"
else
    echo "Instalando pre-commit hooks..."
    python scripts/lint.py pre-commit-install
    if [ $? -eq 0 ]; then
        echo "Pre-commit hooks listos"
    else
        echo "Advertencia: Error instalando pre-commit hooks"
        echo "Puedes instalarlo manualmente: python scripts/lint.py pre-commit-install"
    fi
fi
cd docker

# Limpiar contenedores anteriores
echo "Limpiando contenedores..."
docker-compose down >/dev/null 2>&1

# Construir imágenes
echo "Construyendo imagenes..."
docker-compose build api-dev
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo construir la imagen"
    exit 1
fi

# Iniciar servicios de desarrollo
echo "Iniciando servicios..."
docker-compose up -d postgres
if [ $? -ne 0 ]; then
    echo "ERROR: PostgreSQL no se pudo iniciar"
    exit 1
fi

# Esperar a que PostgreSQL esté listo
echo "Esperando PostgreSQL..."
sleep 10
while ! docker-compose exec postgres pg_isready -U crehana_user -d task_manager >/dev/null 2>&1; do
    echo "Aun no esta listo, esperando..."
    sleep 3
done

echo "PostgreSQL listo"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
docker-compose run --rm api-dev alembic upgrade head
if [ $? -ne 0 ]; then
    echo "ERROR: Fallo en migraciones"
    exit 1
fi

# Iniciar API de desarrollo
echo "Iniciando API..."
echo "Presiona Ctrl+C para parar"
docker-compose up api-dev

echo ""
echo "Entorno iniciado correctamente"
echo ""
echo "Servicios:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - DB: localhost:5432"
echo ""
echo "Comandos utiles:"
echo "  - Logs: docker-compose logs -f api-dev"
echo "  - Tests: docker-compose --profile testing run --rm test-runner"
echo "  - Linting: docker-compose --profile linting run --rm linter"
echo "  - Parar: docker-compose down"
echo ""
echo "Pre-commit configurado para git commits"
echo ""
