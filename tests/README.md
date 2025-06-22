# Test Suite

Suite de tests para el Task Manager API.

## Estructura

```
tests/
├── unit/              # Tests unitarios
├── integration/       # Tests de integración
├── conftest.py        # Configuración de fixtures
└── README.md          # Esta documentación
```

## Ejecutar Tests

```bash
# Todos los tests
python scripts/run_tests.py all

# Solo unitarios
python scripts/run_tests.py unit

# Solo integración
python scripts/run_tests.py integration

# Con cobertura
python scripts/run_tests.py all --coverage
```

## Cobertura

Los tests están configurados para mantener al menos 80% de cobertura.

## Base de Datos

Los tests usan SQLite en memoria para ser rápidos y aislados.

## Mocking

- Servicios externos (Resend email) están mockeados
- JWT tokens son generados para tests de autenticación

## Fixtures Principales

- `test_user`: Usuario de prueba
- `test_list_task`: Lista de tareas de prueba
- `test_task`: Tarea de prueba
- `auth_headers`: Headers de autenticación
- `client`: Cliente de prueba FastAPI
