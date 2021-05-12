from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.Rebroussement
@dataset([DataSet("rebroussement")])
class Rebroussement(object):
    """
    TODO: put there comments about the dataset
    """

    def test_rebroussement_01(self):
        self.journey(
            _from="stop_area:RBR:SA:1",
            to="stop_area:RBR:SA:6",
            datetime="20041213T0700",
        )

    def test_rebroussement_02(self):
        self.journey(
            _from="stop_area:RBR:SA:1",
            to="stop_area:RBR:SA:3",
            datetime="20041213T0900",
        )

    def test_rebroussement_03(self):
        self.journey(
            _from="stop_area:RBR:SA:1",
            to="stop_area:RBR:SA:4",
            datetime="20041213T0900",
        )

    def test_rebroussement_04(self):
        self.journey(
            _from="stop_area:RBR:SA:4",
            to="stop_area:RBR:SA:6",
            datetime="20041213T0900",
        )

    def test_rebroussement_05(self):
        self.journey(
            _from="stop_area:RBR:SA:3",
            to="stop_area:RBR:SA:6",
            datetime="20041213T0900",
        )

    def test_rebroussement_06(self):
        self.journey(
            _from="stop_area:RBR:SA:3",
            to="stop_area:RBR:SA:4",
            datetime="20041213T0900",
        )

    def test_rebroussement_07(self):
        self.journey(
            _from="stop_area:RBR:SA:1",
            to="stop_area:RBR:SA:7",
            datetime="20041213T0900",
        )

    def test_rebroussement_08(self):
        self.journey(
            _from="stop_area:RBR:SA:4",
            to="stop_area:RBR:SA:7",
            datetime="20041213T0900",
        )


class TestRebroussementExperimental(Rebroussement, ArtemisTestFixture):
    pass
