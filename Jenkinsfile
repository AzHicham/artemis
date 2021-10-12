pipeline {
    agent any
    parameters {
        string(name: 'artemis_repo', defaultValue: 'CanalTP/artemis', description: 'Artemis gihub repository')
        string(name: 'artemis_branch', defaultValue: 'master', description: 'Artemis branch to checkout')
        string(name: 'artemis_data_repo', defaultValue: 'CanalTP/artemis_data', description: 'Artemis_data github repository ')
        string(name: 'artemis_data_branch', defaultValue: 'master', description: 'Artemis_data branch to checkout')
        string(name: 'artemis_ref_repo', defaultValue: 'CanalTP/artemis_references', description: 'Artemis_references github repository ')
        string(name: 'artemis_ref_branch', defaultValue: 'artemis_ng', description: 'Artemis_references branch to checkout')
        string(name: 'navitia_docker_compose_repo', defaultValue: 'CanalTP/navitia-docker-compose', description: 'Navitia_docker_compose github repository')
        string(name: 'navitia_docker_compose_branch', defaultValue: 'master', description: 'Navitia_docker_compose branch to checkout')
        string(name: 'commit_id', defaultValue: 'undefined', description: 'Commit sha')
        string(name: 'commit_message', defaultValue: 'title', description: 'Commit title')
        string(name: 'commit_timestamp', defaultValue: 'date', description: 'Commit timestamp')
        string(name: 'commit_url', defaultValue: 'https://github.com/CanalTP/navitia', description: 'Repo URL')
        string(name: 'commit_username', defaultValue: 'username', description: 'Commiter')
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
    options {
        disableConcurrentBuilds()
        ansiColor('xterm')
    }
    stages {
        stage('Pull data') {
          steps {
              withCredentials([usernamePassword(credentialsId: 'jenkins-app-core', usernameVariable: 'GITHUB_APP', passwordVariable: 'GITHUB_TOKEN')]) {
                  sh """
                  rm -rf ./artemis
                  git clone https://${GITHUB_APP}:${GITHUB_TOKEN}@github.com/${params.artemis_repo}.git --branch ${params.artemis_branch} ./artemis
                  git clone https://${GITHUB_APP}:${GITHUB_TOKEN}@github.com/${params.artemis_data_repo}.git --branch ${params.artemis_data_branch} ./artemis/artemis_data
                  git clone https://${GITHUB_APP}:${GITHUB_TOKEN}@github.com/${params.artemis_ref_repo}.git --branch ${params.artemis_ref_branch} ./artemis/artemis_references
                  git clone https://${GITHUB_APP}:${GITHUB_TOKEN}@github.com/${params.navitia_docker_compose_repo}.git --branch ${params.navitia_docker_compose_branch} ./artemis/navitia-docker-compose
                  git clone https://${GITHUB_APP}:${GITHUB_TOKEN}github.com/CanalTP/artemis_benchmark.git --branch main ./artemis_benchmark
                  """
              }
          }
      }
		stage('Clean Docker containers and images') {
			steps {
				dir("./artemis/") {
					// Tear down Navitia stack
					sh 'make stop TAG=local || exit 0'
					// remove images
					sh 'make clean_images TAG=local || exit 0'
					// Force stop artemis container (container executing tests)
					sh 'make clean_artemis || exit 0'
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
                withCredentials([usernamePassword(credentialsId: 'jenkins-app-core', usernameVariable: 'GITHUB_APP', passwordVariable: 'GITHUB_TOKEN')]) {
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
                PYTEST_ARGS  = '--benchmark-json benchmark.json'
            }
            steps {
                dir("./artemis/") {
                    sh "make test"
                }
            }
        }
        stage('Push benchmarks') {
            environment {
                COMMIT_ID        = "${params.commit_id}"
                COMMIT_MESSAGE   = sh(returnStdout: true, script: "echo '${params.commit_message}' | tr '\n' ' ' ").trim()
                COMMIT_TIMESTAMP = "${params.commit_timestamp}"
                COMMIT_URL       = "${params.commit_url}"
                COMMIT_USERNAME  = "${params.commit_username}"
            }
            when { expression { return "${params.navitia_branch}" == 'dev' && "${params.commit_id}" != 'undefined'} }
            steps {
              withCredentials([usernamePassword(credentialsId: 'jenkins-app-core', usernameVariable: 'GITHUB_APP', passwordVariable: 'GITHUB_TOKEN')]) {
                  sh """
                    cp -f ./artemis/benchmark.json ./artemis_benchmark/benchmark.json
                    cd ./artemis_benchmark
                    git config user.name "Jenkins"
                    git add benchmark.json
                    git commit -m "Update benchmarks"
                    git push
                    curl -X POST --url https://api.github.com/repos/CanalTP/artemis_benchmark/dispatches -H 'Content-type: application/json' \
                    -H "authorization: token $GITHUB_TOKEN" \
                    --data '{ "event_type": "bench-report", "client_payload": { "commit_id": "${COMMIT_ID}", "commit_message": "${COMMIT_MESSAGE}", "commit_timestamp": "${COMMIT_TIMESTAMP}", "commit_url": "${COMMIT_URL}", "commit_username": "${COMMIT_USERNAME}" }  }'
                  """
              }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'artemis/output/**/*', allowEmptyArchive :true, fingerprint: true
            archiveArtifacts artifacts: 'artemis/benchmark.json', allowEmptyArchive :true, fingerprint: true
            junit testResults: 'artemis/junit/*.xml', allowEmptyResults: true
            dir("./artemis/") {
                sh 'make logs TAG=local > logs || exit 0'
            }
            archiveArtifacts artifacts: 'artemis/logs', allowEmptyArchive :true
        }
        success { echo 'Job is successful, HO YEAH !' }
        failure {
            withCredentials([string(credentialsId: 'navitia_core_team_slack_chan', variable: 'NAVITIA_CORE_TEAM_SLACK_CHAN')]) {
                sh '''
                    curl -X POST -H 'Content-type: application/json' \
                    --data '{"text":":warning: Artemis NG failed. See https://jenkins-core.canaltp.fr/job/artemis_ng/"}' $NAVITIA_CORE_TEAM_SLACK_CHAN
                '''
            }
        }
        cleanup {
            dir("./artemis/") {
				// Tear down Navitia stack
				sh 'make stop TAG=local || exit 0'
				// remove images
				sh 'make clean_images TAG=local || exit 0'
				// Force stop artemis container (container executing tests)
				sh 'make clean_artemis || exit 0'
            }
            cleanWs()
        }
    }
}
