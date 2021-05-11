import logging
import inspect
import psycopg2
import requests
import os
import datetime
from retrying import retry
import artemis.utils as utils

from artemis.configuration_manager import config

logger = logging.getLogger(__name__)


# given a cursor on a db, and table names separated by a comma (ex: "tata, toto, titi")
def truncate_tables(cursor, table_names_string):
    logger.debug("query db: TRUNCATE {} CASCADE ;".format(table_names_string))
    cursor.execute("TRUNCATE {} CASCADE ;".format(table_names_string))


# the time cost is around 1.3s on artemis platform
def clean_kirin_db():
    logger.debug("cleaning kirin database")
    conn = psycopg2.connect(config["KIRIN_DB"])
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT relname FROM pg_stat_user_tables WHERE relname != 'alembic_version';"
        )
        tables = cur.fetchall()

        truncate_tables(
            cur, ", ".join(e[0] for e in tables if e[0] not in ("layer", "topology"))
        )

        conn.commit()

        cur.execute(
            "INSERT INTO contributor SELECT 'realtime.sherbrooke','ca-qc-sherbrooke','token_to_be_modified',"
            "'feed_url_to_be_modified','gtfs-rt'"
        )
        cur.execute(
            "INSERT INTO contributor SELECT 'realtime.cots','guichet-unique','token_to_be_modified',"
            "'N/A','cots'"
        )
        conn.commit()
        logger.debug("kirin db purge done")
    except Exception as e:
        error_msg = "Problem while cleaning Kirin Db with error : {}".format(str(e))
        logger.exception(error_msg)
        conn.close()
        assert False, error_msg
    conn.close()


class CommonTestFixture(object):
    def get_dataset_name(self):
        mro = inspect.getmro(self.__class__)
        return "Test{}".format(mro[1].__name__)

    def get_reference_suffix_path(self):
        return os.path.join(self.get_dataset_name())

    def get_reference_filename_prefix(self):
        """
        When there is multiple calls to request_compare within one test function
          the name of the reference file for the first call is `func_name`
          For the (n+1)th call, the name of the reference file is `func_name_n`
        """
        func_name = utils.get_calling_test_function()

        if self.nb_call_to_request_compare <= 1:
            return func_name
        else:
            assert self.nb_call_to_request_compare > 1
            return "{}_{}".format(func_name, self.nb_call_to_request_compare - 1)

    def get_test_name(self):
        path = os.path.join(
            self.get_reference_suffix_path(), self.get_reference_filename_prefix()
        )
        return str(path)

    def get_reference_file_path(self):
        filename = "{}.json".format(self.get_reference_filename_prefix())
        return os.path.join(
            config["REFERENCE_FILE_PATH"], self.get_reference_suffix_path(), filename
        )

    @staticmethod
    def _send_cots(cots_file_name):
        r = requests.post(
            config["KIRIN_API"] + "/cots",
            data=utils.get_rt_data(cots_file_name).encode("UTF-8"),
            headers={"Content-Type": "application/json;charset=utf-8"},
        )
        r.raise_for_status()

    @retry(stop_max_delay=25000, wait_fixed=500)
    def get_last_rt_loaded_time(self, cov):
        if self.check_ref:
            return

        _res, _, status_code = utils.request("coverage/{cov}/status".format(cov=cov))

        if status_code == 503:
            raise Exception("Navitia is not available")

        return _res.get("status", {}).get("last_rt_data_loaded", object())

    @retry(stop_max_delay=60000, wait_fixed=500)
    def wait_for_rt_reload(self, last_rt_data_loaded, cov):
        if self.check_ref:
            return

        rt_data_loaded = self.get_last_rt_loaded_time(cov)

        if last_rt_data_loaded == rt_data_loaded:
            raise Exception("real time data not loaded")

    def send_and_wait(self, rt_file_name):
        """
        Send a COTS and wait until the data is reloaded
        :param rt_file_name: name of the real-time feed file (obviously)
        """
        if self.check_ref:
            return

        if len(self.data_sets) > 1:
            logger.warning(" >1 data_set for test class !!!")
        coverage = self.data_sets[0].name
        last_rt_data_loaded = self.get_last_rt_loaded_time(coverage)
        start_datetime = datetime.datetime.utcnow()
        self._send_cots(rt_file_name)
        cots_processing_time = datetime.datetime.utcnow()
        self.wait_for_rt_reload(last_rt_data_loaded, coverage)
        kraken_reloaded_time = datetime.datetime.utcnow()

        def round_time(beginning, end):
            return round((end - beginning).total_seconds(), 2)

        logger.info(
            "{test}: RT processed in {total}s (Kirin:{kirin}/Kraken:{kraken})".format(
                test=utils.get_calling_test_function(),
                total=round_time(start_datetime, kraken_reloaded_time),
                kirin=round_time(start_datetime, cots_processing_time),
                kraken=round_time(cots_processing_time, kraken_reloaded_time),
            )
        )


class DataSet(object):
    def __init__(
        self,
        name,
        reload_timeout=datetime.timedelta(minutes=30),
        fixed_wait=datetime.timedelta(seconds=20),
    ):
        self.name = name
        self.reload_timeout = reload_timeout
        self.fixed_wait = fixed_wait

    def __str__(self):
        return self.name


def dataset(datasets):
    """
    decorator giving class attribute 'data_sets'
    each test should have this decorator to make clear the data set used for the tests
    """

    def deco(cls):
        cls.data_sets = datasets
        return cls

    return deco
