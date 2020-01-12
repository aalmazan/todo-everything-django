import pytest
from todo_everything.apps.accounts.models import Account

from .factories import AccountFactory


def test_account_factory(account_factory):
    assert type(account_factory) == type(AccountFactory)


@pytest.mark.django_db
def test_account_instance(account):
    """Test account instance works"""
    assert isinstance(account, Account)
