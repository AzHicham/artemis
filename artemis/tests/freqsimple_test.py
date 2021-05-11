from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.FreqSimple
@dataset([DataSet("freqsimple")])
class FreqSimple(object):
    """
    TODO: put there comments about the dataset
    """

    def test_freqsimple_01(self):
        self.journey(
            _from="stop_area:FQS:SA:GRA",
            to="stop_area:FQS:SA:MBC",
            datetime="20070417T0540",
        )

    def test_freqsimple_02(self):
        self.journey(
            _from="stop_area:FQS:SA:GRA",
            to="stop_area:FQS:SA:MBC",
            datetime="20070417T0500",
        )

    def test_freqsimple_03(self):
        self.journey(
            _from="stop_area:FQS:SA:MBC",
            to="stop_area:FQS:SA:GRA",
            datetime="20070417T0100",
        )

    def test_freqsimple_04(self):
        self.journey(
            _from="stop_area:FQS:SA:MBC",
            to="stop_area:FQS:SA:GRA",
            datetime="20070417T0520",
            datetime_represents="arrival",
        )

    def test_freqsimple_05(self):
        self.journey(
            _from="stop_area:FQS:SA:MBC",
            to="stop_area:FQS:SA:GRA",
            datetime="20070417T0550",
            datetime_represents="arrival",
        )


@set_scenario({"freqsimple": {"scenario": "experimental"}})
class TestFreqSimpleExperimental(FreqSimple, ArtemisTestFixture):
    pass
