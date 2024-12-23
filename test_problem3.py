import unittest
from unittest.mock import mock_open, patch
from problem3 import *

mock_roles_permission = {
    "users": {},
    "roles": {
        "CLIENT": {
            "permissions": [1, 2, 4]
        },
        "PREMIUM_CLIENT": {
            "permissions": [1, 2, 4, 3, 5]
        },
        "FINANCIAL_ADVISOR": {
            "permissions": [1, 2, 3, 7]
        },
        "FINANCIAL_PLANNER": {
            "permissions": [1, 2, 3, 6, 7]
        },
        "TELLER": {
            "permissions": [1, 2],
            "time_restriction": {
                "start": "09:00",
                "end": "17:00"
            }
        }
    },
    "permissions": {
        "1": "View account balance",
        "2": "View investment portfolio",
        "3": "Modify investment portfolio",
        "4": "View Financial Advisor contact info",
        "5": "View Financial Planner contact info",
        "6": "View money market instruments",
        "7": "View private consumer instruments"
    }
}

class TestProblem3(unittest.TestCase):
    def test_shorter_than_length(self):
        """Test for a password less than 8 chars"""
        test_password = "nivetha"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must be between 8 to 12 characters long.")

    def test_longer_than_length(self):
        """Test for a password more than 12 chars"""
        test_password = "sivasaravanan"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must be between 8 to 12 characters long.")

    def test_no_digit(self):
        """Test for a password with no digit"""
        test_password = "Passwords!"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must include at least one digit.")

    def test_no_uppercase(self):
        """Test for a password with no uppercase letters"""
        test_password = "passwords1!"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must include at least one uppercase letter.")
    
    def test_no_lowercase(self):
        """Test for a password with no lowercase letters"""
        test_password = "PASSWORDS12@"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must include at least one lowercase letter.")
    
    def test_no_special_char(self):
        """Test for a password with no special characters"""
        test_password = "Nivetha124"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must include a special character from: !, @, #, $, %, *, &.")

    def test_password_include_username(self):
        """Test for a password that contains your username"""
        test_password = "Username124!"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must not contain your username.")

    def test_common_password(self):
        """Test for a common password"""
        test_password = "password12"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password is too common, please choose another one.")

    def test_password_contains_comapny(self):
        """Test for a passowrd not containing the company name"""
        test_password = "JustInvest1@"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password cannot contain company name.")

    def test_password_contains_repetition(self):
        """Test for a passowrd not containing repetition"""
        test_password = "AbCAbC@@!1"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertFalse(isValid)
        self.assertEqual(msg, "Password must not contain one or more repeating sequences.")

    def test_valid_password(self):
        """Test for a password that is valid"""
        test_password = "Password123!"
        test_username = "username"
        isValid, msg = validate_password(test_username, test_password)
        self.assertTrue(isValid)
        self.assertEqual(msg, "")

    @patch('builtins.input', side_effect=["johndoe", "janedoe"])
    def test_get_valid_username_duplicate(self, mock_input):
        """Test for getting a valid username, first duplicate, then unique"""
        mock_users = {
            "john doe": {"username": "johndoe"},
        }
        result = get_valid_username(mock_users)
        self.assertEqual(result, "janedoe")

    @patch('getpass.getpass', side_effect=["Valid@1234", "Valid@1235", "Valid@1234"])
    def test_confirm_password(self, mock_getpass):
        """Test the confirm password functionality"""
        result = get_valid_password("username")
        self.assertEqual(result, "Valid@1234")
        self.assertEqual(mock_getpass.call_count, 3) #first password, wrong confirm, right confirm

    
    @patch('builtins.input', side_effect=["7", "1"]) 
    @patch('problem1.get_roles', return_value={
        "CLIENT": {},
        "PREMIUM_CLIENT": {},
        "FINANCIAL_ADVISOR": {},
        "FINANCIAL_PLANNER": {},
        "TELLER": {}
    })
    def test_assign_role(self, mock_get_roles, mock_input):
        """Test for assigning a valid role, first invalid then valid"""
        result = assign_role()
        self.assertEqual(result, "CLIENT")

    @patch('builtins.input', side_effect=["John Doe", "johndoe", "1"])
    @patch('getpass.getpass', return_value="Valid@1234")
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(mock_roles_permission))
    @patch('json.dump')
    def test_enroll_user(self, mock_json_dump, mock_file, mock_getpass, mock_input):
        """Test successfully enrolling a user"""
        with patch('json.dump') as mock_json_dump:
            success = enroll_user(role_perm_file="roles_permission.json")
            self.assertTrue(success)

            #verify mock JSON file was updated
            mock_file.assert_called_with("roles_permission.json", "w")
            written_data = mock_json_dump.call_args[0][0]

            #assert user was added
            self.assertIn("john doe", written_data["users"])
            self.assertEqual(written_data["users"]["john doe"]["username"], "johndoe")
            self.assertEqual(written_data["users"]["john doe"]["role"], "CLIENT")
