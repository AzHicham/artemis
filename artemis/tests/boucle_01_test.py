from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.Boucle01
@dataset([DataSet("boucle-01")])
class Boucle01(object):
    """
    TODO: put there comments about the dataset
    """

    def test_boucle_01_01(self):
        self.journey(
            _from="stop_area:BC1:SA:1",
            to="stop_area:BC1:SA:6",
            datetime="20041213T0730",
        )

    def test_boucle_01_02(self):
        self.journey(
            _from="stop_area:BC1:SA:3",
            to="stop_area:BC1:SA:7",
            datetime="20041213T0730",
            max_duration_to_pt=100,
        )

    def test_boucle_01_03(self):
        self.journey(
            _from="stop_area:BC1:SA:8",
            to="stop_area:BC1:SA:5",
            datetime="20041213T0730",
        )


class TestBoucle01Experimental(Boucle01, ArtemisTestFixture):
    pass
