from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.ArtTest01
@dataset([DataSet("test-01")])
class ArtTest01(object):
    """
    TODO: put there comments about the dataset
    """

    def test_art_test_01_01(self):
        self.journey(
            _from="stop_area:TS1:SA:2",
            to="stop_area:TS1:SA:6",
            datetime="20041214T0700",
        )

    def test_art_test_01_02(self):
        self.journey(
            _from="stop_area:TS1:SA:10",
            to="stop_area:TS1:SA:12",
            datetime="20041214T0700",
        )


@set_scenario({"test-01": {"scenario": "experimental"}})
class TestTadExperimental(ArtTest01, ArtemisTestFixture):
    pass
