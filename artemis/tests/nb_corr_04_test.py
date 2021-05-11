from artemis.common_fixture import dataset, DataSet
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.NbCorr04
@dataset([DataSet("nb-corr-04")])
class NbCorr04(object):
    """
    TODO: put there comments about the dataset
    """

    def test_nb_corr_04_01(self):
        self.journey(
            _from="stop_area:NC4:SA:1",
            to="stop_area:NC4:SA:4",
            datetime="20041213T0700",
        )

    def test_nb_corr_04_02(self):
        self.journey(
            _from="stop_area:NC4:SA:1",
            to="stop_area:NC4:SA:4",
            datetime="20041213T0700",
        )


class TestNbCorr04Experimental(NbCorr04, ArtemisTestFixture):
    pass
