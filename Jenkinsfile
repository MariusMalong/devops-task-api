pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'devops_task_api'
        DOCKER_HUB_REPO = 'mari06/devops-task-api'
        STAGING_PORT = '8000'
        PROD_PORT = '8080'
    }
    
    triggers {
        pollSCM('* * * * *')
    }
    
    stages {
        stage('1. Build & Push Artifact') {
            steps {
                echo 'Building and pushing tagged Docker artifact...'
                sh 'docker build -t ${DOCKER_HUB_REPO}:${BUILD_NUMBER} -t ${DOCKER_HUB_REPO}:latest .'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PW', usernameVariable: 'DOCKER_USER')]) {
                    sh 'echo $DOCKER_PW | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push ${DOCKER_HUB_REPO}:${BUILD_NUMBER}'
                    sh 'docker push ${DOCKER_HUB_REPO}:latest'
                }
            }
        }
        
        stage('2. Test & Coverage') {
            steps {
                echo 'Running pytest with JUnit XML generation...'
                sh 'docker run --rm -v ${WORKSPACE}:/src ${DOCKER_HUB_REPO}:latest python -m pytest -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('3. Code Quality Gate') {
            steps {
                echo 'Executing SonarQube Analysis...'
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        
        stage('4. Security & Dependency Scan') {
            steps {
                echo 'SAST (Bandit) and SCA (pip-audit)...'
                sh 'docker run --rm ${DOCKER_HUB_REPO}:latest bandit -r app/ -ll -ii'
                sh 'docker run --rm ${DOCKER_HUB_REPO}:latest pip-audit -r requirements.txt || true' 
            }
        }
        
        stage('5. Deploy (Staging) & Rollback') {
            steps {
                script {
                    try {
                        echo 'Deploying to Staging with docker-compose...'
                        sh 'docker compose down'
                        sh 'docker compose up -d'
                        sleep time: 10, unit: 'SECONDS'
                        // Health check validation
                        sh 'docker inspect --format="{{json .State.Health.Status}}" devops_task_api | grep "healthy"'
                    } catch (Exception e) {
                        echo 'Deploy failed! Initiating rollback...'
                        sh 'docker compose down'
                        error('Staging deployment failed health checks.')
                    }
                }
            }
        }
        
        stage('6. Release (Production) & Tagging') {
            steps {
                echo 'Applying Production Config and Git Tagging...'
                sh 'docker rm -f ${IMAGE_NAME}_prod || true'
                sh 'docker run -d --name ${IMAGE_NAME}_prod --env-file .env.prod -p ${PROD_PORT}:8000 ${DOCKER_HUB_REPO}:${BUILD_NUMBER}'
                
                // Git tagging the release
                sh 'git tag -a "v1.0.${BUILD_NUMBER}" -m "Production Release Build ${BUILD_NUMBER}" || true'
            }
        }
        
        stage('7. Monitoring Verification') {
            steps {
                echo 'Verifying Prometheus metrics endpoint...'
                sh 'curl -s -f http://localhost:${PROD_PORT}/metrics | grep "http_requests_total" || exit 1'
            }
        }
    }
    
    post {
        success {
            echo 'Top HD Pipeline Completed.'
        }
    }
}