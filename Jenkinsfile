pipeline {
    agent any
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
            steps { sh 'make test' }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/*', fingerprint: true
            junit 'junit/*.xml'
        }
        failure { sh 'make logs' }
        success { echo 'Job is successful, HO YEAH !' }
        cleanup { sh 'make clean' }
    }
}
