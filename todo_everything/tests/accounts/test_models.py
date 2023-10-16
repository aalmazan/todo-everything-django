import pytest
from accounts import models as account_models
from model_bakery import baker

# def test_account_factory(account_factory):
#     assert type(account_factory) == type(AccountFactory)

# @pytest.mark.django_db
# def test_account_instance(account):
#     """Test account instance works"""
#     assert isinstance(account, Account)


@pytest.mark.django_db
def test_account_model_default_sanity():
    account = baker.make(account_models.Account)
    assert isinstance(account, account_models.Account)


@pytest.mark.django_db
def test_account_profile_model_default_sanity():
    account_profile = baker.make(account_models.AccountProfile)
    assert isinstance(account_profile, account_models.AccountProfile)
    assert isinstance(account_profile.account, account_models.Account)
