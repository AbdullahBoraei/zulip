from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError
from typing_extensions import override

from analytics.lib.counts import ALL_COUNT_STATS, do_drop_single_stat
from zerver.lib.management import ZulipBaseCommand


class Command(ZulipBaseCommand):
    help = """Clear analytics tables."""

    branch_coverage = {1: False, 2: False, 3: False}

    @override
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--force", action="store_true", help="Actually do it.")
        parser.add_argument("--property", help="The property of the stat to be cleared.")

    @override
    def handle(self, *args: Any, **options: Any) -> None:
        try:
            property = options["property"]
            if property not in ALL_COUNT_STATS:
                Command.branch_coverage[1] = True
                Command.branch_coverage[2] = False
                Command.branch_coverage[3] = False

                raise CommandError(f"Invalid property: {property}")
            
            if not options["force"]:
                Command.branch_coverage[1] = False
                Command.branch_coverage[2] = True
                Command.branch_coverage[3] = False
                raise CommandError("No action taken. Use --force.")
            
            Command.branch_coverage[1] = False
            Command.branch_coverage[2] = False
            Command.branch_coverage[3] = True
            do_drop_single_stat(property)
        finally:
            print("Branch Coverage Report:")
            for branch_id, hit in self.branch_coverage.items():
                print(f"Branch {branch_id}: {'Taken' if hit else 'Not taken'}")
