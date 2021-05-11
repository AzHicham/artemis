from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.FreqParis
@dataset([DataSet("freqparis")])
class FreqParis(object):
    """
    TODO: put there comments about the dataset
    """

    def test_freqparis_01(self):
        self.journey(
            _from="stop_area:FQP:SA:defen",
            to="stop_area:FQP:SA:grest",
            datetime="20090922T0700",
        )

    def test_freqparis_02(self):
        self.journey(
            _from="stop_area:FQP:SA:defen",
            to="stop_area:FQP:SA:grest",
            datetime="20090922T2330",
        )

    def test_freqparis_03(self):
        self.journey(
            _from="stop_area:FQP:SA:defen",
            to="stop_area:FQP:SA:grest",
            datetime="20090922T2200",
        )

    def test_freqparis_04(self):
        self.journey(
            _from="stop_area:FQP:SA:defen",
            to="stop_area:FQP:SA:grest",
            datetime="20090922T0008",
            datetime_represents="arrival",
        )

    def test_freqparis_05(self):
        self.journey(
            _from="stop_area:FQP:SA:defen",
            to="stop_area:FQP:SA:grest",
            datetime="20090922T0020",
            datetime_represents="arrival",
        )

    def test_freqparis_06(self):
        self.journey(
            _from="stop_area:FQP:SA:defen",
            to="stop_area:FQP:SA:grest",
            datetime="20090922T2350",
        )

    def test_freqparis_07(self):
        self.journey(
            _from="stop_area:FQP:SA:defen",
            to="stop_area:FQP:SA:grest",
            datetime="20090922T2355",
        )


class TestFreqParisExperimental(FreqParis, ArtemisTestFixture):
    pass
