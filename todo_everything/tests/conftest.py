import pytest


@pytest.fixture(autouse=True)
def mock_celery_delay(mocker):
    mocker.patch("celery.app.task.Task.delay", return_value=1)
    mocker.patch("celery.app.task.Task.apply_async", return_value=1)
