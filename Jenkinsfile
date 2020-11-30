pipeline {
    agent any
    parameters {
        string(name: 'ARTEMIS_REPO', defaultValue: 'git@github.com:CanalTP/artemis.git', description: 'Artemis repository address')
        string(name: 'ARTEMIS_BRANCH', defaultValue: 'master', description: 'Artemis branch to checkout')
        string(name: 'ARTEMIS_DATA_REPO', defaultValue: 'git@github.com:CanalTP/artemis_data.git', description: 'Artemis_data repository address')
        string(name: 'ARTEMIS_DATA_BRANCH', defaultValue: 'master', description: 'Artemis_data branch to checkout')
        string(name: 'ARTEMIS_REF_REPO', defaultValue: 'git@github.com:CanalTP/artemis_references.git', description: 'Artemis_references repository address')
        string(name: 'ARTEMIS_REF_BRANCH', defaultValue: 'master', description: 'Artemis_references branch to checkout')
    }
    stages {
        stage('Pull data and images') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'jenkins-core-ssh',
                        keyFileVariable: 'SSH_KEY_FILE',
                        passphraseVariable: '',
                        usernameVariable: 'jenkins-kisio-core')
                ]) {
                    // We have to manually pull data from artemis_data,
                    // because pulling LFS repos from submodule isn't supported yet.
                    sh '''
                        eval `ssh-agent`
                        ssh-add $SSH_KEY_FILE
                        git clone "${params.ARTEMIS_REPO}"      -b "${params.ARTEMIS_BRANCH}" .
                        git clone "${params.ARTEMIS_DATA_REPO}" -b "${params.ARTEMIS_DATA_BRANCH}" ./artemis_data
                        git clone "${params.ARTEMIS_REF_REPO}"  -b "${params.ARTEMIS_REF_BRANCH}" ./artemis_ref
                        make pull

                    '''
                }
            }
        }
        stage('Docker Compose Up') {
            steps { sh 'make start' }
        }
        stage('Run Artemis Test') {
            environment {
                // Examples :
                // If you only want to run IDFM tests
                //      PYTEST = 'idfm_test.py'
                // To stop on the first failing test
                //      PYTEST_ARG = '--exitfirst'
                PYTEST      = ''
                PYTEST_ARG  = ''
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
        failure { sh 'make logs' }
        success { echo 'Job is successful, HO YEAH !' }
        cleanup {
            // shutdown dockers
            sh 'make clean'
            // remove files on disk
            cleanWs()
        }
    }
}
