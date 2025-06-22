#!/usr/bin/env python3
"""
Script para ejecutar linting y formateo de código.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description, check=True):
    """Ejecuta un comando y maneja errores."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Comando: {' '.join(command)}")
    print()

    try:
        result = subprocess.run(command, check=check, capture_output=False)
        if result.returncode == 0:
            print(f"\n✅ {description} - EXITOSO")
            return True
        else:
            print(f"\n⚠️ {description} - COMPLETADO CON ADVERTENCIAS")
            return False
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FALLÓ (código de salida: {e.returncode})")
        return False


def install_dependencies():
    """Instala las dependencias de linting."""
    return run_command(
        ["pip", "install", "-r", "requirements-test.txt"],
        "Instalando dependencias de linting y formateo",
    )


def run_black(check_only=False):
    """Ejecuta Black para formateo de código."""
    command = ["black"]
    if check_only:
        command.extend(["--check", "--diff"])
        description = "Verificando formateo con Black"
    else:
        description = "Formateando código con Black"

    command.extend(["src", "tests", "scripts"])
    return run_command(command, description, check=False)


def run_isort(check_only=False):
    """Ejecuta isort para ordenar imports."""
    command = ["isort"]
    if check_only:
        command.extend(["--check-only", "--diff"])
        description = "Verificando orden de imports con isort"
    else:
        description = "Ordenando imports con isort"

    command.extend(["src", "tests", "scripts"])
    return run_command(command, description, check=False)


def run_ruff():
    """Ejecuta Ruff para linting rápido."""
    return run_command(
        ["ruff", "check", "src", "tests", "scripts"],
        "Ejecutando linting con Ruff",
        check=False,
    )


def run_ruff_fix():
    """Ejecuta Ruff con auto-fix."""
    return run_command(
        ["ruff", "check", "--fix", "src", "tests", "scripts"],
        "Ejecutando auto-fix con Ruff",
        check=False,
    )


def run_flake8():
    """Ejecuta Flake8 para linting adicional."""
    return run_command(
        ["flake8", "src", "tests", "scripts"],
        "Ejecutando linting con Flake8",
        check=False,
    )


def run_bandit():
    """Ejecuta Bandit para análisis de seguridad."""
    return run_command(
        ["bandit", "-r", "src"],
        "Ejecutando análisis de seguridad con Bandit",
        check=False,
    )


def run_all_checks():
    """Ejecuta todas las verificaciones sin modificar código."""
    print("🔍 Ejecutando todas las verificaciones de código...")

    results = []
    results.append(run_black(check_only=True))
    results.append(run_isort(check_only=True))
    results.append(run_ruff())
    results.append(run_flake8())
    results.append(run_bandit())

    return all(results)


def run_all_fixes():
    """Ejecuta todas las herramientas con auto-fix."""
    print("🔧 Ejecutando formateo y auto-fix...")

    results = []
    results.append(run_black())
    results.append(run_isort())
    results.append(run_ruff_fix())

    # Verificaciones finales
    results.append(run_flake8())
    results.append(run_bandit())

    return all(results)


def setup_pre_commit():
    """Configura pre-commit hooks."""
    return run_command(["pre-commit", "install"], "Configurando pre-commit hooks")


def run_pre_commit():
    """Ejecuta pre-commit en todos los archivos."""
    return run_command(
        ["pre-commit", "run", "--all-files"], "Ejecutando pre-commit hooks", check=False
    )


def main():
    parser = argparse.ArgumentParser(description="Herramientas de linting y formateo")
    parser.add_argument(
        "command",
        choices=[
            "install",
            "check",
            "fix",
            "black",
            "isort",
            "ruff",
            "flake8",
            "bandit",
            "pre-commit-install",
            "pre-commit-run",
            "all",
        ],
        help="Comando a ejecutar",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Solo verificar, no modificar archivos",
    )

    args = parser.parse_args()

    # Cambiar al directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    success = True

    if args.command == "install":
        success = install_dependencies()
    elif args.command == "check":
        success = run_all_checks()
    elif args.command == "fix":
        success = run_all_fixes()
    elif args.command == "black":
        success = run_black(check_only=args.check_only)
    elif args.command == "isort":
        success = run_isort(check_only=args.check_only)
    elif args.command == "ruff":
        success = run_ruff_fix() if not args.check_only else run_ruff()
    elif args.command == "flake8":
        success = run_flake8()
    elif args.command == "bandit":
        success = run_bandit()
    elif args.command == "pre-commit-install":
        success = setup_pre_commit()
    elif args.command == "pre-commit-run":
        success = run_pre_commit()
    elif args.command == "all":
        if args.check_only:
            success = run_all_checks()
        else:
            success = run_all_fixes()

    if success:
        print("\n🎉 ¡Operación completada exitosamente!")
        sys.exit(0)
    else:
        print("\n💥 La operación completó con advertencias o errores.")
        print("💡 Revisa los mensajes arriba para más detalles.")
        sys.exit(1)


if __name__ == "__main__":
    main()
