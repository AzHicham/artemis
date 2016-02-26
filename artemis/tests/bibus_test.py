from artemis import default_checker
from artemis.test_mechanism import ArtemisTestFixture, dataset, DataSet
import pytest
xfail = pytest.mark.xfail

@dataset([DataSet("bibus")])
class TestBibus(ArtemisTestFixture):
    """
    """
    def test_bibus_01(self):
        self.journey(_from="stop_area:BIB:SA:527",
                     to="stop_area:BIB:SA:9", datetime="20041214T070000",
                     datetime_represents="arrival", walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_02(self):
        self.journey(_from="stop_area:BIB:SA:336",
                     to="stop_area:BIB:SA:123", datetime="20041215T080000",
                     datetime_represents="arrival", walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_03(self):
        self.journey(_from="stop_area:BIB:SA:1202",
                     to="stop_area:BIB:SA:236", datetime="20041215T160000",
                     datetime_represents="arrival", walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_04(self):
        """
        test_bibus_03 with different walking speed
        """
        self.journey(_from="stop_area:BIB:SA:1202",
                     to="stop_area:BIB:SA:236", datetime="20041215T160000",
                     datetime_represents="arrival", walking_speed="0.75", max_duration_to_pt="1333")

    def test_bibus_05(self):
        self.journey(_from="stop_area:BIB:SA:139",
                     to="stop_area:BIB:SA:236", datetime="20041214T080000",
                     datetime_represents="arrival", walking_speed="0.75", max_duration_to_pt="1333")

    def test_bibus_06(self):
        self.journey(_from="stop_area:BIB:SA:313",
                     to="stop_area:BIB:SA:470", datetime="20041217T070000",
                     walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_07(self):
        self.journey(_from="stop_area:BIB:SA:1204",
                     to="stop_area:BIB:SA:236", datetime="20041214T080000",
                     datetime_represents="arrival", walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_08(self):
        self.journey(_from="stop_area:BIB:SA:512",
                     to="stop_area:BIB:SA:363", datetime="20041215T140000",
                     walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_09(self):
        self.journey(_from="stop_area:BIB:SA:288",
                     to="stop_area:BIB:SA:180", datetime="20041214T070000",
                     datetime_represents="arrival", walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_10(self):
        self.journey(_from="stop_area:BIB:SA:255",
                     to="stop_area:BIB:SA:470", datetime="20041216T070000",
                     walking_speed="0.83", max_duration_to_pt="1200")

    def test_bibus_11(self):
        self.journey(_from="stop_area:BIB:SA:313",
                     to="stop_area:BIB:SA:170", datetime="20050607T114200",
                     datetime_represents="arrival", walking_speed="0.83", max_duration_to_pt="1200")

    def test_v1_end_point(self):
        """
        some retro-compatibility on global API calls

        (Note no calls on /coverage, it depends on the number of instances)
        """
        self._api_call('/', response_checker=default_checker.default_checker)

    """
    Tests on different pt_ref api

    For each test we just call a collection api with a random id, and the
    retrocompatibility of the API must not be broken
    """
    def _pt_ref_call(self, collection, id, depth):
        self.api('{col}/{id}?depth={d}'.format(col=collection, id=id, d=depth))

    # for the moment, I don't know how to handle last_load_at
    # def test_coverage(self):
    #     self.api('/')

    def test_show_codes_on_stop_area(self):
        self.api('stop_areas/stop_area:BIB:SA:212?show_codes=true&depth=3')

    def test_one_stop_area_depth_1(self):
        self._pt_ref_call('stop_areas', 'stop_area:BIB:SA:212', depth=1)
    def test_one_stop_area_depth_2(self):
        self._pt_ref_call('stop_areas', 'stop_area:BIB:SA:212', depth=2)
    def test_one_stop_area_depth_3(self):
        self._pt_ref_call('stop_areas', 'stop_area:BIB:SA:212', depth=3)

    def test_one_stop_point_depth_1(self):
        self._pt_ref_call('stop_points', 'stop_point:BIB:SP:Nav504', depth=1)
    def test_one_stop_point_depth_2(self):
        self._pt_ref_call('stop_points', 'stop_point:BIB:SP:Nav504', depth=2)
    def test_one_stop_point_depth_3(self):
        self._pt_ref_call('stop_points', 'stop_point:BIB:SP:Nav504', depth=3)

    def test_one_network_depth_1(self):
        self._pt_ref_call('networks', 'network:BIB:1001', depth=1)
    def test_one_network_depth_2(self):
        self._pt_ref_call('networks', 'network:BIB:1001', depth=2)
    def test_one_network_depth_3(self):
        self._pt_ref_call('networks', 'network:BIB:1001', depth=3)

    def test_one_route_depth_1(self):
        self._pt_ref_call('routes', 'route:BIB:Nav2092', depth=1)
    def test_one_route_depth_2(self):
        self._pt_ref_call('routes', 'route:BIB:Nav2092', depth=2)
    @xfail(reason="there is some instability on the order of the stoparea list", raises=AssertionError)
    def test_one_route_depth_3(self):
        self._pt_ref_call('routes', 'route:BIB:Nav2092', depth=3)

    def test_one_company_depth_1(self):
        self._pt_ref_call('companies', 'company:default_company', depth=1)
    def test_one_company_depth_2(self):
        self._pt_ref_call('companies', 'company:default_company', depth=2)
    def test_one_company_depth_3(self):
        self._pt_ref_call('companies', 'company:default_company', depth=3)

    def test_one_line_depth_1(self):
        self._pt_ref_call('lines', 'line:BIB:Nav1', depth=1)
    def test_one_line_depth_2(self):
        self._pt_ref_call('lines', 'line:BIB:Nav1', depth=2)
    def test_one_line_depth_3(self):
        self._pt_ref_call('lines', 'line:BIB:Nav1', depth=3)

    @xfail(reason="we need to filter journey pattern name, we can depend on some order, and we don't care", raises=AssertionError)
    def test_one_vj_depth_1(self):
        self._pt_ref_call('vehicle_journeys', 'vehicle_journey:BIBNUIT:44_dst_1', depth=1)
    @xfail(reason="we need to filter journey pattern name, we can depend on some order, and we don't care", raises=AssertionError)
    def test_one_vj_depth_2(self):
        self._pt_ref_call('vehicle_journeys', 'vehicle_journey:BIBNUIT:44_dst_1', depth=2)
    @xfail(reason="we need to filter journey pattern name, we can depend on some order, and we don't care", raises=AssertionError)
    def test_one_vj_depth_3(self):
        self._pt_ref_call('vehicle_journeys', 'vehicle_journey:BIBNUIT:44_dst_1', depth=3)

    def test_one_physical_mode_depth_1(self):
        self._pt_ref_call('physical_modes', 'physical_mode:Bus', depth=1)
    def test_one_physical_mode_depth_2(self):
        self._pt_ref_call('physical_modes', 'physical_mode:Bus', depth=2)
    def test_one_physical_mode_depth_3(self):
        self._pt_ref_call('physical_modes', 'physical_mode:Bus', depth=3)

    def test_one_commercial_mode_depth_1(self):
        self._pt_ref_call('commercial_modes', 'commercial_mode:bus', depth=1)
    def test_one_commercial_mode_depth_2(self):
        self._pt_ref_call('commercial_modes', 'commercial_mode:bus', depth=2)
    def test_one_commercial_mode_depth_3(self):
        self._pt_ref_call('commercial_modes', 'commercial_mode:bus', depth=3)

    def test_one_dataset_depth_1(self):
        self._pt_ref_call('datasets', 'default_dataset:BIB', depth=1)
    def test_one_dataset_depth_2(self):
        self._pt_ref_call('datasets', 'default_dataset:BIB', depth=2)
    def test_one_dataset_depth_3(self):
        self._pt_ref_call('datasets', 'default_dataset:BIB', depth=3)

    def test_one_contributor_depth_1(self):
        self._pt_ref_call('contributors', 'BIB', depth=1)
    def test_one_contributor_depth_2(self):
        self._pt_ref_call('contributors', 'BIB', depth=2)
    def test_one_contributor_depth_3(self):
        self._pt_ref_call('contributors', 'BIB', depth=3)

    """
    Other retrocompat' on API
    """
    @xfail(reason="there is some instability on the 'quality' field", raises=AssertionError)
    def test_autocomplete(self):
        self.api('places?q=jaures')

    def test_geoloc(self):
        self.api('coords/-4.487201604;48.38987538')

    def test_place_nearby(self):
        self.api('stop_areas/stop_area:BIB:SA:212/places_nearby')

    def test_stop_schedule(self):
        self.api('stop_areas/stop_area:BIB:SA:212/stop_schedules?from_datetime=20041002T080000')

    def test_route_schedule(self):
        self.api('routes/route:BIB:Nav2092/route_schedules?from_datetime=20041104T080000')

    def test_departures(self):
        self.api('stop_areas/stop_area:BIB:SA:212/departures?from_datetime=20041106T100000')

    def test_arrivals(self):
        self.api('stop_areas/stop_area:BIB:SA:212/arrivals?from_datetime=20041106T100000')
