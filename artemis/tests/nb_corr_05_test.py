from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.NbCorr05
@dataset([DataSet("nb-corr-05")])
class NbCorr05(object):
    """
    TODO: put there comments about the dataset
    """

    def test_nb_corr_05_01(self):
        self.journey(
            _from="stop_area:NC5:SA:1",
            to="stop_area:NC5:SA:4",
            datetime="20041213T0700",
        )


class TestNbCorr05Experimental(NbCorr05, ArtemisTestFixture):
    pass
