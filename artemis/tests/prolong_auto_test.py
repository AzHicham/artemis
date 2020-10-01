from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.ProlongAuto
@dataset([DataSet("prolong-auto")])
class ProlongAuto(object):
    """
    The dataset provide service prolongation examples.

    This means that different vehicle journeys are actually the same physical vehicle.
    This can be seen with bus or tramway when their head sign changes along the way.
    It allows passengers to continue their journey while staying in the same vehicle.
    This is achieve in the data with the same `block_id` in trips.txt
    """

    def test_prolong_auto_01(self):
        self.journey(
            _from="stop_area:PRA:SA:1",
            to="stop_area:PRA:SA:5",
            datetime="20041213T0700",
        )

    def test_prolong_auto_02(self):
        self.journey(
            _from="stop_area:PRA:SA:1",
            to="stop_area:PRA:SA:9",
            datetime="20041213T0700",
            max_duration_to_pt=0,
        )

    def test_prolong_auto_03(self):
        self.journey(
            _from="stop_area:PRA:SA:1",
            to="stop_area:PRA:SA:5",
            datetime="20041213T0700",
        )


@set_scenario({"prolong-auto": {"scenario": "new_default"}})
class TestProlongAutoNewDefault(ProlongAuto, ArtemisTestFixture):
    pass


@set_scenario({"prolong-auto": {"scenario": "experimental"}})
class TestProlongAutoExperimental(ProlongAuto, ArtemisTestFixture):
    pass
