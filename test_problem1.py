import unittest
from problem1 import *

class TestProblem1(unittest.TestCase):
    with open("roles_permission.json", "r") as f:
        data = json.load(f)
        permissions = data["permissions"]
        users = data["users"]
        roles = data["roles"]
    
    #create users
    user_objs = {}
    for user in users:
        perms = roles[users[user]["role"]]["permissions"]
        time = {}
        try:
            time = roles[users[user]["role"]]["time_restriction"]
        except KeyError:
            pass 
        user_objs[user] = User(user, users[user], perms, time)

    def test_find_authorized_operations_client(self):
        # Test for a user with the CLIENT role
        expected_permissions = ['1', '2', '4']
        result = self.user_objs["sasha kim"].get_permissions()
        self.assertEqual(result, expected_permissions)

    def test_find_authorized_operations_premium_client(self):
        # Test for a user with both CLIENT and PREMIUM_CLIENT roles
        expected_permissions = ['1', '2', '3', '4', '5']
        result = self.user_objs["noor abbasi"].get_permissions()
        self.assertEqual(sorted(result), sorted(expected_permissions))

    def test_find_authorized_operations_financial_advisor(self):
        # Test for a user with the FINANCIAL_ADVISOR role
        expected_permissions = ['1', '2', '3', '7']
        result = self.user_objs["mikael chen"].get_permissions()
        self.assertEqual(result, expected_permissions)

    def test_find_authorized_operations_financial_planner(self):
        # Test for a user with the FINANCIAL_PLANNER role
        expected_permissions = ['1', '2', '3', '6', '7']
        result = self.user_objs["ellis nakamura"].get_permissions()
        self.assertEqual(result, expected_permissions)

    def test_find_authorized_operations_teller(self):
        # Test for a user with the TELLER role
        expected_permissions = ['1', '2']
        result = self.user_objs["alex hayes"].get_permissions()
        self.assertEqual(result, expected_permissions)

    def test_access_denied(self):
        # Test for a user not in the system
        name = "unknown user"
        self.assertNotIn(name.lower(), self.user_objs.keys())
    
    def test_no_permission(self):
        # Test for a user trying to access an operation they can't
        user = self.user_objs["sasha kim"]
        self.assertFalse(user.has_permission('3'))

    def test_time_restriction(self):
        # Test that a user with a time restriction can't access it outside of given time
        user = self.user_objs["alex hayes"]
        hour = datetime.datetime.now().hour
        if hour > 9 and hour < 17:
            self.assertTrue(check_time_restriction(user.get_time_restrictions()))
        else:
            self.assertFalse(check_time_restriction(user.get_time_restrictions()))

