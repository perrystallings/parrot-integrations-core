from datetime import datetime

import pytest

from parrot_integrations.common.crontab import process as process_crontab


@pytest.fixture(scope='session')
def cron_expression():
    expression = '0 5 1 * *'
    return expression


def test_valid_crontab(cron_expression):
    inputs = dict(
        current_ts=datetime(year=2024, month=1, day=1, hour=5, minute=0, second=0, microsecond=0),
        expression=cron_expression
    )
    res = process_crontab(inputs=inputs)
    assert isinstance(res, dict)


def test_invalid_crontab(cron_expression):
    inputs = dict(
        current_ts=datetime(year=2024, month=10, day=12, hour=5, minute=0, second=0, microsecond=0),
        expression=cron_expression
    )
    res = process_crontab(inputs=inputs)
    assert res is None
