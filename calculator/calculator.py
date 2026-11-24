#!/usr/bin/env python3
"""Calculadora simple que suma dos números."""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import os
import sys


def parse_number(raw: str) -> Decimal:
    """Convierte una cadena de texto en un número Decimal finito."""
    try:
        value = Decimal(raw.strip())
    except InvalidOperation as exc:
        raise ValueError(f"Número inválido: {raw!r}") from exc
    if not value.is_finite():
        raise ValueError(f"El número debe ser finito: {raw!r}")
    return value


def sum_two_numbers(a: Decimal, b: Decimal) -> Decimal:
    """Devuelve la suma de dos números."""
    return a + b


def format_number(value: Decimal) -> str:
    """Formatea un número Decimal sin ceros decimales innecesarios."""
    normalized = value.normalize()
    if normalized == 0:
        return "0"
    return format(normalized, "f")


def build_parser() -> argparse.ArgumentParser:
    """Construye el analizador de argumentos de la CLI."""
    parser = argparse.ArgumentParser(
        description="Calculadora simple que suma dos números."
    )
    parser.add_argument("a", nargs="?", help="Primer número")
    parser.add_argument("b", nargs="?", help="Segundo número")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ejecuta la CLI de la calculadora de sumas.

    Orden de prioridad de entrada:
    1. Argumentos posicionales de la CLI (`a`, `b`)
    2. Variables de entorno (`NUM_A`, `NUM_B`)
    3. Entrada interactiva por consola
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if (args.a is None) ^ (args.b is None):
        parser.error(
            "Proporciona ambos números o ninguno para usar variables de entorno o modo interactivo."
        )

    env_a = os.environ.get("NUM_A")
    env_b = os.environ.get("NUM_B")

    try:
        if args.a is not None and args.b is not None:
            raw_a, raw_b = args.a, args.b
        elif env_a is not None or env_b is not None:
            if env_a is None or env_b is None:
                raise ValueError(
                    "Deben definirse ambas variables de entorno: NUM_A y NUM_B."
                )
            raw_a, raw_b = env_a, env_b
        else:
            raw_a = input("Ingresa el primer número: ")
            raw_b = input("Ingresa el segundo número: ")

        a = parse_number(raw_a)
        b = parse_number(raw_b)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nCancelado.", file=sys.stderr)
        return 1

    result = sum_two_numbers(a, b)
    print(f"Resultado: {format_number(result)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
