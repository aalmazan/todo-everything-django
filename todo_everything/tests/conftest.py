import pytest
from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
    pre_delete,
    pre_save,
)
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture(autouse=True)
def api_factory():
    return APIRequestFactory()


@pytest.fixture(autouse=True)
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def mock_celery_delay(mocker):
    mocker.patch("celery.app.task.Task.delay", return_value=1)
    mocker.patch("celery.app.task.Task.apply_async", return_value=1)


@pytest.fixture(scope="session", autouse=True)
def mute_signals(request):
    # Skip applying, if marked with `enabled_signals`
    if "enable_signals" in request.keywords:
        return

    signals = [pre_save, post_save, pre_delete, post_delete, m2m_changed]
    restore = {}
    for signal in signals:
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals():
        for signal, receivers in restore.items():
            signal.sender_receivers_cache.clear()
            signal.receivers = receivers

    request.addfinalizer(restore_signals)
