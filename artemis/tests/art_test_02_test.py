from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.ArtTest02
@dataset([DataSet("test-02")])
class ArtTest02(object):
    """
    TODO: put there comments about the dataset
    """

    def test_art_test_02_01(self):
        self.journey(
            _from="stop_area:TS2:SA:1",
            to="stop_area:TS2:SA:2",
            datetime="20041214T1100",
        )

    def test_art_test_02_02(self):
        self.journey(
            _from="stop_area:TS2:SA:1",
            to="stop_area:TS2:SA:3",
            datetime="20041214T1105",
        )

    def test_art_test_02_03(self):
        self.journey(
            _from="stop_area:TS2:SA:1",
            to="stop_area:TS2:SA:4",
            datetime="20041214T0700",
        )

    def test_art_test_02_04(self):
        self.journey(
            _from="stop_area:TS2:SA:3",
            to="stop_area:TS2:SA:4",
            datetime="20041214T0700",
        )


class TestArtTest02Experimental(ArtTest02, ArtemisTestFixture):
    pass
