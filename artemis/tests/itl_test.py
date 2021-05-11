from artemis.common_fixture import dataset, DataSet, set_scenario
from artemis.tests.fixture import ArtemisTestFixture
import pytest

xfail = pytest.mark.xfail


@pytest.mark.Itl
@dataset([DataSet("itl")])
class Itl(object):
    """
    test local traffic policy constraint
    """

    def test_itl_01(self):
        self.journey(
            _from="stop_area:ITL:SA:1",
            to="stop_area:ITL:SA:7",
            datetime="20041213T070000",
        )

    def test_itl_02(self):
        self.journey(
            _from="stop_area:ITL:SA:1",
            to="stop_area:ITL:SA:7",
            datetime="20041213T070100",
        )


@set_scenario({"itl": {"scenario": "experimental"}})
class TestItlExperimental(Itl, ArtemisTestFixture):
    pass
