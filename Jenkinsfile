pipeline {
    agent any
    parameters {
        string(name: 'artemis_repo', defaultValue: 'CanalTP/artemis', description: 'Artemis gihub repository')
        string(name: 'artemis_branch', defaultValue: 'master', description: 'Artemis branch to checkout')
        string(name: 'artemis_data_repo', defaultValue: 'CanalTP/artemis_data', description: 'Artemis_data github repository ')
        string(name: 'artemis_data_branch', defaultValue: 'master', description: 'Artemis_data branch to checkout')
        string(name: 'artemis_ref_repo', defaultValue: 'CanalTP/artemis_references', description: 'Artemis_references github repository ')
        string(name: 'artemis_ref_branch', defaultValue: 'master', description: 'Artemis_references branch to checkout')
        string(name: 'navitia_docker_compose_repo', defaultValue: 'CanalTP/navitia-docker-compose', description: 'Navitia_docker_compose github repository')
        string(name: 'navitia_docker_compose_branch', defaultValue: 'master', description: 'Navitia_docker_compose branch to checkout')
        choice(
            name: 'navitia_branch',
            choices: ['dev', 'release'],
            description: 'Which branch of navitia to use for artemis tests'
        )
    }
    stages {
        stage('Pull data') {
            steps {
                withCredentials(
                [sshUserPrivateKey(
                    credentialsId: 'jenkins-core-ssh',
                    keyFileVariable: 'SSH_KEY_FILE',
                    passphraseVariable: '',
                    usernameVariable: 'jenkins-kisio-core')])
                {
                    sh """
                    eval `ssh-agent`
                    ssh-add $SSH_KEY_FILE
                    git clone git@github.com:${params.artemis_repo}.git --branch ${params.artemis_branch} .
                    git clone git@github.com:${params.artemis_data_repo}.git --branch ${params.artemis_data_branch} ./artemis_data
                    git clone git@github.com:${params.artemis_ref_repo}.git --branch ${params.artemis_ref_branch} ./artemis_references
                    git clone git@github.com:${params.navitia_docker_compose_repo}.git --branch ${params.navitia_docker_compose_branch} ./navitia-docker-compose
                    """
                }
            }
        }

        stage('Build docker images') {
            steps {
                environment {
                    BRANCH  = "${params.navitia_branch}"
                }
                withCredentials([string(credentialsId: 'jenkins-core-github-access-token', variable: 'GITHUB_TOKEN')]) {
                    dir("./navitia-docker-compose/builder_from_package/") {
                        sh './build.sh -o $GITHUB_TOKE} -b $BRANCH -t local'
                    }
                }
            }
        }
        stage('Pull remaining images') {
            steps { sh 'make pull_available TAG=local' }
        }
        stage('Start all dockers') {
            steps { sh 'make start TAG=local' }
        }
        stage('Run Artemis Test') {
            environment {
                // Examples :
                // If you only want to run IDFM tests
                //      PYTEST = 'idfm_test.py'
                // To stop on the first failing test
                //      PYTEST_ARG = '--exitfirst'
                // To run only Experimental tests
                //      PYTEST_ARG = '-k"Experimental"'
                PYTEST      = ''
                PYTEST_ARGS  = ''
            }

            steps {
                sh "make test"

            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/**/*', fingerprint: true
            junit 'junit/*.xml'
        }
        failure { sh 'make logs TAG=local' }
        success { echo 'Job is successful, HO YEAH !' }
        cleanup {
            // shutdown dockers
            sh 'make stop TAG=local'
            // remove images
            sh 'make clean_images TAG=local'
            // remove files on disk
            cleanWs()
        }
    }
}
