import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):  # pylint: disable=W0613,W0621
    with django_db_blocker.unblock():
        call_command("loaddata", "tests/fixtures/master_datas.jsonl")
        call_command("loaddata", "tests/fixtures/code_datas.jsonl")
