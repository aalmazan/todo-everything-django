from logging import getLogger

from accounts.models import Account
from django.core.management.base import BaseCommand
from todos import factories

logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Generate Todo test data"

    def add_arguments(self, parser):
        parser.add_argument("-n", "--number", type=int, default=10)
        parser.add_argument(
            "-u", "--user", type=int, required=False, help="User id for the todos"
        )

    def handle(self, *args, **options):
        user = None
        user_id = options.get("user", None)

        if user_id:
            user = Account.objects.get(pk=user_id)
            print("User", user)

        for _ in range(options["number"]):
            print(_)
            if user:
                logger.info(f"Generating {user}'s todos")
                factories.TodoFactory(created_by=user)
            else:
                logger.info("Generating")
                factories.TodoFactory()
