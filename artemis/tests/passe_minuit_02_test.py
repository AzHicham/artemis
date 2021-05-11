from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.PasseMinuit02
@dataset([DataSet("passe-minuit-02")])
class PasseMinuit02(object):
    """
    TODO: put there comments about the dataset
    """

    def test_passe_minuit_02_01(self):
        self.journey(
            _from="stop_area:PM2:SA:1",
            to="stop_area:PM2:SA:2",
            datetime="20080310T2300",
        )

    def test_passe_minuit_02_02(self):
        self.journey(
            _from="stop_area:PM2:SA:1",
            to="stop_area:PM2:SA:4",
            datetime="20080310T2300",
        )

    def test_passe_minuit_02_03(self):
        """
        no solution found for this journey because first itinerary available is 2 days later
        """
        self.journey(
            _from="stop_area:PM2:SA:2",
            to="stop_area:PM2:SA:4",
            datetime="20080310T0000",
        )

    def test_passe_minuit_02_04(self):
        self.journey(
            _from="stop_area:PM2:SA:2",
            to="stop_area:PM2:SA:4",
            datetime="20080311T0000",
        )

    def test_passe_minuit_02_05(self):
        self.journey(
            _from="stop_area:PM2:SA:2",
            to="stop_area:PM2:SA:4",
            datetime="20080310T2350",
        )

    def test_passe_minuit_02_06(self):
        self.journey(
            _from="stop_area:PM2:SA:2",
            to="stop_area:PM2:SA:4",
            datetime="20080311T0040",
            datetime_represents="arrival",
        )

    def test_passe_minuit_02_07(self):
        self.journey(
            _from="stop_area:PM2:SA:1",
            to="stop_area:PM2:SA:4",
            datetime="20080311T0040",
            datetime_represents="arrival",
        )

    def test_passe_minuit_02_08(self):
        self.journey(
            _from="stop_area:PM2:SA:2",
            to="stop_area:PM2:SA:4",
            datetime="20080408T0006",
        )

    def test_passe_minuit_02_09(self):
        self.journey(
            _from="stop_area:PM2:SA:1",
            to="stop_area:PM2:SA:2",
            datetime="20080408T0011",
            datetime_represents="arrival",
        )

    def test_passe_minuit_02_10(self):
        self.journey(
            _from="stop_area:PM2:SA:1",
            to="stop_area:PM2:SA:4",
            datetime="20080407T2340",
        )

    def test_passe_minuit_02_11(self):
        self.journey(
            _from="stop_area:PM2:SA:5",
            to="stop_area:PM2:SA:6",
            datetime="20080407T2250",
        )

    def test_passe_minuit_02_12(self):
        self.journey(
            _from="stop_area:PM2:SA:5",
            to="stop_area:PM2:SA:6",
            datetime="20080408T0040",
            datetime_represents="arrival",
        )

    def test_passe_minuit_02_13(self):
        self.journey(
            _from="stop_area:PM2:SA:5",
            to="stop_area:PM2:SA:6",
            datetime="20080408T0055",
            datetime_represents="arrival",
        )


class TestPasseMinuit02Experimental(PasseMinuit02, ArtemisTestFixture):
    pass
