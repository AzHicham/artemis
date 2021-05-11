from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest

xfail = pytest.mark.xfail


@pytest.mark.Sherbrooke
@dataset([DataSet("sherbrooke")])
class Sherbrooke(object):
    def test_sherbrooke_01(self):
        self.journey(
            _from="stop_area:STS:SA:387",
            to="poi:3815 - ADDRESS370 - ADDRESS1126",
            datetime="20111116T070000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_02(self):
        self.journey(
            _from="poi:3713 - ADDRESS370 - ADDRESS1079",
            to="poi:3534 - ADDRESS968 - ADDRESS970",
            datetime="20111112T133000",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_03(self):
        self.journey(
            _from="poi:3534 - ADDRESS968 - ADDRESS970",
            to="poi:3713 - ADDRESS370 - ADDRESS1079",
            datetime="20111112T151500",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_04(self):
        self.journey(
            _from="stop_area:STS:SA:501",
            to="poi:3624 - ADDRESS962 - ADDRESS1013",
            datetime="20111111T063000",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_05(self):
        self.journey(
            _from="stop_area:STS:SA:501",
            to="stop_area:STS:SA:16",
            datetime="20111112T135000",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_06(self):
        self.journey(
            _from="stop_area:STS:SA:501",
            to="poi:2581 - ADDRESS325 - ADDRESS614",
            datetime="20111028T081500",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_07(self):
        self.journey(
            _from="stop_area:STS:SA:501",
            to="stop_area:STS:SA:2008",
            datetime="20111105T135000",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_08(self):
        self.journey(
            _from="stop_area:STS:SA:1147",
            to="stop_area:STS:SA:1475",
            datetime="20111028T075000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_09(self):
        self.journey(
            _from="-71.95892423;45.36721098",
            to="stop_area:STS:SA:1476",
            datetime="20111116T080000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_10(self):
        self.journey(
            _from="-71.83185402499441;45.40472718160273",
            to="-71.92733380024467;45.387133244175885",
            datetime="20111118T111500",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_11(self):
        self.journey(
            _from="poi:5245 - ADDRESS512 - ADDRESS1919",
            to="poi:4107 - ADDRESS740 - ADDRESS1261",
            datetime="20111116T223000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_12(self):
        self.journey(
            _from="stop_area:STS:SA:2346",
            to="stop_area:STS:SA:2007",
            datetime="20111114T080000",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_13(self):
        self.journey(
            _from="stop_area:STS:SA:2073",
            to="stop_area:STS:SA:2079",
            datetime="20111114T091500",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_14(self):
        self.journey(
            _from="stop_area:STS:SA:298",
            to="poi:3815 - ADDRESS370 - ADDRESS1126",
            datetime="20111114T070000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_15_sp_to_sp_with_walking(self):
        self.journey(
            _from="stop_point:STS:SP:322",
            to="stop_point:STS:SP:2160",
            datetime="20111114T070000",
            walking_speed="0.83",
            max_duration_to_pt="720",
        )

    def test_sherbrooke_16_sp_to_sp_without_walking(self):
        self.journey(
            _from="stop_point:STS:SP:322",
            to="stop_point:STS:SP:2160",
            datetime="20111114T070000",
            walking_speed="0.83",
            max_duration_to_pt="0",
        )


@set_scenario({"sherbrooke": {"scenario": "experimental"}})
class TestSherbrookeExperimental(Sherbrooke, ArtemisTestFixture):
    pass
