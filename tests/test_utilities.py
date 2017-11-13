import unittest
import os

from utilities import remove_envvars


class TestRemoveEnvvars(unittest.TestCase):
    def test_does_nothing_with_nonexistent_var(self):
        env_at_start = os.environ
        var_to_remove = 'BLAHBLAH'
        self.assertFalse(var_to_remove in os.environ)
        with remove_envvars([var_to_remove]):
            self.assertEqual(env_at_start, os.environ, 'OS environ different inside context manager')
        self.assertEqual(env_at_start, os.environ, 'OS environ different after context manager')

    def test_removes_and_replaces_var(self):
        var_of_interest = 'BLAHBLAH'
        value = '123'

        self.assertFalse(var_of_interest in os.environ)
        os.environ[var_of_interest] = value
        self.assertTrue(var_of_interest in os.environ)
        self.assertEqual(os.environ[var_of_interest], value)

        with remove_envvars([var_of_interest]):
            self.assertFalse(var_of_interest in os.environ)

        self.assertTrue(var_of_interest in os.environ)
        self.assertEqual('123', os.environ[var_of_interest])

    def test_removes_and_replaces_multiple_vars(self):
        vars_of_interest = ['BLAHBLAH0', 'BLAHBLAH1', 'BLAHBLAH2', 'BLAHBLAH3', 'BLAHBLAH4']
        vals = ['0', '1', '2', '3', '4']

        for var, val in zip(vars_of_interest, vals):
            self.assertFalse(var in os.environ)
            os.environ[var] = val
            self.assertTrue(var in os.environ)
            self.assertEqual(os.environ[var], val)

        with remove_envvars(vars_of_interest):
            for var, val in zip(vars_of_interest, vals):
                self.assertFalse(var in os.environ)

        for var, val in zip(vars_of_interest, vals):
            self.assertTrue(var in os.environ)
            self.assertEqual(os.environ[var], val)
