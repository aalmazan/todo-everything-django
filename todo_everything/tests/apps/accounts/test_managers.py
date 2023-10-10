from unittest import mock

import hypothesis.strategies as st
import pytest
from django.db.models.signals import post_save, pre_save
from hypothesis import given
from hypothesis.extra.django import TestCase as HypothesisTestCase

from todo_everything.apps.accounts.models import Account


@pytest.fixture(autouse=True)  # Automatically use in tests.
def mute_signals(request):
    post_save.receivers = []
    pre_save.receivers = []


class AccountManagerTestCase(HypothesisTestCase):
    """
    Test case for AccountManager.

    Extends `hypothesis` library to test input values.
    """

    @given(st.emails())
    def test_create_user_valid(self, email):
        """Test create_user with valid options."""
        with mock.patch(
            "todo_everything.apps.accounts.managers.AccountManager._create_user"
        ) as mock_create_user:
            Account.objects.create_user(email)

        assert mock_create_user.call_count == 1

    @given(st.emails())
    def test_create_superuser_valid(self, email):
        """Test create_user with valid options."""
        with mock.patch(
            "todo_everything.apps.accounts.managers.AccountManager._create_user"
        ) as mock_create_user:
            Account.objects.create_superuser(email, "some-password")

        assert mock_create_user.call_count == 1
