from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest

xfail = pytest.mark.xfail


@pytest.mark.Airport1
@dataset([DataSet("airport-01")])
class Airport1(object):
    """
    TODO: put there comments about the dataset
    """

    def test_airport_01_01(self):
        self.journey(
            _from="stop_area:AI1:SA:AIRPORTAIRPORT",
            to="stop_area:AI1:SA:AIRPORTLYS",
            datetime="20120904T0700",
        )

    def test_airport_01_02(self):
        self.journey(
            _from="stop_area:AI1:SA:AIRPORTAMS",
            to="stop_area:AI1:SA:AIRPORTAIRPORT",
            datetime="20120904T0900",
        )

    def test_airport_01_03(self):
        self.journey(
            _from="stop_area:AI1:SA:AIRPORTAIRPORT",
            to="stop_area:AI1:SA:AIRPORTCLY",
            datetime="20120908T1000",
        )

    def test_airport_01_04(self):
        self.journey(
            _from="stop_area:AI1:SA:AIRPORTAIRPORT",
            to="stop_area:AI1:SA:AIRPORTMRS",
            datetime="20120908T1200",
        )


@set_scenario({"airport-01": {"scenario": "experimental"}})
class TestAirport1Experimental(Airport1, ArtemisTestFixture):
    pass
