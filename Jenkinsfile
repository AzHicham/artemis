pipeline {
    agent any
    parameters {
        string(name: 'artemis_repo', defaultValue: 'CanalTP/artemis', description: 'Artemis gihub repository')
        string(name: 'artemis_branch', defaultValue: 'master', description: 'Artemis branch to checkout')
        string(name: 'artemis_data_repo', defaultValue: 'CanalTP/artemis_data', description: 'Artemis_data github repository ')
        string(name: 'artemis_data_branch', defaultValue: 'master', description: 'Artemis_data branch to checkout')
        string(name: 'artemis_ref_repo', defaultValue: 'pbench/artemis_references', description: 'Artemis_references github repository ')
        string(name: 'artemis_ref_branch', defaultValue: 'artemis_ng', description: 'Artemis_references branch to checkout')
        string(name: 'navitia_docker_compose_repo', defaultValue: 'CanalTP/navitia-docker-compose', description: 'Navitia_docker_compose github repository')
        string(name: 'navitia_docker_compose_branch', defaultValue: 'master', description: 'Navitia_docker_compose branch to checkout')
        choice(
            name: 'event',
            choices: ['push', 'pull_request'],
            description: 'Which kind of event triggered the github workflow. '
        )
        string(
            name: 'navitia_branch',
            defaultValue: 'dev',
            description: """Which branch of navitia to use for artemis tests. \
                            If `event=push` navitia_branch can be `dev` or `release`. \
                            If `event=pull_request` navitia_branch is the name of the branch used for the pull request."""
        )
        string(
            name: 'navitia_fork',
            defaultValue: 'CanalTP',
            description: 'Which fork of navitia to use. Only used when `event=pull_request` '
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
                    rm -rf ./artemis
                    git clone git@github.com:${params.artemis_repo}.git --branch ${params.artemis_branch} ./artemis
                    git clone git@github.com:${params.artemis_data_repo}.git --branch ${params.artemis_data_branch} ./artemis/artemis_data
                    git clone git@github.com:${params.artemis_ref_repo}.git --branch ${params.artemis_ref_branch} ./artemis/artemis_references
                    git clone git@github.com:${params.navitia_docker_compose_repo}.git --branch ${params.navitia_docker_compose_branch} ./artemis/navitia-docker-compose
                    """
                }
            }
        }

        stage('Build docker images') {
            environment {
                BRANCH  = "${params.navitia_branch}"
                EVENT   = "${params.event}"
                FORK    = "${params.navitia_fork}"
            }
            steps {

                withCredentials([string(credentialsId: 'jenkins-core-github-access-token', variable: 'GITHUB_TOKEN')]) {
                    dir("./artemis/navitia-docker-compose/builder_from_package/") {
                        sh "./build.sh -o ${GITHUB_TOKEN} -t local -e ${EVENT} -f ${FORK} -b ${BRANCH}"
                    }
                }
            }
        }
        stage('Pull remaining images') {
            steps {
                dir("./artemis/") {
                    sh 'make pull_available TAG=local'
                }
            }
        }
        stage('Start all dockers') {
            steps {
                dir("./artemis/") {
                    sh 'make start TAG=local'
                }
            }
        }
        stage('Run Artemis Test') {
            environment {
                // Examples :
                // If you only want to run IDFM tests
                //      PYTEST = 'idfm_test.py'
                // To stop on the first failing test
                //      PYTEST_ARG = '--exitfirst'
                PYTEST      = ''
                PYTEST_ARGS  = ''
            }

            steps {
                dir("./artemis/") {
                    sh "make test"
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'artemis/output/**/*', allowEmptyArchive :true, fingerprint: true
            junit testResults: 'artemis/junit/*.xml', allowEmptyResults: true
            dir("./artemis/") {
                sh 'make logs TAG=local > logs || exit 0'
            }
            archiveArtifacts artifacts: 'artemis/logs', allowEmptyArchive :true
        }
        success { echo 'Job is successful, HO YEAH !' }
        cleanup {
            dir("./artemis/") {
            // shutdown dockers
                sh 'make stop TAG=local || exit 0'
                // remove images
                sh 'make clean_images TAG=local || exit 0'
                // remove files on disk
            }
            cleanWs()
        }
    }
}
