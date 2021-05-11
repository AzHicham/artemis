from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.Mission
@dataset([DataSet("mission")])
class Mission(object):
    """
    TODO: put there comments about the dataset
    """

    def test_mission_01(self):
        self.journey(
            _from="stop_area:MIS:SA:1",
            to="stop_area:MIS:SA:5",
            datetime="20041210T090000",
        )

    def test_mission_02(self):
        self.journey(
            _from="stop_area:MIS:SA:1",
            to="stop_area:MIS:SA:7",
            datetime="20041210T090000",
        )

    def test_mission_03(self):
        self.journey(
            _from="stop_area:MIS:SA:1",
            to="stop_area:MIS:SA:8",
            datetime="20041210T090000",
        )

    def test_mission_04(self):
        self.journey(
            _from="stop_area:MIS:SA:1",
            to="stop_area:MIS:SA:12",
            datetime="20041210T090000",
        )

    def test_mission_05(self):
        self.journey(
            _from="stop_area:MIS:SA:3",
            to="stop_area:MIS:SA:12",
            datetime="20041210T090000",
        )

    def test_mission_06(self):
        self.journey(
            _from="stop_area:MIS:SA:3",
            to="stop_area:MIS:SA:9",
            datetime="20041210T090000",
        )

    def test_mission_07(self):
        self.journey(
            _from="stop_area:MIS:SA:6",
            to="stop_area:MIS:SA:9",
            datetime="20041210T090000",
        )

    def test_mission_08(self):
        self.journey(
            _from="stop_area:MIS:SA:1",
            to="stop_area:MIS:SA:4",
            datetime="20041210T070000",
        )


@set_scenario({"mission": {"scenario": "experimental"}})
class TestMissionExperimental(Mission, ArtemisTestFixture):
    pass
