from artemis.common_fixture import clean_kirin_db, dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest

xfail = pytest.mark.xfail
COVERAGE = "guichet-unique"


@pytest.mark.GuichetUnique
@dataset([DataSet(COVERAGE)])
class GuichetUnique(object):
    """
    """

    @pytest.fixture(scope="function", autouse=True)
    def reload_kraken(self, clean_kirin_db_before_each_test):
        # Reload kraken
        self.kill_the_krakens()
        self.pop_krakens()

    @pytest.fixture
    def clean_kirin_db_before_each_test(self):
        return clean_kirin_db()

    def test_guichet_unique_paris_to_rouen(self):
        """
        ID artemis v1: 1
        """
        self.journey(
            _from="admin:fr:75056",
            to="admin:fr:76540",
            datetime="20121012T120000",
            walking_speed="0.83",
            max_duration_to_pt="240",
        )

    def test_guichet_unique_caen_to_brest(self):
        """
        ID artemis v1: 2
        """
        self.journey(
            _from="admin:fr:14118",
            to="admin:fr:29019",
            datetime="20121022T054500",
            walking_speed="0.83",
            max_duration_to_pt="240",
            count="7",
            type="rapid",
        )

    def test_guichet_unique_reims_to_paris(self):
        """
        ID artemis v1: 18
        """
        self.journey(
            _from="admin:fr:51454",
            to="admin:fr:75056",
            datetime="20121020T120000",
            walking_speed="0.83",
            max_duration_to_pt="240",
        )

    def test_guichet_unique_avignon_to_marseille(self):
        """
        ID artemis v1: 19
        """
        self.journey(
            _from="admin:fr:84007",
            to="admin:fr:13055",
            datetime="20120928T120000",
            walking_speed="0.83",
            max_duration_to_pt="240",
        )

    def test_guichet_unique_paris_to_avignon(self):
        """
        ID artemis v1: 20
        """
        self.journey(
            _from="admin:fr:75056",
            to="admin:fr:84007",
            datetime="20121121T120000",
            walking_speed="0.83",
            max_duration_to_pt="240",
        )

    def test_guichet_unique_paris_to_ay(self):
        """
        ID artemis v1: 21
        """
        self.journey(
            _from="admin:fr:75056",
            to="admin:fr:51030",
            datetime="20121121T120000",
            walking_speed="0.83",
            max_duration_to_pt="240",
        )

    def test_guichet_unique_paris_to_Avenay_Val_d_Or(self):
        """
        ID artemis v1: 22
        """
        self.journey(
            _from="admin:fr:75056",
            to="admin:fr:51028",
            datetime="20121025T120000",
            walking_speed="0.83",
            max_duration_to_pt="6000",
        )

    def test_too_long_waiting_filter(self):
        """
        Test a journey from saint quentin -> saint just

        The query is late, and without filter we have 2 journeys

        * One where the traveller leaves at 20h19, sleeps at Amiens and arrive in the morning (6h22)
        * One where the traveller leaves at 7h22 and arrive at 9h14

        We don't want the first journey, so it is filtered and we should only have the second one

        linked to http://jira.canaltp.fr/browse/NAVITIAII-2000
        """
        self.journey(
            _from="stop_area:OCE:SA:87296004",
            to="stop_area:OCE:SA:87313270",
            datetime="20121123T2019",
        )

    """
    test RealTime on SNCF (COTS)
    """

    def test_kirin_cots_trip_delay_then_normal(self):
        """
        Test delay on a train

        Requested departure: 2012/11/20 16:00:00
        From: gare de Strasbourg (Strasbourg)
        To: gare de Marseille-St-Charles (Marseille)

        Before the delay, the train travels from 16:12:00 to 21:46:00
        After the delay, the train travels from 16:12:00 to 22:16:00
        """
        self.send_and_wait("trip_delay_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            data_freshness="base_schedule",
        )

        # Send new feed where everything is back to normal
        # So train arrives at 21:46:00 in Marseille
        self.send_and_wait("trip_base_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_removal(self):
        """
        Test removal of a train

        Requested departure: 2012/12/16 17:30:00
        From: gare de Bordeaux-St-Jean (Bordeaux)
        To: gare de Marseille-St-Charles (Marseille)

        Before the removal, a train (headsign: 4669) travels on 2012/12/16 from 17:31:00 to 23:46:00
        After the removal, an other train (headsign: 4655) travels on 2012/12/17 from 06:45:00 to 12:59:00
        """
        self.send_and_wait("trip_removal_4669_ic.json")

        self.journey(
            _from="stop_area:OCE:SA:87581009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121216T173000",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87581009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121216T173000",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_deleted_partially(self):
        """
        Test removal of some stops of a vj

        Requested departure: 2012/11/19 12:36:00
        From: gare de Avignon-TGV (Avignon)
        To: gare de Marseille-St-Charles (Marseille)

        Before the removal of the stops, a train (headsign: 5312/5358) travels from 12:39:00 to 13:14:00
        After the removal of the departure stop, an other train (headsign: 5101) travels from 13:11:00 to 13:48:00
        """
        self.send_and_wait("trip_partially_deleted_5312_tgv.json")
        self.send_and_wait("trip_partially_deleted_5358_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87318964",
            to="stop_area:OCE:SA:87751008",
            datetime="20121119T123600",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87318964",
            to="stop_area:OCE:SA:87751008",
            datetime="20121119T123000",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_observed_delay_passe_minuit(self):
        """
        Test delay of a train which arrival is the day after the departure

        Requested departure: 2012/12/16 22:30:00
        From: gare de Paris-Nord (Paris)
        To: gare de St Quentin (Saint-Quentin)

        Before the delay, the train travels from 2012/12/16 22:37:00 to 2012/12/17 00:16:00
        After the delay, the train travels from 2012/12/16 22:37:00 to 2012/12/17 00:41:00
        """
        self.send_and_wait("trip_observed_delay_passe_minuit_847919_ter.json")

        self.journey(
            _from="stop_area:OCE:SA:87271007",
            to="stop_area:OCE:SA:87296004",
            datetime="20121216T223000",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87271007",
            to="stop_area:OCE:SA:87296004",
            datetime="20121216T223000",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_departure_delayed_pass_midnight(self):
        """
        Test delay of a train with a departure without delay before midnight,
        then a departure after midnight with the delay

        Requested departure: 2012/12/16 23:40:00
        From: gare de Noyon (Noyon)
        To: gare de St Quentin (Saint-Quentin)

        Before the delay, the train travels from 2012/12/16 23:44:00 to 2012/12/17 00:16:00
        After the delay, the train travels from 2012/12/17 00:09:00 to 2012/12/17 00:41:00
        """
        self.send_and_wait("trip_observed_delay_passe_minuit_847919_ter.json")

        self.journey(
            _from="stop_area:OCE:SA:87276782",
            to="stop_area:OCE:SA:87296004",
            datetime="20121216T234000",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87276782",
            to="stop_area:OCE:SA:87296004",
            datetime="20121216T234000",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_reload_from_scratch(self):
        """
        Test removal of a train

        Requested departure: 2012/12/16 17:30:00
        From: gare de Bordeaux-St-Jean (Bordeaux)
        To: gare de Marseille-St-Charles (Marseille)

        Before the removal, a train (headsign: 4669) travels on 2012/12/16 from 17:31:00 to 23:46:00
        After the removal, an other train (headsign: 4655) travels on 2012/12/17 from 06:45:00 to 12:59:00
        """
        self.send_and_wait("trip_delay_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            data_freshness="realtime",
        )

        """
        At this point, the COTS feed is saved into the db.
        Now, the Kraken is run from scratch and the previous COTS feed should be taken into account.
        """
        last_rt_data_loaded = self.get_last_rt_loaded_time(COVERAGE)

        self.kill_the_krakens()
        self.pop_krakens()

        self.wait_for_rt_reload(last_rt_data_loaded, COVERAGE)

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_add_new_stop_point_at_the_beginning(self):
        """
        Test add a stop_time at the departure of the vj

        Requested departure: 2012/11/20 13:30:00
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, an other train travels on 2012/11/20 from 13:30:00 to 21:46:00
        """
        self.send_and_wait("trip_add_new_stop_point_at_the_beginning_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T133000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T133000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_add_new_stop_point_in_the_middle(self):
        """
        Test add a stop_time in the middle of the vj

        Requested departure: 2012/11/20 13:58:00
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, the train travels on 2012/11/20 from 14:20:00 to 22:16:00
        """
        self.send_and_wait("trip_add_new_stop_point_9580_tgv_in_the_middle.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_add_new_stop_point_at_the_end(self):
        """
        Test add a stop_time at the end of the vj

        Requested departure: 2012/11/20 13:58:00
        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Nimes (Nimes)

        Before the addition, no solution can be found without transfer
        After the addition, the train travels on 2012/11/20 from 14:20:00 to 22:16:00
        """
        self.send_and_wait("trip_add_new_stop_point_9580_tgv_at_the_end.json")

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_remove_new_stop_point(self):
        """
        Test add a stop_time in the middle of the vj then remove it

        Requested departure: 2012/11/20 13:58:00
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, the train travels on 2012/11/20 from 14:20:00 to 22:16:00
        After the removal, no solution can be found without transfer
        """
        self.send_and_wait("trip_add_new_stop_point_9580_tgv_in_the_middle.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        # Then we send a cots feed with the previously added new_stop_time now to delete
        self.send_and_wait("trip_delete_new_stop_point_9580_tgv_in_the_middle.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_add_stop_point_at_the_beginning_then_delete_then_delay_another_stop_point(
        self
    ):
        """
        Test add a stop_time at the beginning of the vj, then we delete it, then we delay another stop_point

        In the final /disruptions, we should be able to see the deletion of the first stop_point and the delay
        """

        """
        Requested departure: 2012/11/20 13:30:00
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, an other train travels on 2012/11/20 from 13:30:00 to 21:46:00
        """
        self.send_and_wait("trip_add_new_stop_point_at_the_beginning_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T133000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T133000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        """
        Requested departure: 2012/11/20 13:30:00
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Now we delete the added stop_point, no journeys should be found in 'realtime'
        But in the /disruptions we should be able to see that the first stop_point is deleted
        """
        self.send_and_wait("trip_delete_new_stop_point_at_the_beginning_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T133000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Requested departure: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Marseille-St-Charles (Marseille)

        Now we send a delay on the arrival at Marseille St Charles
        """

        # Before sending a new cots, there is no delay
        # From: gare de Frankfurt-am-Main-Hbf at 20121120T140100
        # To: gare de Marseille-St-Charles (Marseille) at 20121120T214600
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.send_and_wait(
            "trip_delay_delete_new_stop_point_at_the_beginning_9580_tgv.json"
        )

        # From: gare de Frankfurt-am-Main-Hbf at 20121120T140100
        # To: gare de Marseille-St-Charles (Marseille) at 20121120T222600
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        # After the new cots, there is still no solution for this request
        # From:  gare de Bitche (Bitche) at 20121120T133000
        # To: gare de Marseille-St-Charles (Marseille)
        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T133000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_add_new_stop_point_several_times(self):
        """
        Test add a stop_time with the same COTS feed several times

        Requested departure: 2012/11/20 13:58:00
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, the train travels on 2012/11/20 from 14:20:00 to 22:16:00
        """
        self.send_and_wait("trip_add_new_stop_point_9580_tgv_in_the_middle.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        # Send the same COTS feed and check that the stop_time is still available
        self.send_and_wait("trip_add_new_stop_point_9580_tgv_in_the_middle.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_add_several_new_stop_points_in_one_cots(self):
        """
        Test add several stop_times in a single COTS feed:
        - gare de Bitche (Bitche) departure 13:30
        - gare de Haguenau (Haguenau) departure 14:15
        - gare de Nimes (Nimes) arrival 23:30

        Requested departure: 2012/11/20 13:25:00
        From: gare de Bitche (Bitche)
        To: gare de Nimes (Nimes)
        Before the addition, no solution can be found without transfer
        After the addition, a train travels on 2012/11/20 from 13:30:00 to 23:30:00

        Requested departure: 2012/11/20 13:25:00
        From: gare de Haguenau (Haguenau)
        To: gare de Nimes (Nimes)
        Before the addition, no solution can be found without transfer
        After the addition, a train travels on 2012/11/20 from 14:15:00 to 23:30:00
        """
        self.send_and_wait("trip_add_several_new_stop_points_in_one_cots_9580_tgv.json")

        # Bitche -> Nimes
        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T132500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T132500",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        # Haguenau -> Nimes
        self.journey(
            _from="stop_area:OCE:SA:87213058",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T132500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87213058",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T132500",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_add_stop_point_non_existent(self):
        """
        Test add a stop_time with an invalid CR-CI-CH code
        The COTS feed isn't rejected and the delay is taken into account

        Requested departure: 2012/11/20 13:58:00
        From: gare de Strasbourg (Strasbourg)
        To: gare de Marseille-St-Charles (Marseille)

        Before the delay, the train travels from 16:12:00 to 21:46:00
        After the delay, the train travels from 16:12:00 to 22:16:00
        """
        self.send_and_wait("trip_add_new_stop_point_trash_stop_points_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_add_stop_point_at_the_end_make_pass_midnight(self):
        """
        Test add a stop_time at the end of the vj that arrives the day after the departure

        Requested departure: 2012/11/20 13:58:00
        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Nimes (Nimes)

        Before the addition, no solution can be found without transfer
        After the addition, an other train travels from 14:01:00 on 2012/11/20 to 00:30:00 on 2012/11/21
        """
        self.send_and_wait(
            "trip_add_new_stop_point_at_the_end_make_pass_midnight_9580_tgv.json"
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87775007",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    @xfail(reason="Waiting for fix - NAVP-1128", raises=AssertionError)
    def test_kirin_cots_trip_add_stop_point_at_the_beginning_make_pass_midnight(self):
        """
        Test add a stop_time at the beginning of the vj that the day before the first stop of the theoretical vj

        Requested departure: 2012/11/19 22:30:00
        From: gare de Luxembourg
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, an other train travels from 22:30:00 on 2012/11/19 to 22:16:00 on 2012/11/20
        """
        self.send_and_wait(
            "trip_add_new_stop_point_at_the_beginning_make_pass_midnight_9580_tgv.json"
        )

        self.journey(
            _from="stop_area:OCE:SA:82001000",
            to="stop_area:OCE:SA:87751008",
            datetime="20121119T223000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:82001000",
            to="stop_area:OCE:SA:87751008",
            datetime="20121119T223000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_add_stop_make_pass_midnight_local_and_utc(self):
        """
        Test add a stop time that arrives the same day of the theoretical vj and leaves the day after

        Requested departure: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Montpellier-Saint-Roch (Montpellier)

        Before the addition, no solution can be found without transfer
        After the addition, an other train travels from 14:01:00 on 2012/11/20 to 01:30:00 on 2012/11/21
        """
        self.send_and_wait(
            "trip_add_stop_point_make_pass_midnight_local_and_UTC_9580_tgv.json"
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87773002",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87773002",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_trip_detour_at_the_beginning(self):
        """
        Test a detour at the beginning of the vj

        Requested departure: 2012/11/20 14:00:00
        From: gare de Bitche (Bitche) that replaces gare de Frankfurt-am-Main-Hbf
        To: gare de Marseille-St-Charles (Marseille)

        Before detour, no solution can be found without transfer
        After detour, the train travels from 14:20:00 to 21:46:00
        After detour, no solution can be found without transfer from gare de Frankfurt-am-Main-Hbf
        """
        self.send_and_wait("trip_detour_start_9580.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_detour_at_the_end(self):
        """
        Test a detour at the end of the vj

        Requested departure: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Nice-Ville (Nice) that replaces gare de Marseille-St-Charles (Marseille)

        Before detour, no solution can be found without transfer
        After detour, the train travels from 14:01:00 to 21:55:00
        After detour, no solution can be found without transfer to gare de Marseille-St-Charles
        """
        self.send_and_wait("trip_detour_end_9580.json")

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_detour_in_the_middle(self):
        """
        Test a detour in the middle of the vj impacting 2 stop points:
        gare de Mulhouse and gare de Belfort-Montbeliard-TGV are deleted and gare de Vesoul is added

        Requested departure: 2012/11/20 17:00:00
        From: gare de Vesoul (Vesoul)
        To: gare de Marseille-St-Charles (Marseille)

        Before detour, no solution can be found without transfer
        After detour, the train travels from 17:33:00 to 21:46:00
        After detour, an other train travels from gare de Mulhouse to gare de Marseille-St-Charles from 21:27:00 to 06:32:00
        """
        self.send_and_wait("trip_detour_middle_9580.json")

        self.journey(
            _from="stop_area:OCE:SA:87185009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87185009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:87182063",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_trip_detour_everywhere(self):
        """
        Test a detour at the beginning, at the end and in the middle of the vj.
        Impacted stops:
        - gare de Bitche (Bitche) that replaces gare de Frankfurt-am-Main-Hbf
        - gare de Nice-Ville (Nice) that replaces gare de Marseille-St-Charles (Marseille)
        - gare de Mulhouse and gare de Belfort-Montbeliard-TGV are deleted and gare de Vesoul is added

        Requested departure: 2012/11/20 14:00:00
        From: gare de Bitche (Bitche)
        To: gare de Vesoul (Vesoul)
        Before detour, no solution can be found without transfer
        After detour, the train travels from 14:20:00 to 16:59:00

        Requested departure: 2012/11/20 17:00:00
        From: gare de Vesoul (Vesoul)
        To: gare de Nice-Ville (Nice)
        Before detour, no solution can be found without transfer
        After detour, the train travels from 17:08:00 to 21:55:00
        """
        self.send_and_wait("trip_detour_start_between_end_9580.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87185009",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87185009",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:87185009",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T170000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87185009",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T170000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_sequence_01(self):
        """
        Sequence
            - Cots 1 : Delay several stop points with a medium delay (10min)
            - Cots 2 : We keep delays except the last. It back to normal
        Requested datetime: 2012/11/20 14:00:00
        From: 14:01 > 14:01 gare de Frankfurt-am-Main-Hbf
        To:   21:46 > 21:46 gare de Marseille-St-Charles (Marseille)
        """

        """
        Delayed the 6 last stations :
        stop_date_times[7]  : 17:54 > 18:09 gare de Besancon-Franche-Comte (Les Auxons)
        ...
        stop_date_times[12] : 21:56 > 21:56 gare de Marseille-St-Charles (Marseille)
        """
        self.send_and_wait("trip_delay_9580_tgv.json")

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Suppress the delay on the last station.
        It remains 5 with delays :
        stop_date_times[7]  : 17:54 > 18:09 gare de Besancon-Franche-Comte (Les Auxons)
        ...
        stop_date_times[11] : 21:41 > 21:44 gare de Aix-en-Provence-TGV (Aix-en-Provence)
        """
        # Reload kraken
        self.kill_the_krakens()
        self.pop_krakens()

        self.send_and_wait("trip_seq1_02_delays_with_last_back_to_normal.json")

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

    def test_kirin_cots_sequence_03(self):
        """
        SNCF sequence n.03:
        1. Add a station on a vj
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, the train travels on 2012/11/20 from 14:20:00 to 21:46:00
        """
        self.send_and_wait("trip_seq3_01_add_new_stop_point.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        """
        2. Add a delay of 15 mins after the added station
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        After the delay, the train travels on 2012/11/20 from 14:20:00 to 22:01:00
        """
        self.send_and_wait("trip_seq3_02_add_delay.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        3. Back to normal: no delay + added station removed
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        After the RT update, no solution can be found without transfer

        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Marseille-St-Charles (Marseille)

        After the RT update, the train travels on 2012/11/20 from 14:01:00 to 21:46:00
        """
        self.send_and_wait("trip_seq3_03_back_to_normal.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        4. Add delay of 30 mins after the 1st station
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Still no solution can be found without transfer

        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Marseille-St-Charles (Marseille)

        After the RT update, the train travels on 2012/11/20 from 14:01:00 to 22:16:00
        """
        self.send_and_wait("trip_seq3_04_add_delay.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T135800",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_sequence_05(self):
        """
        SNCF sequence n.05:
        1. Remove stations from the vj
        From: gare de Strasbourg (Strasbourg)
        To: gare de Marseille-St-Charles (Marseille)

        Before the RT update, the train travels from 16:12:00 to 21:46:00
        After the RT update, an other train travels from 19:59:00 to 06:32:00
        """
        self.send_and_wait("trip_seq5_01_remove_stops.json")

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )
        """
        2. Add a new station
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        Before the RT update, no solution can be found without transfer
        After the RT update, the train travels from 17:18:00 to 21:46:00
        """
        self.send_and_wait("trip_seq5_02_add_stop.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        3. Back to normal: Removed stations are now back and added station isn't available
        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        After the RT update, no solution can be found without transfer

        From: gare de Strasbourg (Strasbourg)
        To: gare de Marseille-St-Charles (Marseille)

        After the RT update, the train travels from 16:12:00 to 21:46:00
        """
        self.send_and_wait("trip_seq5_03_back_to_normal.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87212027",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T160000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_sequence_08(self):
        """
        1. Detour at the beginning of the vj + 25 mins of delay on every other stops
        Requested departure: 2012/11/20 14:00:00
        From: gare de Bitche (Bitche) that replaces gare de Frankfurt-am-Main-Hbf
        To: gare de Marseille-St-Charles (Marseille)

        Before detour, no solution can be found without transfer
        After detour, the train travels from 14:20:00 to 22:11:00
        """
        self.send_and_wait("trip_seq8_01_detour_start_delay_25.json")

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        """
        2. Add new stop
        Requested departure: 2012/11/20 16:30:00
        From: gare de Vesoul (Vesoul)
        To: gare de Marseille-St-Charles (Marseille)

        Before the addition, no solution can be found without transfer
        After the addition, the train travels from 16:40:00 to 22:11:00

        From: gare de Frankfurt-am-Main-Hbf
        To: gare de Marseille-St-Charles (Marseille)

        After detour, no solution can be found without transfer
        """
        self.send_and_wait("trip_seq8_02_detour_start_delay_25_and_add_middle.json")

        self.journey(
            _from="stop_area:OCE:SA:87185009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T163000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87185009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T163000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T163000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        3. Add more delay
        Requested departure: 2012/11/20 16:30:00
        From: gare de Vesoul (Vesoul)
        To: gare de Marseille-St-Charles (Marseille)

        After delay, the train travels from 16:52:00 to 22:26:00

        From: gare de Bitche (Bitche)
        To: gare de Marseille-St-Charles (Marseille)

        After detour and delay, the train travels from 14:20:00 to 22:26:00
        """
        self.send_and_wait("trip_seq8_03_detour_start_delay_40_and_add_middle.json")

        self.journey(
            _from="stop_area:OCE:SA:87185009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T163000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        self.journey(
            _from="stop_area:OCE:SA:87193821",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_add_trip_sequence_11(self):
        """
        1. A simple trip addition with 5 stop_times all existing in navitia
        2. Trip modified with 15 minutes delay in each stop_times
        3. Return to normal
        Attention: Since physical_mode:LongDistanceTrain is absent in NTFS, physical_mode:Bike is
        used in the vehicle_journey.

        Requested datetime: 2012/11/20 11:55:00
        From: gare de Paris-Montparnasse 1-2 (Paris)
        To:   gare de Marseille-St-Charles (Marseille)
        Should have a no-solution for both requests
        """
        self.journey(
            _from="stop_area:OCE:SA:87391003",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T115500",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:87391003",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T115500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Add a new trip with:
        depart: gare de Paris-Montparnasse 1-2 (Paris) at 12:00:00
        destination: gare de Marseille-St-Charles (Marseille) at 17:00:00
        and 3 stations in between
        """
        self.send_and_wait("trip_add_paris_marseille.json")

        """
        Realtime request with same parameters as above
        Should have a solution with departure at 12:00 and arrival at 17:00
        """
        self.journey(
            _from="stop_area:OCE:SA:87391003",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T115500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        All stop times in the trip are delayed by 15 minutes.
        """
        self.send_and_wait("trip_add_paris_marseille_with_delay_15.json")

        """
        Realtime request with same parameters as above
        Should have a solution with departure at 12:15 and arrival at 17:15
        """
        self.journey(
            _from="stop_area:OCE:SA:87391003",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T115500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Return to normal without any delay
        """
        self.send_and_wait("trip_add_paris_marseille_to_normal.json")

        """
        Realtime request with same parameters as above
        Should have a solution with departure at 12:00 and arrival at 17:00
        """
        self.journey(
            _from="stop_area:OCE:SA:87391003",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T115500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_add_trip_sequence_12(self):
        """
        1. A simple trip addition with 5 stop_times all existing in navitia
        2. Trip modified with 15 minutes delay in each stop_times
        3. Trip modified with a stop_time (gare de Auxerre-St-Gervais) deleted in the above flux cots
        4. Return to normal
        Attention: Since physical_mode:LongDistanceTrain is absent in NTFS, physical_mode:Bike is
        used in the vehicle_journey.

        Requested datetime: 2012/11/20 12:55:00
        From: gare de Auxerre-St-Gervais
        To:   gare de Marseille-St-Charles (Marseille)
        Should have a no-solution for both requests
        """
        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Add a new trip with:
        depart: gare de Paris-Montparnasse 1-2 (Paris) at 12:00:00
        destination: gare de Marseille-St-Charles (Marseille) at 17:00:00
        and 3 stations in between
        """
        self.send_and_wait("trip_add_paris_marseille.json")

        """
        Realtime request with same parameters as above
        Should have a solution with departure at 13:10 and arrival at 17:00
        """
        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        All stop times in the trip are delayed by 15 minutes.
        """
        self.send_and_wait("trip_add_paris_marseille_with_delay_15.json")

        """
        Realtime request with same parameters as above
        Should have a solution with departure at 13:25 and arrival at 17:15
        """
        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Delete the second station "gare de Auxerre-St-Gervais" in the recently added trip with 15 minutes delay
        """
        self.send_and_wait(
            "trip_add_paris_marseille_with_delay_15_and_stop_time_deleted.json"
        )

        """
        Realtime request with same parameters as above
        Should have a no-solution as the departure station is deleted
        """
        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Return to normal without any delay
        """
        self.send_and_wait("trip_add_paris_marseille_to_normal.json")

        """
        Realtime request with same parameters as above
        Should have a solution with departure at 13:10 and arrival at 17:00
        """
        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_add_trip_sequence_2(self):
        """
        1. A simple trip addition with 5 stop_times all existing in navitia
        2. Trip modified with 15 minutes delay in each stop_times
        3. Trip modified with a new stop_time (gare de Orleans) added in the above flux cots
        4. Delete the trip with "statutCirculationOPE": "SUPPRESSION" in all stop_times
        5. Add again the same trip as 1.
        Attention: Since physical_mode:LongDistanceTrain is absent in NTFS, physical_mode:Bike is
        used in the vehicle_journey.

        Requested datetime: 2012/11/20 12:55:00
        From: gare de Orleans
        To:   gare de Marseille-St-Charles (Marseille)
        Should have a no-solution for both requests
        """
        self.journey(
            _from="stop_area:OCE:SA:87543009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        self.journey(
            _from="stop_area:OCE:SA:87543009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Add a new trip with:
        depart: gare de Paris-Montparnasse 1-2 (Paris) at 12:00:00
        destination: gare de Marseille-St-Charles (Marseille) at 17:00:00
        and 3 stations in between
        """
        self.send_and_wait("trip_add_paris_marseille.json")

        """
        Realtime request with same parameters as above
        Should have a no-solution as the departure station doesn't exist in recently added trip
        """
        self.journey(
            _from="stop_area:OCE:SA:87543009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        All stop times in the trip are delayed by 15 minutes.
        """
        self.send_and_wait("trip_add_paris_marseille_with_delay_15.json")

        """
        Realtime request with same parameters as above
        Should have a no-solution as the departure station doesn't exist in recently added trip
        """
        self.journey(
            _from="stop_area:OCE:SA:87543009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Add a station "gare de Orleans" in the recently added trip with 15 minutes delay
        """
        self.send_and_wait(
            "trip_add_paris_marseille_with_delay_15_and_stop_time_added.json"
        )

        """
        Realtime request with same parameters as above
        Should have a solution with departure at 12:55 and arrival at 17:15
        """
        self.journey(
            _from="stop_area:OCE:SA:87543009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Delete the recently added trip
        """
        self.send_and_wait(
            "trip_add_paris_marseille_delete_with_delay_15_and_stop_time_added.json"
        )

        """
        Realtime request with same parameters as above
        Should have a no-solution as the trip has been deleted
        """
        self.journey(
            _from="stop_area:OCE:SA:87543009",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Add the trip recently deleted above
        """
        self.send_and_wait("trip_add_paris_marseille.json")

        """
        Realtime request with datetime: 2012/11/20 12:55:00
        From: gare de Auxerre-St-Gervais
        To:   gare de Marseille-St-Charles (Marseille)
        Should have a solution with departure at 13:10 and arrival at 17:00
        """
        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T125500",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_sequence_09(self):
        """
        Sequence 09
          - Cots 1 : Delay All stop points with a medium delay (10min) + add 2 new stop point at the end
          - Cots 2 : Change delays (60 mins) of the last 5 stop point
          - Cots 3 : Remove the 2 added stop point

        Base request:
        Requested datetime: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To:   gare de Marseille-St-Charles (Marseille)
        Departure at 14:01 and arrival at 21:46
        """
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        """
        Delay all stop point + add 2 new stop point at the end:
            stop_date_times[0]  : 14:11 gare de Frankfurt-am-Main-Hbf
            ...
        add stop_date_times[13] : 22:00 > 22:30 gare de Cannes (Cannes)
        add stop_date_times[14] : 23:00         gare de Nice-ville (Nice)
        """
        self.send_and_wait("trip_seq9_01_delays_and_new_stop_points.json")

        """
        Requested datetime: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To:   gare de Marseille-St-Charles (Marseille)
        Departure at 14:11 and arrival at 21:56 with 10 minutes delay
        """
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Requested datetime: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To:   gare de Nice-ville (Nice)
        Should have a no-solution as the destination is added by flux cots
        """
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="base_schedule",
        )

        """
        Requested datetime: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To:   gare de Nice-ville (Nice)
        Departure at 14:11 and arrival at 23:00
        """
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Change delays (60 mins) of the last 5 stop point
        stop_date_times[0]  : 14:11 gare de Frankfurt-am-Main-Hbf
        ...
        stop_date_times[14] : 00:00 gare de Nice-ville (Nice)
        """
        self.send_and_wait("trip_seq9_02_update_delays.json")

        """
        Requested datetime: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To:   gare de Nice-ville (Nice)
        Departure at 14:11 and arrival at 00:00 with one hour delay
        """
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Remove the 2 added stop point at the end
        stop_date_times[0]  : 14:11 gare de Frankfurt-am-Main-Hbf
        ...
        stop_date_times[12] : 22:46 gare de Marseille-St-Charles (Marseille)
        """
        self.send_and_wait("trip_seq9_03_delays_and_delete_stop_points.json")

        """
        Requested datetime: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To:   gare de Marseille-St-Charles (Marseille)
        Departure at 14:11 and arrival at 22:46 with one hour delay
        """
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        Requested datetime: 2012/11/20 14:00:00
        From: gare de Frankfurt-am-Main-Hbf
        To:   gare de Nice-ville (Nice)
        Should have a no-solution as the destination is added and then deleted by flux cots
        """
        self.journey(
            _from="stop_area:OCE:SA:80110684",
            to="stop_area:OCE:SA:87756056",
            datetime="20121120T140000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

    def test_kirin_cots_add_and_remove_new_course(self):
        """
        Test the addition of a circulation and then, the removal of the added circulation

        Requested datetime: 2012/11/20 12:00:00
        From: gare de Auxerre-St-Gervais
        To:   gare de Marseille-St-Charles

        Before added circulation, no solution can be found without transfer.
        After added circulation, a train travels from 13:10:00 to 17:00:00
        """
        self.send_and_wait("trip_add_new_trip_151515.json")

        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T120000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )

        """
        After new RT update (removal of the added circulation), no solution can be found without transfer.
        """
        self.send_and_wait("trip_remove_new_trip_151515.json")

        self.journey(
            _from="stop_area:OCE:SA:87683573",
            to="stop_area:OCE:SA:87751008",
            datetime="20121120T120000",
            max_nb_transfers="0",
            data_freshness="realtime",
        )


class TestGuichetUniqueExperimental(GuichetUnique, ArtemisTestFixture):
    pass
