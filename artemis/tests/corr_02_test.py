from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest


@pytest.mark.Corr02
@dataset([DataSet("corr-02")])
class Corr02(object):
    """
    TODO: put there comments about the dataset
    """

    def test_corr_02_01(self):
        """
        This test shows that a third compute is necessary.
        The journey must be:
        13/12  15:00 Arret 1
        13/12  15:10 Arret 2
          transfert
        13/12  15:16 Arret 2
        13/12  15:24 Arret 3
          transfert
        13/12  15:40 Arret 3
        13/12  15:50 Arret 4
        """
        self.journey(
            _from="stop_area:CR2:SA:1",
            to="stop_area:CR2:SA:4",
            datetime="20041213T0700",
        )


@set_scenario({"corr-02": {"scenario": "experimental"}})
class TestCorr02Experimental(Corr02, ArtemisTestFixture):
    pass
