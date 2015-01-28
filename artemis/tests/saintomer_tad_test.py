from artemis.test_mechanism import ArtemisTestFixture, dataset, DataSet


@dataset([DataSet("saintomer")])
class TestSaintOmer(ArtemisTestFixture):
    """
      test "on demand transport"
    """
    @xfail(reason="http://jira.canaltp.fr/browse/NAVITIAII-1540", raises=AssertionError)
    def test_saint_omer_admin_to_poi(self):
        """
        ID artemis v1: 0 and 1
        """
        self.journey(_from="admin:62595",
                     to="poi:adm117", datetime="20121206T133500",
                     walking_speed="1", max_duration_to_pt="1000")

    def test_saint_omer_poi_to_admin(self):
        """
        ID artemis v1: 2
        """
        self.journey(_from="poi:adm117",
                     to="admin:62595", datetime="20121206T153500",
                     walking_speed="1", max_duration_to_pt="1000")

    @xfail(reason="http://jira.canaltp.fr/browse/NAVITIAII-1540", raises=AssertionError)
    def test_saint_omer_admin_to_address(self):
        """
        ID artemis v1: 3
        """
        self.journey(_from="admin:62595",
                     to="2.26668185;50.75150538", datetime="20121206T153500",
                     walking_speed="1", max_duration_to_pt="1000")

    def test_saint_omer_address_to_admin(self):
        """
        ID artemis v1: 4
        """
        self.journey(_from="2.26668185;50.75150538",
                     to="admin:62595", datetime="20121206T153500",
                     walking_speed="1", max_duration_to_pt="1000")

    @xfail(reason="http://jira.canaltp.fr/browse/NAVITIAII-1540", raises=AssertionError)
    def test_saint_omer_admin_to_sto_area(self):
        """
        ID artemis v1: 5
        """
        self.journey(_from="admin:62595",
                     to="stop_area:ASO:SA:1", datetime="20121206T153500",
                     walking_speed="1", max_duration_to_pt="1000")

    def test_saint_omer_stop_area_to_admin(self):
        """
        ID artemis v1: 6
        """
        self.journey(_from="stop_area:ASO:SA:1",
                     to="admin:62595", datetime="20121206T153500",
                     walking_speed="1", max_duration_to_pt="1000")

    @xfail(reason="http://jira.canaltp.fr/browse/NAVITIAII-1540", raises=AssertionError)
    def test_saint_omer_admin_to_admin_01(self):
        """
        ID artemis v1: 7
        """
        self.journey(_from="admin:62765",
                     to="admin:62458", datetime="20121120T101500",
                     walking_speed="1", max_duration_to_pt="1000")

    @xfail(reason="http://jira.canaltp.fr/browse/NAVITIAII-1540", raises=AssertionError)
    def test_saint_omer_admin_to_admin_02(self):
        """
        ID artemis v1: 8
        """
        self.journey(_from="admin:62458",
                     to="admin:62765", datetime="20121120T101500",
                     walking_speed="1", max_duration_to_pt="1000")
