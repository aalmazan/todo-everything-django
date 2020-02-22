import pytest
from model_bakery import baker
from todo_everything.apps.accounts.models import Account

# def test_account_factory(account_factory):
#     assert type(account_factory) == type(AccountFactory)

# @pytest.mark.django_db
# def test_account_instance(account):
#     """Test account instance works"""
#     assert isinstance(account, Account)


@pytest.mark.django_db
def test_account_model_default_sanity():
    account = baker.make(Account)
    assert isinstance(account, Account)
