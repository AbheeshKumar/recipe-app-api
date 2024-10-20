from unittest.mock import patch

# Connecting to db before its ready
from psycopg2 import OperationalError as Psycog2Error

# Calling command by name
from django.core.management import call_command

# Database exception
from django.db.utils import OperationalError

# Base test class for testing
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        """Test Waiting for db if db already ready"""
        patched_check.return_value = True

        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    # Usually there is a sleep interval each time database is called
    # This is useful in production
    # However in testing , it slows test down so we remove it
    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test Waiting for database when getting OperationalError"""
        # 2 times psycog2Error is called to check if postgres is initialized
        # and 3 times OperationalError is called to check if devdb is created
        # in 6th time, True returns db successfully launched
        patched_check.side_effect = [Psycog2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command("wait_for_db")
        # 6 times patched_check is called, 2+3+1
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
