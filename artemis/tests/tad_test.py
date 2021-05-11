from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.Tad
@dataset([DataSet("tad")])
class Tad(object):
    """
    On demand transport tests
    """

    """
    City to City
        > In this case, these are the frequencies that are used
    """

    def test_city_2_city(self):
        self.journey(
            _from="admin:fr:41246", to="admin:fr:41266", datetime="20150302T102000"
        )

    # to is a coord in admin : admin:fr:41266
    def test_city_2_coord(self):
        self.journey(
            _from="admin:fr:41246", to="1.2453;47.4713", datetime="20150302T102000"
        )

    # _from is a coord in admin : admin:fr:41246
    def test_coord_2_city(self):
        self.journey(
            _from="1.3379;47.5096", to="admin:fr:41266", datetime="20150302T102000"
        )

    # _from is a coord in admin : admin:fr:41246
    # to is a coord in admin : admin:fr:41266
    def test_coord_2_coord(self):
        self.journey(
            _from="1.3379;47.5096", to="1.2453;47.4713", datetime="20150302T102000"
        )

    """
    City to Station
        > In this case, these are the frequencies that are used
    """

    def test_stop_point_2_city(self):
        self.journey(
            _from="stop_point:CAA:SP:blr2",
            to="admin:fr:41212",
            datetime="20150310T102000",
        )

    def test_stop_area_2_city(self):
        self.journey(
            _from="stop_area:CAA:SA:blr2",
            to="admin:fr:41212",
            datetime="20150310T102000",
        )

    # to is a coord in admin : admin:fr:41212
    def test_stop_point_2_coord(self):
        self.journey(
            _from="stop_point:CAA:SP:blr2",
            to="1.3573;47.5564",
            datetime="20150310T102000",
        )

    # to is a coord in admin : admin:fr:41212
    def test_stop_area_2_coord(self):
        self.journey(
            _from="stop_area:CAA:SA:blr2",
            to="1.3573;47.5564",
            datetime="20150310T102000",
        )

    def test_city_2_stop_point(self):
        self.journey(
            _from="admin:fr:41212",
            to="stop_point:CAA:SP:blr2",
            datetime="20150310T102000",
        )

    def test_city_2_stop_area(self):
        self.journey(
            _from="admin:fr:41212",
            to="stop_area:CAA:SA:blr2",
            datetime="20150310T102000",
        )

    # _from is a coord in admin : admin:fr:41212
    def test_coord_2_stop_point(self):
        self.journey(
            _from="1.3573;47.5564",
            to="stop_point:CAA:SP:blr2",
            datetime="20150310T102000",
        )

    # _from is a coord in admin : admin:fr:41212
    def test_coord_2_stop_area(self):
        self.journey(
            _from="1.3573;47.5564",
            to="stop_area:CAA:SA:blr2",
            datetime="20150310T102000",
        )

    """
    City to Station
        > Departure from station with time fixed
            > From the station to the city, it is the frequency that is used
            > From the city to the station, it is the fixed time that is used
    """

    def test_stop_point_2_city_dep_after(self):
        self.journey(
            _from="stop_point:CA2:SP:blr1",
            to="admin:fr:41295",
            datetime="20150313T102000",
        )

    def test_stop_area_2_city_dep_after(self):
        self.journey(
            _from="stop_area:CA2:SA:blr1",
            to="admin:fr:41295",
            datetime="20150313T102000",
        )

    # to is a coord in admin : admin:fr:41295
    def test_stop_point_2_coord_dep_after(self):
        self.journey(
            _from="stop_point:CA2:SP:blr1",
            to="1.3828;47.5831",
            datetime="20150313T102000",
        )

    def test_stop_area_2_coord_dep_after(self):
        self.journey(
            _from="stop_area:CA2:SA:blr1",
            to="1.3828;47.5831",
            datetime="20150313T102000",
        )

    def test_city_2_stop_point_dep_after(self):
        self.journey(
            _from="admin:fr:41295",
            to="stop_point:CA2:SP:blr1",
            datetime="20150313T102000",
        )

    def test_city_2_stop_area_dep_after(self):
        self.journey(
            _from="admin:fr:41212",
            to="stop_area:CA2:SA:blr1",
            datetime="20150313T102000",
        )

    # _from is a coord in admin : admin:fr:41295
    def test_coord_2_stop_point_dep_after(self):
        self.journey(
            _from="1.3828;47.5831",
            to="stop_point:CA2:SP:blr1",
            datetime="20150313T102000",
        )

    # _from is a coord in admin : admin:fr:41295
    def test_coord_2_stop_area_dep_after(self):
        self.journey(
            _from="1.3828;47.5831",
            to="stop_area:CA2:SA:blr1",
            datetime="20150313T102000",
        )

    """
    City to Station
        >Arrival in station with time fixed
            > From the station to the city, it is the fixed time that is used
            > From the city to the station, it is the frequency that is used
    """

    def test_stop_point_2_city_arr_before(self):
        self.journey(
            _from="stop_point:CA1:SP:blr9",
            to="admin:fr:41047",
            datetime="20150319T102000",
        )

    def test_stop_area_2_city_arr_before(self):
        self.journey(
            _from="stop_area:CA1:SA:blr9",
            to="admin:fr:41047",
            datetime="20150319T102000",
        )

    # to is a coord in admin : admin:fr:41047
    def test_stop_point_2_coord_arr_before(self):
        self.journey(
            _from="stop_point:CA1:SP:blr9",
            to="1.3561;47.6089",
            datetime="20150319T102000",
        )

    # to is a coord in admin : admin:fr:41047
    def test_stop_area_2_coord_arr_before(self):
        self.journey(
            _from="stop_area:CA1:SA:blr9",
            to="1.3561;47.6089",
            datetime="20150319T102000",
        )

    def test_city_2_stop_point_arr_before(self):
        self.journey(
            _from="admin:fr:41047",
            to="stop_point:CA1:SP:blr9",
            datetime="20150319T102000",
        )

    def test_city_2_stop_area_arr_before(self):
        self.journey(
            _from="admin:fr:41047",
            to="stop_area:CA1:SA:blr9",
            datetime="20150319T102000",
        )

    # _from is a coord in admin : admin:fr:41047
    def test_coord_2_stop_point_arr_before(self):
        self.journey(
            _from="1.3561;47.6089",
            to="stop_point:CA1:SP:blr9",
            datetime="20150319T102000",
        )

    # _from is a coord in admin : admin:fr:41047
    def test_coord_2_stop_area_arr_before(self):
        self.journey(
            _from="1.3561;47.6089",
            to="stop_area:CA1:SA:blr9",
            datetime="20150319T102000",
        )

    """
    City to Station
        >Arrival in station with hour fixed
        >Departure from station with hour fixed
            > From the station to the city, it is the fixed time that is used
            > From the city to the station, it is the fixed time that is used
    """

    def test_stop_point_2_city_arr_dep(self):
        self.journey(
            _from="stop_point:CA3:SP:blr9",
            to="admin:fr:41295",
            datetime="20150407T102000",
        )

    def test_stop_area_2_city_arr_dep(self):
        self.journey(
            _from="stop_area:CA3:SA:blr9",
            to="admin:fr:41295",
            datetime="20150407T102000",
        )

    # to is a coord in admin : admin:fr:41295
    def test_stop_point_2_coord_arr_dep(self):
        self.journey(
            _from="stop_point:CA3:SP:blr9",
            to="1.3828;47.5831",
            datetime="20150407T102000",
        )

    # to is a coord in admin : admin:fr:41295
    def test_stop_area_2_coord_arr_dep(self):
        self.journey(
            _from="stop_area:CA3:SA:blr9",
            to="1.3828;47.5831",
            datetime="20150407T102000",
        )

    def test_city_2_stop_point_arr_dep(self):
        self.journey(
            _from="admin:fr:41295",
            to="stop_point:CA3:SP:blr9",
            datetime="20150407T102000",
        )

    def test_city_2_stop_area_arr_dep(self):
        self.journey(
            _from="admin:fr:41295",
            to="stop_area:CA3:SA:blr9",
            datetime="20150407T102000",
        )

    # _from is a coord in admin : admin:fr:41295
    def test_coord_2_stop_point_arr_dep(self):
        self.journey(
            _from="1.3828;47.5831",
            to="stop_point:CA3:SP:blr9",
            datetime="20150407T102000",
        )

    # _from is a coord in admin : admin:fr:41295
    def test_coord_2_stop_area_arr_dep(self):
        self.journey(
            _from="1.3828;47.5831",
            to="stop_area:CA3:SA:blr9",
            datetime="20150407T102000",
        )


@set_scenario({"tad": {"scenario": "experimental"}})
class TestTadExperimental(Tad, ArtemisTestFixture):
    pass
