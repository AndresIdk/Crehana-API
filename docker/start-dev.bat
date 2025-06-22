@echo off
chcp 65001 >nul

REM Script para iniciar el entorno de desarrollo
echo Iniciando Crehana Task Manager
echo ==============================

REM Cambiar al directorio del script
cd /d "%~dp0"
echo Directorio: %cd%

REM Verificar que Docker esté corriendo
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker no esta corriendo
    echo Inicia Docker Desktop e intenta de nuevo
    pause
    exit /b 1
)

echo Configuracion lista

REM Configurar pre-commit hooks si no están instalados
echo Revisando pre-commit hooks...
cd ..
if exist ".git\hooks\pre-commit" (
    echo Pre-commit ya configurado
) else (
    echo Instalando pre-commit hooks...
    python scripts/lint.py pre-commit-install
    if errorlevel 1 (
        echo Advertencia: Error instalando pre-commit hooks
        echo Puedes instalarlo manualmente: python scripts/lint.py pre-commit-install
    ) else (
        echo Pre-commit hooks listos
    )
)
cd docker

REM Limpiar contenedores anteriores
echo Limpiando contenedores...
docker-compose down >nul 2>&1

REM Construir imágenes
echo Construyendo imagenes...
docker-compose build api-dev
if errorlevel 1 (
    echo ERROR: No se pudo construir la imagen
    pause
    exit /b 1
)

REM Iniciar servicios de desarrollo
echo Iniciando servicios...
docker-compose up -d postgres
if errorlevel 1 (
    echo ERROR: PostgreSQL no se pudo iniciar
    pause
    exit /b 1
)

REM Esperar a que PostgreSQL esté listo
echo Esperando PostgreSQL...
timeout /t 10 /nobreak >nul
:wait_postgres
docker-compose exec postgres pg_isready -U crehana_user -d task_manager >nul 2>&1
if errorlevel 1 (
    echo Aun no esta listo, esperando...
    timeout /t 3 /nobreak >nul
    goto wait_postgres
)

echo PostgreSQL listo

REM Ejecutar migraciones
echo Ejecutando migraciones...
docker-compose run --rm api-dev alembic upgrade head
if errorlevel 1 (
    echo ERROR: Fallo en migraciones
    pause
    exit /b 1
)

REM Iniciar API de desarrollo
echo Iniciando API...
echo Presiona Ctrl+C para parar
docker-compose up api-dev

echo.
echo Entorno iniciado correctamente
echo.
echo Servicios:
echo   - API: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo   - DB: localhost:5432
echo.
echo Comandos utiles:
echo   - Logs: docker-compose logs -f api-dev
echo   - Tests: docker-compose --profile testing run --rm test-runner
echo   - Linting: docker-compose --profile linting run --rm linter
echo   - Parar: docker-compose down
echo.
echo Pre-commit configurado para git commits
echo.
pause
