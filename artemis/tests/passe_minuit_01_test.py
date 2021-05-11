from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.PasseMinuit01
@dataset([DataSet("passe-minuit-01")])
class PasseMinuit01(object):
    """
    test journeys over midnight
    """

    def test_passe_minuit_01_01(self):
        self.journey(
            _from="stop_area:PM1:SA:1",
            to="stop_area:PM1:SA:3",
            datetime="20051123T230000",
        )

    def test_passe_minuit_01_02(self):
        self.journey(
            _from="stop_area:PM1:SA:1",
            to="stop_area:PM1:SA:3",
            datetime="20051124T233000",
        )

    def test_passe_minuit_01_03(self):
        self.journey(
            _from="stop_area:PM1:SA:1",
            to="stop_area:PM1:SA:4",
            datetime="20051124T070000",
            datetime_represents="arrival",
        )

    def test_passe_minuit_01_04(self):
        self.journey(
            _from="stop_area:PM1:SA:1",
            to="stop_area:PM1:SA:3",
            datetime="20051129T230000",
        )

    def test_passe_minuit_01_05(self):
        self.journey(
            _from="stop_area:PM1:SA:1",
            to="stop_area:PM1:SA:4",
            datetime="20051124T070000",
            datetime_represents="arrival",
        )


@set_scenario({"passe-minuit-01": {"scenario": "experimental"}})
class TestPasseMinuit01Experimental(PasseMinuit01, ArtemisTestFixture):
    pass
