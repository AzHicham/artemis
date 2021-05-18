from collections import defaultdict, OrderedDict
import logging
import os
import shutil
import psycopg2
import json
import pytest
import inspect
from retrying import Retrying, RetryError
from artemis import default_checker
from artemis import utils
from artemis.configuration_manager import config
from artemis.common_fixture import CommonTestFixture, truncate_tables

from typing import List

_tyr = config["TYR_DIR"] + "/manage.py"
_tyr_config_file = config["TYR_DIR"] + "/settings.py"

# to limit the permissions of the jenkins user on the artemis platform, we create a proxy for all kraken services
_kraken_wrapper = "/usr/local/bin/kraken_service_wrapper"


def kraken_status(data_set):
    response, _, _ = utils.request("coverage/{r}".format(r=data_set.name))
    assert "error" not in response, "problem with the region: {error}".format(
        error=response["error"]
    )

    current_region = response.get("regions", [None])[0]
    # the region should be the one asked for
    assert current_region and current_region["id"] == data_set.name

    return current_region["status"]


class ArtemisTestFixture(CommonTestFixture):
    """
    Mother class for all integration tests
    """

    dataset_binarized = []  # type: List[str]

    @pytest.fixture(scope="function", autouse=True)
    def before_each_test(self):
        """
        setup function called before each test

        Note: py.test does not want to collect class with custom constructor,
        so we init the class in the setup
        """
        self.test_counter = defaultdict(int)

    def get_file_name(self):
        """
        create the name of the file for storing the query.

        the file is:

        {class_name}/{function_name}(|_{call_number}).json

        """
        mro = inspect.getmro(self.__class__)
        class_name = "Test{}".format(mro[1].__name__)

        func_name = utils.get_calling_test_function()
        test_name = "{}/{}".format(class_name, func_name)

        self.test_counter[test_name] += 1

        if self.test_counter[test_name] > 1:
            return "{}_{}.json".format(test_name, self.test_counter[test_name] - 1)
        else:
            return "{}.json".format(test_name)

    @classmethod
    @pytest.yield_fixture(scope="class", autouse=True)
    def my_method_setup(cls, request):
        """
        method called once for each fixture

        Handle init and teardown of the fixture
        """
        logging.getLogger(__name__).debug(
            "Setting up the tests {}".format(cls.__name__)
        )
        cls.init_fixture(
            skip_bina=request.config.getvalue("skip_bina"),
            journey_full_response_comparison_mode=request.config.getvalue(
                "hard_journey_check"
            ),
            check_ref=request.config.getvalue("check_ref"),
        )

        logging.getLogger(__name__).debug("Running the tests {}".format(cls.__name__))
        yield

        if not request.config.getvalue("check_ref"):
            logging.getLogger(__name__).debug(
                "Cleaning up the tests {}".format(cls.__name__)
            )
            cls.clean_fixture()

    @classmethod
    def init_fixture(cls, skip_bina, journey_full_response_comparison_mode, check_ref):
        """
        Method called once before running the tests of the fixture

        Launch all necessary services to have a running navitia solution
        :param skip_bina to use the already done binarization
        :param journey_full_response_comparison_mode if set to True will compare the journeys
        on the full_response with the no regression mode (like the other apis)
        :param check_ref to check only consistency of reference files
        This should be used only occasionally as the journey response are prone to changes
        """
        # we store the variable to use it a test time
        if journey_full_response_comparison_mode:
            logging.getLogger(__name__).warning("Full journeys comparison activated")
        cls.journey_full_response_comparison_mode = (
            journey_full_response_comparison_mode
        )
        cls.check_ref = check_ref

        if check_ref:
            return

        cls.kill_jormungandr()

        cls.run_additional_service()

        cls.manage_data(skip_bina)

        cls.pop_krakens()

        cls.pop_jormungandr()

    @classmethod
    def manage_data(cls, skip_bina):

        cls.clean_jormun_db()

        if skip_bina:
            logging.getLogger(__name__).info("skipping binarization")
            return

        for data_set in cls.data_sets:
            if data_set.name in cls.dataset_binarized:
                logging.getLogger(__name__).debug(
                    "binarization dataset {} has been done, skipping....".format(
                        data_set
                    )
                )
                continue
            cls.remove_data_by_dataset(data_set)
            cls.update_data_by_dataset(data_set)
            cls.read_data_by_dataset(data_set)
            cls.dataset_binarized.append(data_set.name)

    @classmethod
    def remove_data_by_dataset(cls, data_set):
        logging.getLogger(__name__).debug("deleting data for {}".format(data_set.name))
        try:
            if os.path.exists(utils.nav_path(data_set.name)):
                os.remove(utils.nav_path(data_set.name))
        except Exception:
            logging.getLogger(__name__).exception("can't remove data.nav.lz4")

    @classmethod
    def update_data_by_dataset(cls, data_set):
        fusio_databases_file = utils.new_fusio_files_path(data_set.name)
        if not os.path.exists(fusio_databases_file):
            return

        logging.getLogger(__name__).debug("updating data for {}".format(data_set.name))

        # we copy the file to update the reference data
        shutil.move(
            fusio_databases_file,
            os.path.join(
                utils.instance_data_path(data_set.name), "fusio/databases.zip"
            ),
        )

    @classmethod
    def read_data_by_dataset(cls, data_set):
        logging.getLogger(__name__).debug("reading data for {}".format(data_set.name))
        # we'll read all subdir
        data_path = utils.instance_data_path(data_set.name)

        data_dirs = [
            os.path.join(data_path, sub_dir_name)
            for sub_dir_name in os.listdir(data_path)
            if os.path.isdir(os.path.join(data_path, sub_dir_name))
        ]

        logging.getLogger(__name__).debug("loading {}".format(data_dirs))
        utils.launch_exec(
            "sudo {tyr} load_data {data_set} {data_set_dir}".format(
                tyr=_tyr, data_set=data_set.name, data_set_dir=",".join(data_dirs)
            ),
            additional_env={"TYR_CONFIG_FILE": _tyr_config_file},
        )

    @classmethod
    def clean_fixture(cls):
        """
        Method called once after running the tests of the fixture.
        """
        logging.getLogger(__name__).debug(
            "Tearing down the tests {}, time to clean up".format(cls.__name__)
        )
        cls.kill_the_krakens()

    @classmethod
    def run_additional_service(cls):
        """
        run all services that have to be active for all tests
        """
        pass

    @classmethod
    def clean_jormun_db(cls):
        logging.getLogger(__name__).debug("cleaning jormungandr database")
        conn = psycopg2.connect(config["JORMUNGANDR_DB"])
        try:
            cur = conn.cursor()
            tables = ["data_set", "instance", "job"]

            truncate_tables(cur, ", ".join(tables))

            # we add the instances in the table
            for data_set in cls.data_sets:
                cur.execute(
                    "INSERT INTO instance (name, is_free, is_open_data, scenario) VALUES ('{}', true, false, '{}');".format(
                        data_set.name, "distributed"
                    )
                )

            conn.commit()
            logging.getLogger(__name__).debug("query done")
        except Exception:
            logging.getLogger(__name__).exception("problem with jormun db")
            conn.close()
            assert False, "problem while cleaning jormungandr db"
        conn.close()

    @classmethod
    def pop_krakens(cls):
        """
        launch all the kraken services
        """
        if cls.check_ref:
            return

        for data_set in cls.data_sets:
            logging.getLogger(__name__).debug(
                "launching the kraken {}".format(data_set.name)
            )
            return_code, _ = utils.launch_exec(
                "sudo {service} {kraken} start".format(
                    service=_kraken_wrapper, kraken=data_set.name
                )
            )

            assert return_code == 0, "command failed"

    @classmethod
    def kill_the_krakens(cls):
        if cls.check_ref:
            return

        for data_set in cls.data_sets:
            logging.getLogger(__name__).debug(
                "killing the kraken {}".format(data_set.name)
            )
            return_code, _ = utils.launch_exec(
                "sudo {service} {kraken} stop".format(
                    service=_kraken_wrapper, kraken=data_set.name
                )
            )

            assert return_code == 0, "command failed"

    @classmethod
    def pop_jormungandr(cls):
        """
        launch the front end
        """
        logging.getLogger(__name__).debug("running jormungandr")
        # jormungandr is launched with apache
        utils.launch_exec("sudo service apache2 status")
        ret, _ = utils.launch_exec("sudo service apache2 start")
        utils.launch_exec("sudo service apache2 status")

        assert ret == 0, "cannot start apache"

        # to have better errors, we check at the beginning that all is right
        for data_set in cls.data_sets:

            # we wait a bit for the kraken to be started
            try:
                Retrying(
                    stop_max_delay=data_set.reload_timeout.total_seconds() * 1000,
                    wait_fixed=data_set.fixed_wait.total_seconds() * 1000,
                    retry_on_result=lambda x: x != "running",
                ).call(kraken_status, data_set)
            except RetryError as e:
                assert False, "region {r} KO, status={s}".format(
                    r=data_set.name, s=e.last_attempt.value
                )

    @classmethod
    def kill_jormungandr(cls):
        logging.getLogger(__name__).debug("killing jormungandr")
        utils.launch_exec("sudo service apache2 status")
        ret, _ = utils.launch_exec("sudo service apache2 stop")
        utils.launch_exec("sudo service apache2 status")

        assert ret == 0, "cannot stop apache"

    ###################################
    # wrappers around utils functions #
    ###################################

    def api(
        self,
        url,
        response_checker=default_checker.default_checker,
        enable_benchmark=False,
    ):
        """
        used to check misc API

        NOTE: works only when one region is loaded for the moment (when needed change this)
        """
        if len(self.__class__.data_sets) == 1:
            full_url = "coverage/{region}/{url}".format(
                region=self.__class__.data_sets[0].name, url=url
            )

        return self._api_call(full_url, response_checker, enable_benchmark)

    def _api_call(self, url, response_checker, enable_benchmark=False):
        """
        call the api and check against previous results

        the query is writen in a file
        """
        if self.check_ref:  # only check consistency
            filename = self.get_file_name()
            assert utils.check_reference_consistency(filename, response_checker)
            return

        response, url, _ = utils.request(url)
        filtered_response = response_checker.filter(response)

        filename = self._save_response(url, response, filtered_response)

        utils.compare_with_ref(filtered_response, filename, response_checker)

    def journey(
        self,
        _from,
        to,
        datetime,
        datetime_represents="departure",
        response_checker=default_checker.default_journey_checker,
        auto_from=None,
        auto_to=None,
        first_section_mode=[],
        last_section_mode=[],
        direct_path_mode=[],
        enable_benchmark=False,
        **kwargs
    ):
        """
        syntactic sugar around the journey api

        auto_from and auto_to are used to access the autocomplete api

        TODO: example

        TODO: just forward args to the 'request' module without creating a string
        """
        real_from = self.call_autocomplete(auto_from) if auto_from else _from
        assert real_from

        real_to = self.call_autocomplete(auto_to) if auto_to else to
        assert real_to

        assert datetime
        query = "from={real_from}&to={real_to}&datetime={date}&datetime_represents={represent}".format(
            date=datetime,
            represent=datetime_represents,
            real_from=real_from,
            real_to=real_to,
        )
        for mode in first_section_mode:
            query = "{query}&first_section_mode[]={mode}".format(query=query, mode=mode)

        for mode in last_section_mode:
            query = "{query}&last_section_mode[]={mode}".format(query=query, mode=mode)

        for mode in direct_path_mode:
            query = "{query}&direct_path_mode[]={mode}".format(query=query, mode=mode)

        for k, v in kwargs.iteritems():
            query = "{query}&{k}={v}".format(query=query, k=k, v=v)

        # Add current_datetime for disruptions
        query = "{query}&_current_datetime={d}".format(query=query, d=datetime)

        if len(self.__class__.data_sets) == 1:
            # for tests with only one dataset, we directly use the region's journey API
            # Note: this should not be mandatory, but since there are still bugs with the global journey API
            # we use this for the moment.
            query = "coverage/{region}/journeys?{q}".format(
                region=self.__class__.data_sets[0].name, q=query
            )

        if self.journey_full_response_comparison_mode:
            # we want to compare the journeys very thoroughly, check the non regression on the full_response
            response_checker = default_checker.journeys_retrocompatibility_checker

        self._api_call(query, response_checker)

    def _save_response(self, url, response, filtered_response):
        """
        save the response in a file and return the filename (with the fixture directory)
        """
        filename = self.get_file_name()
        file_complete_path = os.path.join(config["RESPONSE_FILE_PATH"], filename)
        if not os.path.exists(os.path.dirname(file_complete_path)):
            os.makedirs(os.path.dirname(file_complete_path))

        # to ease debug, we add additional information to the file
        # only the response elt will be compared, so we can add what we want (additional flags or whatever)
        enhanced_response = OrderedDict(
            {
                "query": url,
                "response": utils.order_response(filtered_response),
                "full_response": response,
            }
        )

        file_ = open(file_complete_path, "w")
        file_.write(
            json.dumps(
                enhanced_response, indent=2, separators=(",", ": "), sort_keys=False
            )
        )
        file_.close()

        return filename

    def call_autocomplete(self, place):
        # TODO!
        pass
