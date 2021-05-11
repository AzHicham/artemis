from artemis import default_checker
from artemis.default_checker import stop_schedule_checker
from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest

xfail = pytest.mark.xfail


@pytest.mark.Bibus
@dataset([DataSet("bibus")])
class Bibus(object):
    """
    """

    def test_bibus_01(self):
        self.journey(
            _from="stop_area:BIB:SA:527",
            to="stop_area:BIB:SA:9",
            datetime="20041214T070000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_02(self):
        self.journey(
            _from="stop_area:BIB:SA:336",
            to="stop_area:BIB:SA:123",
            datetime="20041215T080000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_03(self):
        self.journey(
            _from="stop_area:BIB:SA:1202",
            to="stop_area:BIB:SA:236",
            datetime="20041215T160000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_04(self):
        """
        test_bibus_03 with different walking speed
        """
        self.journey(
            _from="stop_area:BIB:SA:1202",
            to="stop_area:BIB:SA:236",
            datetime="20041215T160000",
            datetime_represents="arrival",
            walking_speed="0.75",
            max_duration_to_pt="1333",
        )

    def test_bibus_05(self):
        self.journey(
            _from="stop_area:BIB:SA:139",
            to="stop_area:BIB:SA:236",
            datetime="20041214T080000",
            datetime_represents="arrival",
            walking_speed="0.75",
            max_duration_to_pt="1333",
        )

    def test_bibus_06(self):
        self.journey(
            _from="stop_area:BIB:SA:313",
            to="stop_area:BIB:SA:470",
            datetime="20041217T070000",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_07(self):
        self.journey(
            _from="stop_area:BIB:SA:1204",
            to="stop_area:BIB:SA:236",
            datetime="20041214T080000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_08(self):
        self.journey(
            _from="stop_area:BIB:SA:512",
            to="stop_area:BIB:SA:363",
            datetime="20041215T140000",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_09(self):
        self.journey(
            _from="stop_area:BIB:SA:288",
            to="stop_area:BIB:SA:180",
            datetime="20041214T070000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_10(self):
        self.journey(
            _from="stop_area:BIB:SA:255",
            to="stop_area:BIB:SA:470",
            datetime="20041216T070000",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_bibus_11(self):
        self.journey(
            _from="stop_area:BIB:SA:313",
            to="stop_area:BIB:SA:170",
            datetime="20050607T114200",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    """
    Tests of responses with error message.
    """

    def test_date_out_of_bound(self):
        self.journey(
            _from="stop_area:BIB:SA:527",
            to="stop_area:BIB:SA:9",
            datetime="20051214T070000",
            datetime_represents="arrival",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    # There is not any stop_point within 50 seconds of walking period from origin
    def test_no_origin(self):
        self.journey(
            _from="-4.48244;48.404277",
            to="stop_area:BIB:SA:1210",
            datetime="20041214T220000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="50",
        )

    # There is not any stop_point within 50 seconds of walking period from destination
    def test_no_destination(self):
        self.journey(
            _from="stop_area:BIB:SA:9",
            to="-4.48244;48.404277",
            datetime="20041214T220000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="50",
        )

    # There is no solution without any correspondence and with max duration of 1500 seconds
    def test_no_solution(self):
        self.journey(
            _from="stop_area:BIB:SA:9",
            to="-4.48244;48.404277",
            datetime="20041214T000000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="1200",
            max_duration="1500",
            max_transfers="0",
        )

    def test_from_unknown_object(self):
        self.journey(
            _from="stop_area:unexisting:",
            to="stop_area:BIB:SA:9",
            datetime="20041214T000000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_to_unknown_object(self):
        self.journey(
            _from="stop_area:BIB:SA:9",
            to="stop_area:unexisting:",
            datetime="20041214T000000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="1200",
        )

    def test_no_origin_nor_destination(self):
        self.journey(
            _from="-4.084801490596711;48.01533468818747",
            to="-4.080642851923755;47.97614436460814",
            datetime="20041214T000000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="1200",
            max_transfers="0",
        )

    def test_v1_end_point(self):
        """
        some retro-compatibility on global API calls

        (Note no calls on /coverage, it depends on the number of instances)
        """
        self._api_call("/", response_checker=default_checker.default_checker)

    """
    Tests on different pt_ref api

    For each test we just call a collection api with a random id, and the
    retrocompatibility of the API must not be broken
    """

    def _pt_ref_call(self, collection, id, depth):
        self.api("{col}/{id}?depth={d}".format(col=collection, id=id, d=depth))

    # for the moment, I don't know how to handle last_load_at
    # def test_coverage(self):
    #     self.api('/')

    def test_show_codes_on_stop_area(self):
        self.api("stop_areas/stop_area:BIB:SA:212?show_codes=true&depth=3")

    def test_one_stop_area_depth_1(self):
        self._pt_ref_call("stop_areas", "stop_area:BIB:SA:212", depth=1)

    def test_one_stop_area_depth_2(self):
        self._pt_ref_call("stop_areas", "stop_area:BIB:SA:212", depth=2)

    def test_one_stop_area_depth_3(self):
        self._pt_ref_call("stop_areas", "stop_area:BIB:SA:212", depth=3)

    def test_one_stop_point_depth_1(self):
        self._pt_ref_call("stop_points", "stop_point:BIB:SP:Nav504", depth=1)

    def test_one_stop_point_depth_2(self):
        self._pt_ref_call("stop_points", "stop_point:BIB:SP:Nav504", depth=2)

    def test_one_stop_point_depth_3(self):
        self._pt_ref_call("stop_points", "stop_point:BIB:SP:Nav504", depth=3)

    def test_one_network_has_code_bibus(self):
        self.api("networks?filter=network.has_code(source,bibus)")

    def test_one_network_has_code_1001(self):
        self.api("networks?filter=network.has_code(source,1001)")

    def test_one_network_has_code_rien(self):
        self.api("networks?filter=network.has_code(source,rien)")

    def test_one_network_external_code_BIB1001(self):
        self._api_call(
            "/networks?external_code=BIB1001", default_checker.default_checker
        )

    def test_one_network_external_code_BIB1006(self):
        self._api_call(
            "/networks?external_code=BIB1006", default_checker.default_checker
        )

    def test_one_network_external_code_rien(self):
        self._api_call("/networks?external_code=rien", default_checker.default_checker)

    def test_one_network_depth_1(self):
        self._pt_ref_call("networks", "network:bibus", depth=1)

    def test_one_network_depth_2(self):
        self._pt_ref_call("networks", "network:bibus", depth=2)

    def test_one_network_depth_3(self):
        self._pt_ref_call("networks", "network:bibus", depth=3)

    def test_one_route_depth_1(self):
        self._pt_ref_call("routes", "route:BIB:Nav2092", depth=1)

    def test_one_route_depth_2(self):
        self._pt_ref_call("routes", "route:BIB:Nav2092", depth=2)

    @xfail(
        reason="there is some instability on the order of the stoparea list",
        raises=AssertionError,
    )
    def test_one_route_depth_3(self):
        self._pt_ref_call("routes", "route:BIB:Nav2092", depth=3)

    def test_one_company_depth_1(self):
        self._pt_ref_call("companies", "company:default_company", depth=1)

    def test_one_company_depth_2(self):
        self._pt_ref_call("companies", "company:default_company", depth=2)

    def test_one_company_depth_3(self):
        self._pt_ref_call("companies", "company:default_company", depth=3)

    def test_one_line_depth_1(self):
        self._pt_ref_call("lines", "line:BIB:Nav1", depth=1)

    def test_one_line_depth_2(self):
        self._pt_ref_call("lines", "line:BIB:Nav1", depth=2)

    def test_one_line_depth_3(self):
        self._pt_ref_call("lines", "line:BIB:Nav1", depth=3)

    @xfail(
        reason="we need to filter journey pattern name, we can depend on some order, and we don't care",
        raises=AssertionError,
    )
    def test_one_vj_depth_1(self):
        self._pt_ref_call(
            "vehicle_journeys", "vehicle_journey:BIBNUIT:44_dst_1", depth=1
        )

    @xfail(
        reason="we need to filter journey pattern name, we can depend on some order, and we don't care",
        raises=AssertionError,
    )
    def test_one_vj_depth_2(self):
        self._pt_ref_call(
            "vehicle_journeys", "vehicle_journey:BIBNUIT:44_dst_1", depth=2
        )

    @xfail(
        reason="we need to filter journey pattern name, we can depend on some order, and we don't care",
        raises=AssertionError,
    )
    def test_one_vj_depth_3(self):
        self._pt_ref_call(
            "vehicle_journeys", "vehicle_journey:BIBNUIT:44_dst_1", depth=3
        )

    def test_one_physical_mode_depth_1(self):
        self._pt_ref_call("physical_modes", "physical_mode:Bus", depth=1)

    def test_one_physical_mode_depth_2(self):
        self._pt_ref_call("physical_modes", "physical_mode:Bus", depth=2)

    def test_one_physical_mode_depth_3(self):
        self._pt_ref_call("physical_modes", "physical_mode:Bus", depth=3)

    def test_one_commercial_mode_depth_1(self):
        self._pt_ref_call("commercial_modes", "commercial_mode:bus", depth=1)

    def test_one_commercial_mode_depth_2(self):
        self._pt_ref_call("commercial_modes", "commercial_mode:bus", depth=2)

    def test_one_commercial_mode_depth_3(self):
        self._pt_ref_call("commercial_modes", "commercial_mode:bus", depth=3)

    def test_one_dataset_depth_1(self):
        self._pt_ref_call("datasets", "BIB:0", depth=1)

    def test_one_dataset_depth_2(self):
        self._pt_ref_call("datasets", "BIB:0", depth=2)

    def test_one_dataset_depth_3(self):
        self._pt_ref_call("datasets", "BIB:0", depth=3)

    def test_one_contributor_depth_1(self):
        self._pt_ref_call("contributors", "BIB", depth=1)

    def test_one_contributor_depth_2(self):
        self._pt_ref_call("contributors", "BIB", depth=2)

    def test_one_contributor_depth_3(self):
        self._pt_ref_call("contributors", "BIB", depth=3)

    """
    Other retrocompat' on API
    """

    @xfail(
        reason="there is some instability on the 'quality' field", raises=AssertionError
    )
    def test_autocomplete(self):
        self.api("places?q=jaures")

    def test_geoloc(self):
        self.api("coords/-4.487201604;48.38987538")

    def test_place_nearby(self):
        self.api("stop_areas/stop_area:BIB:SA:212/places_nearby")

    def test_stop_schedule(self):
        self.api(
            "stop_areas/stop_area:BIB:SA:212/stop_schedules?from_datetime=20041107T080000",
            response_checker=stop_schedule_checker,
        )

    def test_route_schedule(self):
        self.api(
            "routes/route:BIB:Nav2092/route_schedules?from_datetime=20041104T080000"
        )

    def test_departures(self):
        self.api(
            "stop_areas/stop_area:BIB:SA:212/departures?from_datetime=20041106T100000"
        )

    def test_arrivals(self):
        self.api(
            "stop_areas/stop_area:BIB:SA:212/arrivals?from_datetime=20041106T100000"
        )

    def test_geo_status(self):
        """
        check geodata sources and volume
        """
        self.api("_geo_status")


@set_scenario({"bibus": {"scenario": "experimental"}})
class TestBibusExperimental(Bibus, ArtemisTestFixture):
    # There is not any stop_point within 50 seconds of walking period from origin
    def test_no_origin(self):
        self.journey(
            _from="-4.48244;48.404277",
            to="stop_area:BIB:SA:1210",
            datetime="20041214T220000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="50",
            max_walking_direct_path_duration=0,
        )

    # There is not any stop_point within 50 seconds of walking period from destination
    def test_no_destination(self):
        self.journey(
            _from="stop_area:BIB:SA:9",
            to="-4.48244;48.404277",
            datetime="20041214T220000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="50",
            max_walking_direct_path_duration=0,
        )

    # There is no solution without any correspondence and with max duration of 1500 seconds
    def test_no_solution(self):
        self.journey(
            _from="stop_area:BIB:SA:9",
            to="-4.48244;48.404277",
            datetime="20041214T000000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="1200",
            max_duration="1500",
            max_transfers="0",
            max_walking_direct_path_duration=0,
        )

    def test_no_origin_nor_destination(self):
        self.journey(
            _from="-4.084801490596711;48.01533468818747",
            to="-4.080642851923755;47.97614436460814",
            datetime="20041214T000000",
            datetime_represents="departure",
            walking_speed="0.83",
            max_duration_to_pt="1200",
            max_transfers="0",
            max_walking_direct_path_duration=0,
        )
