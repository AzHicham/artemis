pipeline {
    agent any
    stages {
        stage('Docker Compose Up') {
            steps {
                sh 'make start'
            }
        }
        stage('Run Artemis Test') {
            steps {
                sh 'make test'
            }
        }
    }
    post {
        cleanup { sh 'make clean' }
        failure { echo 'Job has failed' }
        success { echo 'Job is successful' }
    }
}
