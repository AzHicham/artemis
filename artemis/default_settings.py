# encoding: utf-8

import os

# Active Artemis NG
USE_ARTEMIS_NG = os.getenv("ARTEMIS_USE_ARTEMIS_NG", "False") == "True"

# Use Artemis with loki for pt
USE_LOKI = os.getenv("ARTEMIS_USE_LOKI", "False") == "True"

# Path to artemis_data folder
DATA_DIR = os.getenv("ARTEMIS_DATA_DIR", "/srv/artemis_data")

# By default, the requests will be made locally. But it can be directed to any Jormun/Tyr instance
URL_JORMUN = os.getenv("ARTEMIS_URL_JORMUN", "http://localhost")
URL_TYR = os.getenv("ARTEMIS_URL_TYR", "http://localhost:9898")

# Usefull when using Kirin with Artemis
KIRIN_API = os.getenv("ARTEMIS_KIRIN_API", "http://localhost:9090")
KIRIN_DB = os.getenv(
    "ARTEMIS_KIRIN_DB", "dbname=kirin user=kirin host=localhost password=kirin"
)

# Path of the Artemis references
REFERENCE_FILE_PATH = os.getenv("ARTEMIS_REFERENCE_FILE_PATH", "reference")

# Path to Create responses and references files, when there is a fail
RESPONSE_FILE_PATH = os.getenv("ARTEMIS_RESPONSE_FILE_PATH", "output")

base_path = os.path.realpath(os.path.dirname(__file__) + "/..")
# For ArtemisNG orchestrator, path to the sources of repo 'navitia-docker-compose'
DOCKER_COMPOSE_PATH = os.getenv(
    "ARTEMIS_DOCKER_COMPOSE_PATH", base_path + "/navitia-docker-compose"
)
# For ArtemisNG orchestrator, path to the root of artemis tests sources
TEST_PATH = os.getenv("ARTEMIS_TEST_PATH", base_path + "/artemis/tests")

TYR_DIR = "/srv/tyr"

CITIES_INPUT_FILE = DATA_DIR + "/france_boundaries.osm.pbf"

DATASET_PATH_LAYOUT = DATA_DIR + "/{dataset}/"

NAV_FILE_PATH_LAYOUT = "/srv/ed/{dataset}/data.nav.lz4"

NEW_FUSIO_FILE_PATH_LAYOUT = "/srv/fusio/source/{dataset}/NAVITIART/databases.zip"

API_POINT_PREFIX = ""

JORMUNGANDR_DB = (
    "dbname=jormungandr user=jormungandr host=localhost password=jormungandr"
)

CITIES_DB = os.getenv(
    "ARTEMIS_CITIES_DB", "dbname=cities user=navitia host=localhost password=password"
)

CONTAINER_DATA_INPUT_PATH = "/srv/ed/input"

CONTAINER_DATA_OUTPUT_PATH = "/srv/ed/output"

LOG_LEVEL = os.getenv("ARTEMIS_LOG_LEVEL", "INFO")

LOGGER = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "[%(asctime)s] [%(levelname)5s] [%(name)25s] %(message)s"}
    },
    "handlers": {
        "default": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "": {"handlers": ["default"], "level": LOG_LEVEL, "propagate": True},
        "requests": {"handlers": ["default"], "level": "WARN", "propagate": True},
    },
}
