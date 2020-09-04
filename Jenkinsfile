pipeline {
    agent any
    stages {
        stage('Docker Compose') {
            steps {
                sh 'cd navitia-docker-compose'
                sh 'docker-compose -f docker-compose.yml -f artemis/docker-artemis-instance.yml up -d'
            }
        }
        stage('Build') {
            agent {
                dockerfile true
            }
            environment {
                ARTEMIS_LOG_LEVEL='DEBUG'
                ARTEMIS_USE_ARTEMIS_NG='True'
                ARTEMIS_URL_JORMUN='http://navitia_jormungandr_1'
                ARTEMIS_URL_TYR='http://navitia_tyr_web_1'
                ARTEMIS_DATA_DIR='artemis_data'
                ARTEMIS_REFERENCE_FILE_PATH='artemis_references'
                ARTEMIS_CITIES_DB='postgresql://navitia:navitia@navitia_cities_database_1/cities'
            }
            steps {
                echo 'Run pytest'
                sh 'py.test artemis/tests -x'
            }
        }
    }
    post {
        failure { echo 'Job has failed' }
        success { echo 'Job is successful' }
    }
}
