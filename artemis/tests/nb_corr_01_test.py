from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.NbCorr01
@dataset([DataSet("nb-corr-01")])
class NbCorr01(object):
    """
    TODO: put there comments about the dataset
    """

    def test_nb_corr_01_01(self):
        self.journey(
            _from="stop_area:NC1:SA:1",
            to="stop_area:NC1:SA:4",
            datetime="20041213T0700",
        )


class TestNbCorr01Experimental(NbCorr01, ArtemisTestFixture):
    pass
