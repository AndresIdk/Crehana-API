"""
Script para ejecutar tests del proyecto Task Manager con diferentes configuraciones.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Ejecuta un comando y maneja errores."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Comando: {' '.join(command)}")
    print()

    try:
        subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description} - EXITOSO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FALLÓ (código de salida: {e.returncode})")
        return False


def install_dependencies():
    """Instala las dependencias de testing."""
    return run_command(
        ["pip", "install", "-r", "requirements-test.txt"],
        "Instalando dependencias de testing",
    )


def run_unit_tests():
    """Ejecuta solo los tests unitarios."""
    return run_command(["pytest", "tests/unit/", "-v"], "Ejecutando tests unitarios")


def run_integration_tests():
    """Ejecuta solo los tests de integración."""
    return run_command(
        ["pytest", "tests/integration/", "-v"], "Ejecutando tests de integración"
    )


def run_all_tests():
    """Ejecuta todos los tests."""
    return run_command(["pytest", "-v"], "Ejecutando todos los tests")


def run_tests_with_coverage():
    """Ejecuta tests con reporte de cobertura."""
    return run_command(
        ["pytest", "--cov=src", "--cov-report=html", "--cov-report=term-missing", "-v"],
        "Ejecutando tests con cobertura",
    )


def run_specific_test_file(file_path):
    """Ejecuta un archivo de test específico."""
    return run_command(
        ["pytest", file_path, "-v"], f"Ejecutando tests del archivo: {file_path}"
    )


def run_tests_by_marker(marker):
    """Ejecuta tests con un marcador específico."""
    return run_command(
        ["pytest", "-m", marker, "-v"], f"Ejecutando tests con marcador: {marker}"
    )


def run_parallel_tests():
    """Ejecuta tests en paralelo."""
    return run_command(["pytest", "-n", "auto", "-v"], "Ejecutando tests en paralelo")


def run_fast_tests():
    """Ejecuta tests rápidos (sin marcador slow)."""
    return run_command(["pytest", "-m", "not slow", "-v"], "Ejecutando tests rápidos")


def generate_coverage_report():
    """Genera reporte de cobertura HTML."""
    success = run_command(
        ["pytest", "--cov=src", "--cov-report=html", "--cov-report=xml"],
        "Generando reporte de cobertura",
    )

    if success:
        print(
            f"\n📊 Reporte de cobertura HTML generado en: {Path('htmlcov/index.html').absolute()}"
        )
        print(
            f"📊 Reporte de cobertura XML generado en: {Path('coverage.xml').absolute()}"
        )

    return success


def main():
    parser = argparse.ArgumentParser(description="Ejecutor de tests para Task Manager")
    parser.add_argument(
        "command",
        choices=[
            "install",
            "unit",
            "integration",
            "all",
            "coverage",
            "parallel",
            "fast",
            "report",
            "auth",
            "task",
            "list_task",
        ],
        help="Comando a ejecutar",
    )
    parser.add_argument("--file", help="Archivo de test específico a ejecutar")

    args = parser.parse_args()

    # Cambiar al directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Agregar el directorio raíz al PYTHONPATH
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    success = True

    if args.command == "install":
        success = install_dependencies()
    elif args.command == "unit":
        success = run_unit_tests()
    elif args.command == "integration":
        success = run_integration_tests()
    elif args.command == "all":
        success = run_all_tests()
    elif args.command == "coverage":
        success = run_tests_with_coverage()
    elif args.command == "parallel":
        success = run_parallel_tests()
    elif args.command == "fast":
        success = run_fast_tests()
    elif args.command == "report":
        success = generate_coverage_report()
    elif args.command in ["auth", "task", "list_task"]:
        success = run_tests_by_marker(args.command)

    if args.file:
        success = run_specific_test_file(args.file)

    if success:
        print("\n🎉 ¡Operación completada exitosamente!")
        sys.exit(0)
    else:
        print("\n💥 La operación falló. Revisa los errores arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main()
