from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.ArtTest03
@dataset([DataSet("test-03")])
class ArtTest03(object):
    """
    TODO: put there comments about the dataset
    """

    def test_art_test_03_01(self):
        self.journey(
            _from="stop_area:TS3:SA:1",
            to="stop_area:TS3:SA:6",
            datetime="20041214T0700",
        )


class TestTest03Experimental(ArtTest03, ArtemisTestFixture):
    pass
