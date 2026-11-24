"""Pruebas unitarias para la calculadora simple de sumas."""

from decimal import Decimal
import io
import unittest
from unittest.mock import patch

from calculator import format_number, main, parse_number, sum_two_numbers


class TestCalculatorFunctions(unittest.TestCase):
    def test_sum_positive_integers(self) -> None:
        result = sum_two_numbers(parse_number("2"), parse_number("3"))
        self.assertEqual(format_number(result), "5")

    def test_sum_negative_numbers(self) -> None:
        self.assertEqual(
            format_number(sum_two_numbers(parse_number("-4"), parse_number("10"))),
            "6",
        )
        self.assertEqual(
            format_number(sum_two_numbers(parse_number("-5"), parse_number("-7"))),
            "-12",
        )

    def test_sum_decimals_exact(self) -> None:
        result = sum_two_numbers(parse_number("0.1"), parse_number("0.2"))
        self.assertEqual(result, Decimal("0.3"))
        self.assertEqual(format_number(result), "0.3")

    def test_sum_large_round_numbers_and_zeros(self) -> None:
        self.assertEqual(
            format_number(sum_two_numbers(parse_number("1000"), parse_number("2000"))),
            "3000",
        )
        self.assertEqual(
            format_number(sum_two_numbers(parse_number("-0.0"), parse_number("0.0"))),
            "0",
        )

    def test_parse_invalid_inputs(self) -> None:
        for invalid in ("abc", "", "   ", "NaN", "Infinity", "-Infinity"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    parse_number(invalid)


class TestCalculatorCLI(unittest.TestCase):
    def test_cli_positional_arguments(self) -> None:
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            code = main(["5", "7"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue().strip(), "Resultado: 12")

    def test_cli_negative_positional_arguments(self) -> None:
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            code = main(["-4", "10"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue().strip(), "Resultado: 6")

    def test_cli_interactive_mode(self) -> None:
        stdout = io.StringIO()
        with patch.dict("os.environ", {}, clear=True), patch(
            "builtins.input", side_effect=["10.5", "2.5"]
        ), patch("sys.stdout", stdout):
            code = main([])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue().strip(), "Resultado: 13")

    def test_cli_env_vars_mode(self) -> None:
        stdout = io.StringIO()
        with patch.dict("os.environ", {"NUM_A": "12", "NUM_B": "30"}, clear=True), patch(
            "sys.stdout", stdout
        ):
            code = main([])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue().strip(), "Resultado: 42")

    def test_cli_args_override_env_vars(self) -> None:
        stdout = io.StringIO()
        with patch.dict("os.environ", {"NUM_A": "100", "NUM_B": "200"}, clear=True), patch(
            "sys.stdout", stdout
        ):
            code = main(["5", "7"])
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue().strip(), "Resultado: 12")

    def test_cli_partial_env_vars_returns_error(self) -> None:
        stderr = io.StringIO()
        with patch.dict("os.environ", {"NUM_A": "10"}, clear=True), patch(
            "sys.stderr", stderr
        ):
            code = main([])
        self.assertEqual(code, 1)
        self.assertIn("Deben definirse ambas variables de entorno", stderr.getvalue())

    def test_cli_invalid_argument_returns_error(self) -> None:
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = main(["abc", "2"])
        self.assertEqual(code, 1)
        self.assertIn("Número inválido", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
