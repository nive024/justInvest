import unittest
import os
from unittest.mock import patch, MagicMock
from io import StringIO
from problem4 import *
from problem1 import *


class TestProblem4(unittest.TestCase):
    test_user = User("test_user", "CLIENT", [1, 2, 4], {})

    def setUp(self):
        """Create an empty temporary password file for testing."""
        self.test_file = "passwd_test.txt"
        with open(self.test_file, "w") as f:
            pass  

    def tearDown(self):
        """Clean up after tests by removing the test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('builtins.input', return_value="1")
    @patch('builtins.print')
    def test_perform_authorized_operation(self, mock_print, mock_input):
        """Test authorized operation performance"""
        self.assertTrue(perform_operations(self.test_user))
        mock_print.assert_called_with(f"You have performed {get_permissions()['1']}")

    @patch('builtins.input', return_value="6")
    @patch('builtins.print')
    def test_perform_unauthorized_operation(self, mock_print, mock_input):
        """Test unauthorized operation performance"""
        self.assertFalse(perform_operations(self.test_user))
        mock_print.assert_called_with("You are not permitted to perform this operation.")

    @patch('builtins.input', return_value="exit")
    @patch('builtins.print')
    @patch('problem4.sys.exit')
    def test_perform_exit_operation(self, mock_exit, mock_print, mock_input):
        """Test exit operation performance"""
        try:
            self.assertFalse(perform_operations(self.test_user))
        except SystemExit as e:
            mock_print.assert_called_with("Exiting operation menu.")
            mock_exit.assert_called_with(0)
            self.assertEqual(e.code, 0)

    @patch('builtins.input', return_value="hello")
    @patch('builtins.print')
    def test_perform_random_operation(self, mock_print, mock_input):
        """Test random operation performance"""
        try:
            self.assertFalse(perform_operations(self.test_user))
        except ValueError:
            mock_print.assert_called_with("Invalid input. Please enter a valid operation number or 'exit' to quit.")

    @patch('builtins.input', return_value="10")
    @patch('builtins.print')
    def test_perform_nonexistent_operation(self, mock_print, mock_input):
        """Test nonexistent operation performance"""
        try:
            self.assertFalse(perform_operations(self.test_user))
        except KeyError:
            mock_print.assert_called_with("The specified operation does not exist.")

    @patch('builtins.print')
    def test_login_user(self, mock_print):
        """Test valid login for user"""
        username = "test_username"
        password = "Password123!"
        encode_password(username, password, self.test_file)
        login_user(username, password, self.test_file)
        mock_print.assert_called_with("ACCESS GRANTED!")

    @patch('builtins.print')
    def test_invalid_login_user(self, mock_print):
        """Test invalid login for user"""
        username = "test_username"
        password = "Password123!"
        wrong_password = "Password123!!"
        encode_password(username, password, self.test_file)
        login_user(username, wrong_password, self.test_file)
        mock_print.assert_called_with("ACCESS DENIED!")





        
    


