from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.Poitiers
@dataset([DataSet("poitiers")])
class Poitiers(object):
    """
    """

    def test_poitiers_01(self):
        """
        ID artemis v1: 3
        """
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10046",
            datetime="20091117T070000",
            walking_speed="0.83",
            max_duration_to_pt="240",
        )

    def test_poitiers_02(self):
        """
        ID artemis v1: 4
        """
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10046",
            datetime="20091116T235000",
            walking_speed="0.83",
            max_duration_to_pt="1800",
        )

    def test_poitiers_03(self):
        """
        ID artemis v1: 5
        """
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10046",
            datetime="20091116T225000",
            walking_speed="0.83",
            max_duration_to_pt="1800",
        )

    def test_poitiers_04(self):
        """
        ID artemis v1: 6
        """
        # depending on the projection, walking can be a little more than 30min
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10046",
            datetime="20091116T002000",
            walking_speed="0.83",
            max_duration_to_pt="2100",
        )

    def test_poitiers_05(self):
        """
        ID artemis v1: 7
        """
        # depending on the projection, walking can be a little more than 30min
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10046",
            datetime="20091117T002000",
            walking_speed="0.83",
            max_duration_to_pt="2100",
        )

    def test_poitiers_06(self):
        """
        ID artemis v1: 8
        """
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10046",
            datetime="20091114T002000",
            walking_speed="0.83",
            max_duration_to_pt="1800",
        )

    def test_poitiers_07(self):
        """
        ID artemis v1: 12
        """
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10114",
            datetime="20090906T070000",
            walking_speed="0.83",
            max_duration_to_pt="240",
        )

    def test_poitiers_08(self):
        """
        ID artemis v1: 13
        """
        self.journey(
            _from="stop_area:POI:SA:10001",
            to="stop_area:POI:SA:10114",
            datetime="20091007T180000",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )


class TestPoitiersExperimental(Poitiers, ArtemisTestFixture):
    pass
