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
            steps { sh 'make test' }
        }
    }
    post {
        failure { sh 'make logs' }
        success { echo 'Job is successful, HO YEAH !' }
        cleanup { sh 'make clean' }
    }
}
