from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.NbCorr03
@dataset([DataSet("nb-corr-03")])
class NbCorr03(object):
    """
    TODO: put there comments about the dataset
    """

    def test_nb_corr_03_01(self):
        self.journey(
            _from="stop_area:NC3:SA:1",
            to="stop_area:NC3:SA:4",
            datetime="20041213T0700",
        )

    def test_nb_corr_03_02(self):
        self.journey(
            _from="stop_area:NC3:SA:1",
            to="stop_area:NC3:SA:5",
            datetime="20041213T0700",
        )


@set_scenario({"nb-corr-03": {"scenario": "experimental"}})
class TestNbCorr03Experimental(NbCorr03, ArtemisTestFixture):
    pass
