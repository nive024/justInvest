import unittest
import os
from problem2 import *

class TestProblem2(unittest.TestCase):
    def setUp(self):
        """Create an empty temporary password file for testing."""
        self.test_file = "passwd_test.txt"
        with open(self.test_file, "w") as f:
            pass  

    def tearDown(self):
        """Clean up after tests by removing the test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_encode_password(self):
        """Test if encode_password stores the data correctly."""
        username = "test_username"
        password = "test_password"

        self.assertTrue(encode_password(username, password, self.test_file))

        with open(self.test_file, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 1)
        for line in lines:
            values = line.strip().split(":")
            self.assertEqual(username, values[0]) 

    def test_decode_correct_password(self):
        """Test if decode_password passes with correct password."""
        username = "test_username"
        password = "test_password"
        encode_password(username, password, self.test_file)
        self.assertTrue(decode_password(username, password, self.test_file))

    def test_decode_incorrect_password(self):
        """Test if decode_password fails with incorrect password."""
        username = "test_username"
        password = "test_password"
        incorrect_password = "Test_password"

        encode_password(username, password, self.test_file)
        self.assertFalse(decode_password(username, incorrect_password, self.test_file))  

    def test_decode_password_incorrect_username(self):
        """Test if decode_password fails with incorrect username."""
        username = "test_user"
        password = "test_password"
        wrong_username = "wrong_user"
        
        encode_password(username, password, self.test_file)
        self.assertFalse(decode_password(wrong_username, password, self.test_file))   
        