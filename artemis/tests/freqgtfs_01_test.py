from artemis.test_mechanism import ArtemisTestFixture, dataset, DataSet


@dataset([DataSet("freqgtfs-01")])
class TestFreqGtfs_01(ArtemisTestFixture):
    """
    test frequencies to stops serialisation by FUSiO
    """

    def test_freqgtfs_01_01(self):
        self.journey(_from="stop_area:FQT:SA:1374208",
                     to="stop_area:FQT:SA:211435",
                     datetime="20120905T062000")

    def test_freqgtfs_01_02(self):
        self.journey(_from="stop_area:FQT:SA:527405",
                     to="stop_area:FQT:SA:1344488",
                     datetime="20120820T170000")

    def test_freqgtfs_01_03(self):
        self.journey(_from="stop_area:FQT:SA:215949",
                     to="stop_area:FQT:SA:212127",
                     datetime="20121110T070000")

    def test_freqgtfs_01_04(self):
        self.journey(_from="stop_area:FQT:SA:212127",
                     to="stop_area:FQT:SA:215949",
                     datetime="20121110T070000")

    def test_freqgtfs_01_05(self):
        self.journey(_from="stop_area:FQT:SA:210216",
                     to="stop_area:FQT:SA:211020",
                     datetime="20120923T094000")

    def test_freqgtfs_01_06(self):
        self.journey(_from="stop_area:FQT:SA:527405",
                     to="stop_area:FQT:SA:1374208",
                     datetime="20120822T192900")

