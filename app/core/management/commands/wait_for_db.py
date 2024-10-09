"""
Django COmmand to wait for db to be available
"""

import time
from psycopg2 import OperationalError as Psycog2Error
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        """EntryPoint for command"""
        self.stdout.write("Waiting for database...")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycog2Error, OperationalError):
                self.stdout.write("Database Unavailable, waiting 1 sec...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database Available"))
