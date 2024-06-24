from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError
from typing_extensions import override

from analytics.lib.counts import do_drop_all_analytics_tables
from zerver.lib.management import ZulipBaseCommand
from zilencer.views import get_last_id_from_server
from argparse import ArgumentParser
from typing import Any
from typing_extensions import override
from analytics.lib.counts import do_drop_all_analytics_tables
from zerver.lib.management import ZulipBaseCommand

# command_module.py
from argparse import ArgumentParser
from typing import Any
from django.core.management.base import CommandError
from typing_extensions import override
from analytics.lib.counts import do_drop_all_analytics_tables
from zerver.lib.management import ZulipBaseCommand

class Command(ZulipBaseCommand):
    # Step 2: Create data structures for coverage information
    branch_coverage = {
        1: False,  # for 'if options["force"]'
        2: False   # for 'else'
    }

    help = """Clear analytics tables."""

    @override
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--force", action="store_true", help="Clear analytics tables.")

    @override
    def handle(self, *args: Any, **options: Any) -> None:
        try:
        # Step 3: Set flags for branch coverage
            if options["force"]:
                Command.branch_coverage[1] = True
                Command.branch_coverage[2] = False
                do_drop_all_analytics_tables()
            else:
                Command.branch_coverage[2] = True
                Command.branch_coverage[1] = False
                raise CommandError("Would delete all data from analytics tables (!); use --force to do so.")

        finally:
            # Ensure the branch coverage report is always printed
            print("Branch Coverage Report:")
            for branch_id, hit in Command.branch_coverage.items():
                print(f"Branch {branch_id}: {'Taken' if hit else 'Not taken'}")
