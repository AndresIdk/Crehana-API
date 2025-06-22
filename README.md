# Task Manager API - Crehana

Una API REST para gestión de tareas construida con FastAPI y PostgreSQL. Este proyecto incluye autenticación JWT, testing completo, y está containerizado con Docker.
Tenemos unas configuracion basada en Clean Architecture, donde se intento de manera basica (lo digo asi porque se puede mejorar muchos más) mosntrar conceptos como inyeccion de dependencias,
interfaces, abstracciones, etc. Tambien tenemos un enfoque al desacoplamiento donde simulamos una inyeccion de base de datos (PostgreSQL y MySQL), actualmente quedó la configuracion de
postgres lista pero se dejo todo en su lugar para crear una implementacion de MySQl que se pueda utilizar, bueno, realmente cualquier base de datos.

## ¿Qué hace esta API?

La API permite:
- Registrar usuarios y autenticarse con JWT
- Crear y gestionar listas de tareas
- Añadir, editar y eliminar tareas dentro de las listas
- Enviar notificaciones por email (integrado con Resend)

## Empezar rápidamente

### Docker

Clona el repo y levanta los servicios:

```bash
git clone https://github.com/AndresIdk/Crehana-API.git (esto para wimdows, tambien puedes clonar via ssh)
git clone git@github.com:AndresIdk/Crehana-API.git
cd CREHANA/docker
./start-dev.bat  # Windows
# o
./start-dev.sh   # Linux/Mac
```

Esto levanta automáticamente:
- API en http://localhost:8000
- PostgreSQL en puerto 5434
- Ejecuta las migraciones
- Documentación en http://localhost:8000/docs

### Manual

Si prefieres trabajar sin Docker:

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements-test.txt
pip install -r requirements.txt

# Configurar PostgreSQL local y ejecutar
alembic upgrade head
fastapi dev .\src\main.py o fastapi run .\src\main.py
```

## Testing

```bash
# Con Docker
docker compose --profile testing run --rm test-runner

# Local
python scripts/run_tests.py all o utilizar el script
```

Comandos útiles:
- `python scripts/run_tests.py unit` - Solo tests unitarios
- `python scripts/run_tests.py integration` - Solo integración
- `python scripts/run_tests.py coverage` - Con reporte de cobertura
- `python scripts/run_tests.py auth` - Solo tests de autenticación

## Calidad de código

El proyecto usa múltiples herramientas para mantener la calidad:

```bash
# Formatear todo el código
python scripts/lint.py fix

# Solo verificar
python scripts/lint.py check
```

Herramientas configuradas:
- **Black** - Formateo automático
- **isort** - Ordenar imports
- **Ruff** - Linting rápido y moderno
- **Flake8** - Verificaciones adicionales
- **Bandit** - Análisis de seguridad

También hay pre-commit hooks que se ejecutan automáticamente:
```bash
python scripts/lint.py pre-commit-install
```

## Estructura del proyecto

```
src/
├── api/                 # Endpoints y schemas
├── application/         # Lógica de negocio
├── domain/             # Modelos y interfaces
├── infrastructure/     # Repositorios y servicios externos
└── main.py            # Punto de entrada

tests/
├── unit/              # Tests unitarios
└── integration/       # Tests de integración

configs/               # Configuraciones por ambiente
docker/               # Docker Compose y scripts
alembic/              # Migraciones de BD
```

## Endpoints principales

La API está documentada automáticamente en `/docs`

**Autenticación:**
- `POST /auth/register` - Crear cuenta
- `POST /auth/login` - Obtener token JWT

**Listas de tareas:**
- `GET /list_tasks/` - Ver todas las listas
- `POST /list_tasks/` - Crear lista nueva
- `PUT /list_tasks/{id}` - Editar lista
- `DELETE /list_tasks/{id}` - Eliminar lista

**Tareas:**
- `GET /tasks/` - Ver todas las tareas
- `POST /tasks/` - Crear tarea
- `PUT /tasks/{id}` - Editar tarea
- `DELETE /tasks/{id}` - Eliminar tarea

Todos los endpoints de tareas y listas de tareas requieren autenticación JWT.

## Base de datos

Usamos PostgreSQL con SQLAlchemy y Alembic para las migraciones.

**Migraciones:**
```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones
alembic upgrade head
```

## Configuración por ambientes

El proyecto usa diferentes configuraciones según el ambiente:

- **Desarrollo**: `configs/config_dev_postgres.py`
- **Producción**: `configs/config_prod_postgres.py`

Se controla con la variable `APP_SETTINGS_MODULE`. Docker Compose ya viene configurado en modo de desarrollo, lo puedes cambiar si gustas.

## Docker Compose

Tenemos varios profiles para diferentes necesidades:

```bash
# Desarrollo (API + PostgreSQL)
docker-compose up api-dev postgres

# Producción
docker-compose --profile production up api-prod postgres

# Con pgAdmin para gestionar la BD
docker-compose --profile admin up api-dev postgres pgadmin

# Solo testing
docker-compose --profile testing run test-runner

# Solo linting
docker-compose --profile linting run linter
```

**Puertos:**
- API desarrollo: 8000
- API producción: 8001
- PostgreSQL: 5434
- pgAdmin: 5050 (admin@crehana.com / admin123)

## Email notifications

Integrado con Resend para envío de emails. Configura estas variables (Yo dejé unas propias en los archivos de config para que pruebes):

```bash
RESEND_API_KEY=tu_api_key
RESEND_FROM_EMAIL=noreply@tudominio.com
```

Los pre-commit hooks se encargan de verificar el formato automáticamente.

## Troubleshooting

**Error de puerto ocupado:**
- PostgreSQL usa puerto 5434 (no el estándar 5432)
- Si tienes conflictos, cambia el puerto en docker-compose.yml

**Tests fallan:**
- Asegúrate de que PostgreSQL esté corriendo
- Verifica que las migraciones estén aplicadas: `alembic upgrade head`

**Problemas con migraciones:**
- Revisa que todos los modelos estén importados en `alembic/env.py`
- Ejecuta `alembic revision --autogenerate` para crear nuevas migraciones
