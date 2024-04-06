#!/usr/bin/python3
"""
 unittests for my console
"""
from io import StringIO
from unittest.mock import patch
import pycodestyle
import inspect
import unittest
from console import HBNBCommand
import cmd
import console


class Test_HBHNBCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.HBNBConsole = HBNBCommand()

    def test_module_docstring(self):
        self.assertIsNotNone(console.__dict__, 'Module has no docstring')

    def test_class_docstring(self):
        self.assertIsNotNone(HBNBCommand.__doc__, 'Class has no docstring')

    def test_method_docstrings(self):
        # Get all methods defined in HBNBCommand excluding those inherited from cmd.Cmd
        all_methods = [method_name for method_name, _ in inspect.getmembers(HBNBCommand, predicate=inspect.isfunction)]
        inherited_methods = [method_name for method_name, _ in inspect.getmembers(cmd.Cmd, predicate=inspect.isfunction)]
        custom_methods = list(set(all_methods) - set(inherited_methods))

        for method_name in custom_methods:
            method = getattr(self.HBNBConsole, method_name)
            self.assertIsNotNone(method.__doc__, f'{method_name} has no docstring')

    def test_pep8_compliance(self):
        style_guide = pycodestyle.StyleGuide()
        report = style_guide.check_files(["console.py"])
        self.assertEqual(report.total_errors, 0, f"PEP8 violations found: {report.total_errors}")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_missing_class_name(self, mock_stdout):
        # Call do_create without providing class name
        self.HBNBConsole.onecmd("create")
        # Get the printed output
        printed_output = mock_stdout.getvalue().strip()
        # Assert that the printed output matches the expected message
        self.assertEqual(printed_output, '** class name missing **')

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_wrong_name(self, mock_stdout):
        # Call do_create without providing class name
        self.HBNBConsole.onecmd("create Base")
        # Get the printed output
        printed_output = mock_stdout.getvalue().strip()
        # Assert that the printed output matches the expected message
        self.assertEqual(printed_output, "** class dosen't exist **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_wrong_name(self, mock_stdout):
        # Call do_create without providing class name
        self.HBNBConsole.onecmd('create Base')
        printed_output = mock_stdout.getvalue().strip()
        # print(printed_output)

        # Get the printed output
        # Assert that the printed output matches the expected message
        self.assertEqual(printed_output, "** class dosen't exist **")




if __name__ == '__main__':
    unittest.main()
