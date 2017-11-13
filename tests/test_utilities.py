import unittest
import os

from utilities import remove_envvars, add_envvars


class TestRemoveEnvvars(unittest.TestCase):
    def test_does_nothing_with_nonexistent_var(self):
        env_at_start = os.environ
        var_to_remove = 'BLAHBLAH'
        self.assertTrue(var_to_remove not in os.environ)
        with remove_envvars([var_to_remove]):
            self.assertEqual(env_at_start, os.environ, 'OS environ different inside context manager')
        self.assertEqual(env_at_start, os.environ, 'OS environ different after context manager')

    def test_removes_and_replaces_var(self):
        var_of_interest = 'BLAHBLAH'
        value = '123'

        self.assertTrue(var_of_interest not in os.environ)
        os.environ[var_of_interest] = value
        self.assertTrue(var_of_interest in os.environ)
        self.assertEqual(os.environ[var_of_interest], value)

        with remove_envvars([var_of_interest]):
            self.assertTrue(var_of_interest not in os.environ)

        self.assertTrue(var_of_interest in os.environ)
        self.assertEqual('123', os.environ[var_of_interest])

    def test_removes_and_replaces_multiple_vars(self):
        vars_of_interest = ['BLAHBLAH0', 'BLAHBLAH1', 'BLAHBLAH2', 'BLAHBLAH3', 'BLAHBLAH4']
        vals = ['0', '1', '2', '3', '4']

        for var, val in zip(vars_of_interest, vals):
            self.assertTrue(var not in os.environ)
            os.environ[var] = val
            self.assertTrue(var in os.environ)
            self.assertEqual(os.environ[var], val)

        with remove_envvars(vars_of_interest):
            for var, val in zip(vars_of_interest, vals):
                self.assertTrue(var not in os.environ)

        for var, val in zip(vars_of_interest, vals):
            self.assertTrue(var in os.environ)
            self.assertEqual(os.environ[var], val)


class TestAddVars(unittest.TestCase):
    def test_adds_single_variable(self):
        var_to_add = 'BLAHBLAH'
        val = '123'
        self.assertTrue(var_to_add not in os.environ)
        with add_envvars({var_to_add: val}):
            self.assertTrue(var_to_add in os.environ)
            self.assertEqual(val, os.environ[var_to_add])
        self.assertTrue(var_to_add not in os.environ)

    def test_adds_multiple_vars(self):
        vars_of_interest = ['BLAHBLAH0', 'BLAHBLAH1', 'BLAHBLAH2', 'BLAHBLAH3', 'BLAHBLAH4']
        vals = ['0', '1', '2', '3', '4']

        for var in vars_of_interest:
            self.assertTrue(var not in os.environ)

        with add_envvars(dict(zip(vars_of_interest, vals))):
            for var, val in zip(vars_of_interest, vals):
                self.assertTrue(var in os.environ)
                self.assertEqual(os.environ[var], val)

        for var in vars_of_interest:
            self.assertTrue(var not in os.environ)
