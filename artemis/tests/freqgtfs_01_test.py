from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.FreqGtfs_01
@dataset([DataSet("freqgtfs-01")])
class FreqGtfs_01(object):
    """
    test frequencies to stops serialisation by FUSiO
    """

    def test_freqgtfs_01_01(self):
        self.journey(
            _from="stop_area:FQT:SA:1374208",
            to="stop_area:FQT:SA:211435",
            datetime="20120905T062000",
        )

    def test_freqgtfs_01_02(self):
        self.journey(
            _from="stop_area:FQT:SA:527405",
            to="stop_area:FQT:SA:1344488",
            datetime="20120820T170000",
        )

    def test_freqgtfs_01_03(self):
        self.journey(
            _from="stop_area:FQT:SA:215949",
            to="stop_area:FQT:SA:212127",
            datetime="20121110T070000",
        )

    def test_freqgtfs_01_04(self):
        self.journey(
            _from="stop_area:FQT:SA:212127",
            to="stop_area:FQT:SA:215949",
            datetime="20121110T070000",
        )

    def test_freqgtfs_01_05(self):
        self.journey(
            _from="stop_area:FQT:SA:210216",
            to="stop_area:FQT:SA:211020",
            datetime="20120923T094000",
        )

    def test_freqgtfs_01_06(self):
        self.journey(
            _from="stop_area:FQT:SA:527405",
            to="stop_area:FQT:SA:1374208",
            datetime="20120822T192900",
        )


@set_scenario({"freqgtfs-01": {"scenario": "experimental"}})
class TestFreqGtfs_01Experimental(FreqGtfs_01, ArtemisTestFixture):
    pass
